import time
from starlette.middleware.base import BaseHTTPMiddleware
from fastapi import Request


class MetricsMiddleware(BaseHTTPMiddleware):
    def __init__(self, app, registry):
        super().__init__(app)
        self.registry = registry

    async def dispatch(self, request: Request, call_next):
        start = time.time()

        try:
            response = await call_next(request)
            latency = time.time() - start

            self.registry.metrics_engine.log_request(
                request.url.path, latency
            )

            return response

        except Exception:
            self.registry.metrics_engine.log_error()
            raise