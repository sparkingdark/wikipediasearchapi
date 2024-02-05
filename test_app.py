import logging
from fastapi.testclient import TestClient
from app import app

# Set up logging
logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)

client = TestClient(app)

def test_analyze_word_frequency():
    # Test valid request
    payload = {"topic": "Natural Language Processing", "n": 5}
    response = client.post("/wordfrequencyanalysis", json=payload)
    result = response.json()
    
    logger.debug(f"Response: {response.text}")
    
    assert response.status_code == 200
    assert "topic" in result
    assert "id" in result
    assert "top_words" in result

    # Test invalid request (missing 'n')
    payload = {"topic": "Invalid Topic"}
    response = client.post("/wordfrequencyanalysis", json=payload)
    
    logger.debug(f"Response: {response.text}")
    
    assert response.status_code == 422  # Unprocessable Entity

def test_search_history():
    # Test search history endpoint
    response = client.get("/searchhistory")
    history = response.json()

    logger.debug(f"Response: {response.text}")

    assert response.status_code == 200
    assert isinstance(history, list)
