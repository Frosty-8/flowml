from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
import os
import asyncio
import logging

# Routes
from flowml.api.routes import upload, preview, cleaning, visualize, metrics, pipeline, jobs
from flowml.api.middleware import MetricsMiddleware
from flowml.api.websocket import router as ws_router

# Core
from flowml.runtime.state import registry
from flowml.runtime.scheduler import set_event_loop
from flowml.storage.sqlite import init_db
from flowml.logging.rich_logger import setup_logger


# ---------------- LOGGING ---------------- #
setup_logger()
logger = logging.getLogger(__name__)


# ---------------- APP FACTORY ---------------- #
def create_app():
    init_db()

    app = FastAPI(
        title="FlowML API",
        version="0.1.0"
    )

    # ---------------- CORS ---------------- #
    app.add_middleware(
        CORSMiddleware,
        allow_origins=["*"],   # change in production
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

    # ---------------- METRICS ---------------- #
    app.add_middleware(MetricsMiddleware, registry=registry)

    # ---------------- API ROUTES ---------------- #
    app.include_router(upload.router, prefix="/upload", tags=["Upload"])
    app.include_router(preview.router, prefix="/preview", tags=["Preview"])
    app.include_router(cleaning.router, prefix="/clean", tags=["Cleaning"])
    app.include_router(visualize.router, prefix="/visualize", tags=["Visualization"])
    app.include_router(metrics.router, prefix="/metrics", tags=["Metrics"])
    app.include_router(pipeline.router, prefix="/pipeline", tags=["Pipeline"])
    app.include_router(jobs.router, prefix="/jobs", tags=["Jobs"])
    app.include_router(ws_router)

    # ---------------- EVENT LOOP FIX ---------------- #
    @app.on_event("startup")
    async def startup_event():
        loop = asyncio.get_running_loop()
        set_event_loop(loop)
        logger.info("Event loop initialized for scheduler")

    # ---------------- FRONTEND (REACT) ---------------- #

    FRONTEND_PATH = os.path.join(os.path.dirname(__file__), "..", "..", "frontend", "dist")
    FRONTEND_PATH = os.path.abspath(FRONTEND_PATH)

    if os.path.exists(FRONTEND_PATH):
        logger.info("Serving React frontend...")

        # Serve static assets
        app.mount(
            "/assets",
            StaticFiles(directory=os.path.join(FRONTEND_PATH, "assets")),
            name="assets"
        )

        # Catch-all route → React app
        @app.get("/{full_path:path}")
        async def serve_react_app(full_path: str):
            index_file = os.path.join(FRONTEND_PATH, "index.html")
            return FileResponse(index_file)

    else:
        logger.warning("Frontend build not found. Please run `npm run build` in /frontend")

        @app.get("/")
        def fallback():
            return {
                "message": "Frontend not built",
                "solution": "Run `cd frontend && npm install && npm run build`"
            }

    return app