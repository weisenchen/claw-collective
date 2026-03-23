"""Claw Collective dashboard — web-based monitoring.

Innovation: single Python process (aiohttp + Jinja2), zero-config, reads ~/.claws/
"""

from __future__ import annotations

import asyncio
from pathlib import Path

import click
from aiohttp import web
import jinja2
import aiohttp_jinja2

from claws.config import load_config, data_dir
from claws.team import team_list


@aiohttp_jinja2.template("index.html")
async def index(request: web.Request) -> dict:
    config = load_config()
    teams_root = data_dir() / "teams"
    teams = []
    if teams_root.exists():
        for d in sorted(teams_root.iterdir()):
            if d.is_dir():
                teams.append({"name": d.name})
    
    return {
        "teams": teams,
        "config": config.model_dump(),
        "title": "Claw Collective Dashboard"
    }


async def start_dashboard(port: int) -> None:
    app = web.Application()
    
    # Setup Jinja2
    template_dir = Path(__file__).parent / "templates"
    template_dir.mkdir(exist_ok=True)
    
    # Create a basic template if it doesn't exist
    index_html = template_dir / "index.html"
    if not index_html.exists():
        index_html.write_text("""
<!DOCTYPE html>
<html>
<head>
    <title>{{ title }}</title>
    <style>
        body { font-family: sans-serif; margin: 2rem; background: #f4f4f9; color: #333; }
        .card { background: white; padding: 1.5rem; border-radius: 8px; box-shadow: 0 2px 4px rgba(0,0,0,0.1); margin-bottom: 1rem; }
        h1 { color: #2c3e50; }
        .team-list { display: grid; grid-template-columns: repeat(auto-fill, minmax(200px, 1fr)); gap: 1rem; }
        .team-card { background: #ecf0f1; padding: 1rem; border-radius: 4px; text-align: center; font-weight: bold; }
    </style>
</head>
<body>
    <h1>🦞 Claw Collective Dashboard</h1>
    <div class="card">
        <h2>Teams</h2>
        <div class="team-list">
            {% for team in teams %}
                <div class="team-card">{{ team.name }}</div>
            {% else %}
                <p>No teams found.</p>
            {% endfor %}
        </div>
    </div>
    <div class="card">
        <h2>Configuration</h2>
        <pre>{{ config | tojson(indent=2) }}</pre>
    </div>
</body>
</html>
""", encoding="utf-8")

    aiohttp_jinja2.setup(app, loader=jinja2.FileSystemLoader(str(template_dir)))
    app.router.add_get("/", index)
    
    runner = web.AppRunner(app)
    await runner.setup()
    site = web.TCPSite(runner, "0.0.0.0", port)
    await site.start()
    print(f"🌐 Dashboard running on http://localhost:{port}")
    
    while True:
        await asyncio.sleep(3600)


@click.command("dashboard")
@click.option("--port", "-p", default=8080, help="Port to listen on")
def cmd_dashboard(port: int) -> None:
    """Start the web dashboard."""
    try:
        asyncio.run(start_dashboard(port))
    except KeyboardInterrupt:
        click.echo("🛑 Dashboard stopped")
