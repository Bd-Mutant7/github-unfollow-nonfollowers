import pytest
from unittest.mock import Mock, patch
from unfollow_nonfollowers import GitHubUnfollower

@pytest.fixture
def unfollower():
    return GitHubUnfollower("fake_token", "testuser")

def test_find_non_followers(unfollower):
    followers = ["user1", "user2", "user3"]
    following = ["user1", "user2", "user4", "user5"]
    
    non_followers = unfollower.find_non_followers(followers, following)
    
    assert non_followers == ["user4", "user5"]
    assert len(non_followers) == 2
    assert "user1" not in non_followers

@patch('unfollow_nonfollowers.requests.get')
def test_make_request_single_page(mock_get, unfollower):
    # Mock response
    mock_response = Mock()
    mock_response.json.return_value = [{"login": "user1"}, {"login": "user2"}]
    mock_response.headers = {'X-RateLimit-Remaining': '100'}
    mock_response.status_code = 200
    mock_get.return_value = mock_response
    
    result = unfollower.make_request("https://api.github.com/test")
    
    assert len(result) == 2
    assert result[0]["login"] == "user1"

@patch('unfollow_nonfollowers.requests.delete')
def test_unfollow_user_success(mock_delete, unfollower):
    # Mock successful unfollow
    mock_response = Mock()
    mock_response.status_code = 204
    mock_delete.return_value = mock_response
    
    result = unfollower.unfollow_user("testuser")
    
    assert result is True

@patch('unfollow_nonfollowers.requests.delete')
def test_unfollow_user_failure(mock_delete, unfollower):
    # Mock failed unfollow
    mock_response = Mock()
    mock_response.status_code = 404
    mock_delete.return_value = mock_response
    
    result = unfollower.unfollow_user("nonexistent")
    
    assert result is False
