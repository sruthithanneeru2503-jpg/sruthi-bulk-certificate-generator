from fastapi.testclient import TestClient

from app.main import app


client = TestClient(app)


def test_create_job():
    response = client.post(
        "/jobs",
        json={
            "event_name": "Test Workshop",
            "event_date": "2026-10-06",
            "recipients": [
                {
                    "name": "Test User",
                    "email": "test@gmail.com"
                }
            ]
        }
    )

    assert response.status_code == 200
    data = response.json()

    assert data["total"] == 1
    assert data["successful"] == 1
    assert data["failed"] == 0


def test_invalid_email():
    response = client.post(
        "/jobs",
        json={
            "event_name": "Test Workshop",
            "event_date": "2026-10-06",
            "recipients": [
                {
                    "name": "Test User",
                    "email": "wrong-email"
                }
            ]
        }
    )

    assert response.status_code == 422


def test_get_job():
    response = client.post(
        "/jobs",
        json={
            "event_name": "Test Workshop",
            "event_date": "2026-10-06",
            "recipients": [
                {
                    "name": "Test User",
                    "email": "test2@gmail.com"
                }
            ]
        }
    )

    job_id = response.json()["job_id"]

    response = client.get(f"/jobs/{job_id}")

    assert response.status_code == 200
    assert response.json()["job_id"] == job_id


def test_get_certificate():
    response = client.post(
        "/jobs",
        json={
            "event_name": "Test Workshop",
            "event_date": "2026-10-06",
            "recipients": [
                {
                    "name": "Certificate User",
                    "email": "certificate@gmail.com"
                }
            ]
        }
    )

    assert response.status_code == 200
    
    
def test_individual_failure_does_not_stop_job(monkeypatch):
    from app import main

    original_generate = main.generate_certificate

    def fake_generate(name, event_name, event_date, certificate_id):
        if name == "Fail User":
            raise Exception("Test certificate failure")
        return original_generate(
            name,
            event_name,
            event_date,
            certificate_id
        )

    monkeypatch.setattr(
        main,
        "generate_certificate",
        fake_generate
    )

    response = client.post(
        "/jobs",
        json={
            "event_name": "Failure Test",
            "event_date": "2026-10-07",
            "recipients": [
                {
                    "name": "Fail User",
                    "email": "fail@gmail.com"
                },
                {
                    "name": "Success User",
                    "email": "success@gmail.com"
                }
            ]
        }
    )

    assert response.status_code == 200

    data = response.json()

    assert data["total"] == 2
    assert data["successful"] == 1
    assert data["failed"] == 1