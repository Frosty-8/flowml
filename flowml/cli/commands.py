import typer
import json
import requests
import os
import subprocess
import webbrowser
import time

app = typer.Typer()

BASE_URL = "http://127.0.0.1:8000"


# -----------------------
# Run Pipeline
# -----------------------
@app.command()
def run(config: str):
    """
    Run pipeline from JSON file
    """
    with open(config, "r") as f:
        data = json.load(f)

    res = requests.post(f"{BASE_URL}/pipeline/run", json=data)

    if res.status_code != 200:
        typer.echo("❌ Failed to start pipeline")
        return

    job = res.json()
    typer.echo(f"🚀 Job started: {job['job_id']}")


# -----------------------
# Job Status
# -----------------------
@app.command()
def status(job_id: str):
    res = requests.get(f"{BASE_URL}/pipeline/status/{job_id}")

    if res.status_code != 200:
        typer.echo("❌ Job not found")
        return

    typer.echo(res.json())


# -----------------------
# List Jobs
# -----------------------
@app.command()
def jobs():
    res = requests.get(f"{BASE_URL}/jobs/")
    typer.echo(res.json())


# -----------------------
# Preview Dataset
# -----------------------
@app.command()
def preview(dataset_id: str):
    res = requests.get(f"{BASE_URL}/preview/?dataset_id={dataset_id}")
    typer.echo(res.json())


# =====================================================
# NEW FEATURES (ADDED BELOW - NO CHANGE ABOVE)
# =====================================================

# -----------------------
# Initialize Project
# -----------------------
@app.command()
def init():
    """
    Initialize FlowML project (creates pipeline.json)
    """
    if os.path.exists("pipeline.json"):
        typer.echo("⚠️ pipeline.json already exists")
        return

    config = {
        "dataset_id": "",
        "steps": [
            {"step": "fill_nulls"},
            {"step": "drop_nulls"},
            {"step": "summary"},
        ],
    }

    with open("pipeline.json", "w") as f:
        json.dump(config, f, indent=2)

    typer.echo("✅ FlowML project initialized")
    typer.echo("📄 Created: pipeline.json")
    typer.echo("👉 Next: run 'flowml start'")


# -----------------------
# Start Server + UI
# -----------------------
@app.command()
def start():
    """
    Start FlowML server and open UI
    """
    typer.echo("🚀 Starting FlowML server...")

    try:
        process = subprocess.Popen(
            [
                "uvicorn",
                "flowml.api.server:create_app",
                "--factory",
                "--host",
                "127.0.0.1",
                "--port",
                "8000",
            ]
        )
    except FileNotFoundError:
        typer.echo("❌ Uvicorn not found. Please install it: pip install uvicorn")
        return

    # Wait for server to boot
    time.sleep(2)

    webbrowser.open("http://127.0.0.1:8000")

    typer.echo("🌐 UI running at http://127.0.0.1:8000")