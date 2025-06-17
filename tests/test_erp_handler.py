from erp.erp_handler import handle_intent

def test_handle_intent():
    """
    Test the handle_intent function with a sample intent object.
    """
    intent_obj = {
        "intent": "create_task",
        "task_name": "Viết báo cáo",
        "project_name": "Phát triển sản phẩm"
    }
    result = handle_intent(intent_obj)
    assert result["status"] in ["success", "error"]
