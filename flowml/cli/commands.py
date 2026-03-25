import typer
import json
import requests

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
