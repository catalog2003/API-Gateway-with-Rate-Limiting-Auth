from app.services.rate_limiter_service import RateLimiterService


def test_rate_limiter_allows_request(mocker):
    service = RateLimiterService()

    mock_script = mocker.Mock()
    mock_script.return_value = [1, 4]

    service.lua_script = mock_script

    allowed, remaining, capacity = service.allow_request(
        user_id="123",
        role="free"
    )

    assert allowed is True
    assert remaining == 4
    assert capacity == 5  # free role has capacity of 5