from flask import Blueprint, request, jsonify, current_app
from services.ai_service import analyze_text
from services.erp_service import create_project_with_tasks
from services.mattermost_service import send_message

bp = Blueprint("mattermost", __name__)

@bp.route("/mattermost", methods=["POST"])
def handle_webhook():
    token = request.form.get("token")
    if token != current_app.config["MATTERMOST_TOKEN"]:
        return jsonify({"text": "❌ Invalid token"}), 403

    text = request.form.get("text", "")
    # 1) Gọi AI để parse intent
    ai_resp = analyze_text(text)

    intent = ai_resp.get("intent")
    if intent == "initiate_workflow":
        wf_name = ai_resp.get("workflow_name")
        tasks   = ai_resp.get("tasks", [])
        # 2) Tạo project + tasks lên ERPNext
        project_id = create_project_with_tasks(wf_name, tasks)
        # 3) Gửi confirm về Mattermost
        send_message(f"✅ Created *{wf_name}* (ID={project_id}) with {len(tasks)} tasks.")
    else:
        send_message("🤖 Sorry, I didn't understand your request.")

    return "", 200
