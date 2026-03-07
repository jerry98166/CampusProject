"""
Test API Module
API 端點測試
"""
import sys
from pathlib import Path

# 添加 src 目錄到 Python 路徑
sys.path.insert(0, str(Path(__file__).parent.parent / 'src'))

import pytest
from app import app


@pytest.fixture
def client():
    """建立測試客戶端"""
    app.config['TESTING'] = True
    with app.test_client() as client:
        yield client


def test_health_check(client):
    """測試健康檢查端點"""
    response = client.get('/health')
    assert response.status_code == 200
    data = response.get_json()
    assert data['status'] == 'healthy'
    assert 'service' in data


def test_index(client):
    """測試首頁"""
    response = client.get('/')
    assert response.status_code == 200


def test_ask_question_success(client):
    """測試成功的問答請求"""
    response = client.post(
        '/api/chat/ask',
        json={'question': '中原大學的學則是什麼？'}
    )
    assert response.status_code == 200
    data = response.get_json()
    assert data['status'] == 'success'
    assert 'response' in data


def test_ask_question_empty(client):
    """測試空問題"""
    response = client.post(
        '/api/chat/ask',
        json={'question': ''}
    )
    assert response.status_code == 400
    data = response.get_json()
    assert data['status'] == 'error'


def test_ask_question_too_long(client):
    """測試過長的問題"""
    long_question = 'x' * 1001
    response = client.post(
        '/api/chat/ask',
        json={'question': long_question}
    )
    assert response.status_code == 400


def test_ask_question_no_json(client):
    """測試沒有 JSON 內容的請求"""
    response = client.post('/api/chat/ask')
    assert response.status_code == 400


def test_reset_conversation(client):
    """測試重置對話"""
    response = client.post('/api/chat/reset')
    assert response.status_code == 200
    data = response.get_json()
    assert data['status'] == 'success'


def test_get_chat_history(client):
    """測試獲取對話歷史"""
    response = client.get('/api/chat/history')
    assert response.status_code == 200
    data = response.get_json()
    assert 'history' in data
    assert isinstance(data['history'], list)


def test_404_error(client):
    """測試 404 錯誤"""
    response = client.get('/nonexistent')
    assert response.status_code == 404
    data = response.get_json()
    assert 'error' in data
