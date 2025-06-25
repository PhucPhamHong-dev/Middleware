#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import os
import json
import requests
from datetime import date, datetime, timedelta
from flask import Flask, request, jsonify
from dotenv import load_dotenv

load_dotenv()

# ————— Cấu hình từ .env —————
MM_INCOMING = os.getenv("MM_INCOMING_WEBHOOK_URL")
ERP_URL     = os.getenv("ERP_URL", "").rstrip("/")
ERP_KEY     = os.getenv("ERP_API_KEY")
ERP_SECRET  = os.getenv("ERP_API_SECRET")
GROQ_TOKEN  = os.getenv("GROQ_TOKEN")

HEADERS_ERP = {
    "Authorization": f"token {ERP_KEY}:{ERP_SECRET}",
    "Content-Type": "application/json"
}
HEADERS_GROQ = {
    "Authorization": f"Bearer {GROQ_TOKEN}",
    "Content-Type": "application/json"
}

app = Flask(__name__)
print("→ Mattermost Incoming:", MM_INCOMING)
print("→ ERPNext URL       :", ERP_URL)
print("→ GROQ Token loaded:", bool(GROQ_TOKEN))


def fix_relative_date(text, parsed_date):
   
    try:
        d0 = datetime.fromisoformat(parsed_date).date()
    except Exception:
        return parsed_date
    today = date.today()
    t = text.lower()
    if "ngày mai" and "mai" in t and d0 <= today:
        return (today + timedelta(days=1)).isoformat()
    if "ngày mốt" and "mốt" in t and d0 <= today:
        return (today + timedelta(days=2)).isoformat()
    return parsed_date


def parse_task(text):
    print(">> [parse_task] nhận text:", text)
    url = "https://api.groq.com/openai/v1/chat/completions"
    system_prompt = (
        f"Hôm nay là {date.today().isoformat()}. "
        "Bạn là trợ lý trích xuất task. "
        "Trả về đúng 1 JSON object với 3 key: "
        "`assignee` (tên), `date` (YYYY-MM-DD), `description` (nội dung)."
    )
    body = {
        "model": "llama3-8b-8192",
        "messages": [
            {"role": "system", "content": system_prompt},
            {"role": "user",   "content": text}
        ],
        "temperature": 0,
        "response_format": {"type": "json_object"}
    }

    resp = requests.post(url, headers=HEADERS_GROQ, json=body)
    print(">> [parse_task] Groq status:", resp.status_code)
    print(">> [parse_task] Groq resp body:", resp.text)
    resp.raise_for_status()

    # parse JSON string từ choices
    content = resp.json()["choices"][0]["message"]["content"]
    print(">> [parse_task] Groq raw content:", content)
    data = json.loads(content)
    print(">> [parse_task] Parsed JSON:", data)

    # fix lại nếu ngày AI trả <= hôm nay
    due = fix_relative_date(text, data["date"])
    print(f">> [parse_task] final due_date: {due}")

    return {
        "assignee":    f"{data['assignee']}@yourcorp.com",
        "due_date":    due,
        "description": data["description"]
    }


def send_confirmation(msg):
    print(">> [send_confirmation] gửi về MM:", msg)
    r = requests.post(MM_INCOMING, json={"text": msg})
    print(">> [send_confirmation] status:", r.status_code, r.text)


@app.route("/create_task", methods=["POST"])
@app.route("/mattermost-webhook", methods=["POST"])
def webhook():
    print("\n=== New request ===")
    print(">> Headers:", dict(request.headers))
    raw = request.get_data(as_text=True)
    print(">> Raw body:", raw)

    # Slash Command?
    if request.form.get("command"):
        flow = "slash"
        text = request.form["text"].strip()
        user = request.form.get("user_name")
        print(f">> [webhook] Slash flow: user={user}, text={text}")
    else:
        # Outgoing Webhook (JSON)
        flow = "outgoing"
        payload = request.get_json(silent=True)
        if not isinstance(payload, dict):
            print("!! [webhook] Invalid JSON")
            return "Invalid JSON", 400

        tw = payload.get("trigger_words") or payload.get("trigger_word")
        print(">> [webhook] trigger_words:", tw)
        ok = False
        if isinstance(tw, list) and "task" in [w.lower() for w in tw]:
            ok = True
        if isinstance(tw, str) and tw.lower() == "task":
            ok = True
        if not ok:
            print(">> [webhook] skip non-task")
            return "", 200

        text = payload.get("text", "").strip()
        user = payload.get("user_name")
        print(f">> [webhook] Outgoing flow: user={user}, text={text}")

    # Parse
    try:
        params = parse_task(text)
    except Exception as e:
        print("!! [webhook] parse_task error:", e)
        if flow == "slash":
            return jsonify({
                "response_type": "ephemeral",
                "text": f"❌ Lỗi parse: {e}"
            }), 200
        send_confirmation(f"❓ Lỗi parse hệ thống: {e}")
        return "", 200

    print(">> [webhook] params:", params)

    # Tạo ERPNext Task
    erp_payload = {
        "subject":     params["description"],
        "assigned_to": params["assignee"],
        "due_date":    params["due_date"]
    }
    print(">> [webhook] send to ERPNext:", erp_payload)
    try:
        r = requests.post(f"{ERP_URL}/api/resource/Task",
                          headers=HEADERS_ERP, json=erp_payload)
        print(">> [webhook] ERP status:", r.status_code, r.text)
        r.raise_for_status()
        tid = r.json()["data"]["name"]
        msg = (f"✅ Task “{params['description']}” (ID:{tid}) "
               f"đã tạo cho @{params['assignee'].split('@')[0]}, hạn {params['due_date']}.")
    except Exception as e:
        print("!! [webhook] ERPNext error:", e)
        msg = f"❌ Tạo Task thất bại: {e}"

    # Gửi confirmation / trả về Slash
    if flow == "slash":
        print(">> [webhook] slash response:", msg)
        return jsonify({"response_type": "in_channel", "text": msg}), 200
    else:
        send_confirmation(msg)
        return "", 200


if __name__ == "__main__":
    print("→ Starting Flask on 0.0.0.0:8080 (debug=True)")
    app.run(host="0.0.0.0", port=8080, debug=True)
