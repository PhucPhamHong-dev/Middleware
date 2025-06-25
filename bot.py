#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import os
import json
import requests
import logging
from urllib.parse import urlparse
from mattermostdriver import Driver
from dotenv import load_dotenv

load_dotenv()

# ————— Cấu hình từ .env —————
# Bạn chỉ cần khai báo MM_URL, MM_BOT_TOKEN, CREATE_TASK_ENDPOINT
MM_URL               = os.getenv("MM_URL")  # e.g. "http://autoss.ddns.net:5022"
MM_BOT_TOKEN         = os.getenv("MM_BOT_TOKEN")  # Personal Access Token của bot
CREATE_TASK_ENDPOINT = os.getenv("CREATE_TASK_ENDPOINT")  # e.g. "http://localhost:8080/create_task"

if not (MM_URL and MM_BOT_TOKEN and CREATE_TASK_ENDPOINT):
    raise RuntimeError("Thiếu MM_URL, MM_BOT_TOKEN, hoặc CREATE_TASK_ENDPOINT trong .env")

# Phân tích URL để lấy host, scheme, port
parsed = urlparse(MM_URL)
scheme = parsed.scheme
host   = parsed.hostname
port   = parsed.port

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("mm-listener")

driver = Driver({
    "url":      host,
    "scheme":   scheme,
    "port":     port,
    "token":    MM_BOT_TOKEN,
    "basepath": "/api/v4",
    "verify":   False,
})

async def on_event(event):
    """
    Callback WebSocket: xử lý event 'posted'.
    Gọi CREATE_TASK_ENDPOINT khi message chứa 'task'.
    """
    event = json.loads(event)
    if event.get("event") != "posted":
        return

    post = json.loads(event["data"].get("post", "{}"))
    msg     = post.get("message", "")
    user_id = post.get("user_id")

    if post.get("props", {}).get("from_webhook") or user_id == driver.client.userid:
        return

    if "task" in msg.lower():
        logger.info(f"→ Detected 'task' in message: {msg!r}")
        payload = {
            "trigger_word": "task",
            "text":         msg,
            "user_name": (
                post.get("props", {}).get("override_username")
                or post.get("username")
                or user_id
            )
        }
        try:
            r = requests.post(CREATE_TASK_ENDPOINT, json=payload, timeout=5)
            logger.info(f"→ POST to create_task returned {r.status_code}")
        except Exception:
            logger.exception("✖ Failed calling create_task")

if __name__ == "__main__":
    # Mở WebSocket và đăng ký callback
    logger.info("🟢 Starting Mattermost listener…")
    driver.login()
   
    driver.init_websocket(on_event)
    driver.websocket_listen()
