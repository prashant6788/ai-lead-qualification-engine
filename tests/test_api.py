from fastapi.testclient import TestClient

from app.main import app


client = TestClient(app)


def test_health_endpoint():
    response = client.get("/health")

    assert response.status_code == 200
    assert response.json() == {"status": "ok"}


def test_qualify_endpoint():
    payload = {
        "name": "Rahul Sharma",
        "company": "Northstar Realty",
        "email": "rahul@example.com",
        "phone": "+919999999999",
        "message": "We generate around 100 enquiries a month and need CRM automation and WhatsApp follow-up.",
        "service_interest": "crm_automation",
        "location": "Gurugram",
        "budget": 50000,
        "timeline": "30 days",
        "lead_source": "google_ads"
    }

    response = client.post("/qualify", json=payload)

    assert response.status_code == 200

    result = response.json()

    assert result["qualification_status"] == "qualified"
    assert result["score"] == 100
    assert result["service_interest"] == "crm_automation"
    assert result["needs_human_review"] is False
    assert result["recommended_action"] == "book_sales_call"


def test_invalid_lead_returns_422():
    payload = {
        "company": "Missing Name Ltd"
    }

    response = client.post("/qualify", json=payload)

    assert response.status_code == 422


def test_commercial_request_requires_human_review():
    payload = {
        "name": "Anita Mehta",
        "company": "Example Consulting",
        "message": "We need CRM automation. Can you offer a discount for a long contract?",
        "service_interest": "crm_automation",
        "location": "Delhi",
        "budget": 60000,
        "timeline": "1 month"
    }

    response = client.post("/qualify", json=payload)

    assert response.status_code == 200

    result = response.json()

    assert result["qualification_status"] == "review"
    assert result["needs_human_review"] is True
    assert result["recommended_action"] == "human_review"
