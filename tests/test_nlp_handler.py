from nlp.nlp_handler import analyze_text

def test_analyze_text():
    """
    Test the analyze_text function with a sample input.
    """
    text = "Tạo nhiệm vụ 'Viết báo cáo' cho dự án 'Phát triển sản phẩm'"
    result = analyze_text(text)
    assert result["intent"] == "create_task"
    assert result["task_name"] == "Viết báo cáo"
    assert result["project_name"] == "Phát triển sản phẩm"
