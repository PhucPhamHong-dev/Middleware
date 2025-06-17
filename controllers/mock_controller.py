from flask import Blueprint, request, jsonify

mock_bp = Blueprint("mock", __name__)

@mock_bp.route("/api", methods=["POST"])
def ai_stub():
    # Trả cố định kết quả khởi tạo workflow
    return jsonify({
        "intent": "initiate_workflow",
        "workflow_name": "DemoWorkflow",
        "tasks": [
            {"title": "Sample Task 1", "description": "This is a sample task"}
        ]
    })

@mock_bp.route("/Project", methods=["POST"])
def project_stub():
    # Giả lập tạo project
    return jsonify({"data": {"name": "PROJECT123"}})

@mock_bp.route("/Task", methods=["POST"])
def task_stub():
    # Giả lập tạo task
    return jsonify({})
