from app.services.extraction_service import ExtractionService


def test_extract_text_success(mocker):
    mock_response = mocker.Mock()
    mock_response.status_code = 200
    mock_response.text = """
    <html>
        <head><title>Test Page</title></head>
        <body>Hello World</body>
    </html>
    """

    mocker.patch("requests.get", return_value=mock_response)

    service = ExtractionService()
    result = service.extract_text(user_id="123", url="http://test.com")

    assert result["title"] == "Test Page"
    assert "Hello World" in result["text"]
    assert result["word_count"] > 0