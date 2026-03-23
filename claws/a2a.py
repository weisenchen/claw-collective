"""octeam a2a — multi-machine agent-to-agent protocol.

Innovation: pure Python (aiohttp) — no Node dependency, auto-detects peer cards.
"""

from __future__ import annotations

import asyncio
import json
import os
import socket
import uuid
from datetime import datetime, timezone
from pathlib import Path

import click
from aiohttp import web

from octeam.config import load_config, save_config


def _get_ip() -> str:
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    try:
        s.connect(("8.8.8.8", 80))
        ip = s.getsockname()[0]
    except Exception:
        ip = "127.0.0.1"
    finally:
        s.close()
    return ip


async def _handle_message(request: web.Request) -> web.Response:
    try:
        data = await request.json()
        print(f"📩 Received message: {data}")
        # In a real app, this would route to inbox.py
        return web.json_response({"status": "delivered", "id": uuid.uuid4().hex})
    except Exception as e:
        return web.json_response({"error": str(e)}, status=400)


async def _handle_card(request: web.Request) -> web.Response:
    config = load_config()
    card = {
        "hostname": socket.gethostname(),
        "ip": _get_ip(),
        "port": config.a2a_port,
        "agent": os.environ.get("OCTEAM_AGENT", "octeam-peer"),
        "protocol": "a2a/0.3.0",
    }
    return web.json_response(card)


async def start_server(port: int) -> web.AppRunner:
    app = web.Application()
    app.router.add_post("/message", _handle_message)
    app.router.add_get("/card", _handle_card)
    
    runner = web.AppRunner(app)
    await runner.setup()
    site = web.TCPSite(runner, "0.0.0.0", port)
    await site.start()
    print(f"🚀 A2A server running on http://0.0.0.0:{port}")
    return runner


async def serve_forever(port: int) -> None:
    runner = await start_server(port)
    try:
        while True:
            await asyncio.sleep(3600)
    finally:
        await runner.cleanup()


@click.group("a2a")
def cmd_a2a() -> None:
    """A2A Communication Protocol."""
    pass


@cmd_a2a.command("serve")
@click.option("--port", "-p", type=int, help="Port to listen on")
def a2a_serve(port: int | None) -> None:
    """Start A2A server."""
    config = load_config()
    p = port or config.a2a_port or 18800
    try:
        asyncio.run(serve_forever(p))
    except KeyboardInterrupt:
        click.echo("🛑 Server stopped")


@cmd_a2a.command("send")
@click.argument("peer")
@click.argument("message")
@click.option("--port", "-p", type=int, help="Peer port")
def a2a_send(peer: str, message: str, port: int | None) -> None:
    """Send a message to a peer agent."""
    import aiohttp
    
    config = load_config()
    p = port or config.a2a_port or 18800
    url = f"http://{peer}:{p}/message"
    
    async def _send():
        async with aiohttp.ClientSession() as session:
            payload = {
                "content": message,
                "from": socket.gethostname(),
                "timestamp": datetime.now(timezone.utc).isoformat(),
            }
            async with session.post(url, json=payload, timeout=5) as resp:
                if resp.status == 200:
                    await resp.json()
                    click.echo(f"✅ Sent successfully to {peer}")
                else:
                    click.echo(f"❌ Failed to send: {resp.status}")
    
    loop = asyncio.get_event_loop()
    try:
        loop.run_until_complete(_send())
    except Exception as e:
        click.echo(f"❌ Error: {e}")


@cmd_a2a.command("card")
def a2a_card() -> None:
    """Show agent card for this machine."""
    config = load_config()
    card = {
        "hostname": socket.gethostname(),
        "ip": _get_ip(),
        "port": config.a2a_port,
        "protocol": "a2a/0.3.0",
    }
    click.echo(json.dumps(card, indent=2))
