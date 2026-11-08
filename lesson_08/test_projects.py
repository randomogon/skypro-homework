import os
import uuid
from pathlib import Path
from uuid import uuid4

import requests
from dotenv import load_dotenv


load_dotenv(Path(__file__).parent / ".env")

BASE_URL = "https://ru.yougile.com/api-v2/projects"


def test_create_project_positive():
    api_key = os.environ["YOUGILE_API_KEY"]

    headers = {
        "Authorization": f"Bearer {api_key}",
        "Content-Type": "application/json",
    }

    project_title = f"SkyPro Test {uuid4()}"

    response = requests.post(
        BASE_URL,
        headers=headers,
        json={"title": project_title},
        timeout=20,
    )

    assert response.status_code == 201, response.text

    project_id = response.json().get("id")
    assert project_id, "Сервер не вернул ID проекта"

    try:
        get_response = requests.get(
            f"{BASE_URL}/{project_id}",
            headers=headers,
            timeout=20,
        )

        assert get_response.status_code == 200
        assert get_response.json()["title"] == project_title

    finally:
        cleanup = requests.put(
            f"{BASE_URL}/{project_id}",
            headers=headers,
            json={"deleted": True},
            timeout=20,
        )

        assert cleanup.status_code == 200, cleanup.text


def test_create_project_negative():
    api_key = os.environ["YOUGILE_API_KEY"]

    headers = {
        "Authorization": f"Bearer {api_key}",
        "Content-Type": "application/json",
    }

    response = requests.post(
        BASE_URL,
        headers=headers,
        json={},
        timeout=20,
    )

    assert response.status_code == 400, response.text

    data = response.json()

    assert data["error"] == "Bad Request"
    assert "title should not be empty" in data["message"]
    assert "title must be a string" in data["message"]


def test_update_project_positive():
    api_key = os.environ["YOUGILE_API_KEY"]

    headers = {
        "Authorization": f"Bearer {api_key}",
        "Content-Type": "application/json",
    }

    original_title = f"Original Project {uuid4()}"
    updated_title = f"Updated Project {uuid4()}"

    create_response = requests.post(
        BASE_URL,
        headers=headers,
        json={"title": original_title},
        timeout=20,
    )

    assert create_response.status_code == 201, create_response.text

    project_id = create_response.json()["id"]

    try:
        update_response = requests.put(
            f"{BASE_URL}/{project_id}",
            headers=headers,
            json={"title": updated_title},
            timeout=20,
        )

        assert update_response.status_code == 200, (
            update_response.text
        )

        get_response = requests.get(
            f"{BASE_URL}/{project_id}",
            headers=headers,
            timeout=20,
        )

        assert get_response.status_code == 200, get_response.text

        assert get_response.json()["title"] == updated_title, (
            "Название проекта не обновилось"
        )

    finally:
        cleanup = requests.put(
            f"{BASE_URL}/{project_id}",
            headers=headers,
            json={"deleted": True},
            timeout=20,
        )

        assert cleanup.status_code == 200, cleanup.text


def test_update_project_negative():
    api_key = os.environ["YOUGILE_API_KEY"]

    headers = {
        "Authorization": f"Bearer {api_key}",
        "Content-Type": "application/json",
    }

    project_id = str(uuid4())

    response = requests.put(
        f"{BASE_URL}/{project_id}",
        headers=headers,
        json={"title": "Test update"},
        timeout=20,
    )

    assert response.status_code == 404, response.text

    data = response.json()

    assert data["statusCode"] == 404
    assert data["error"] == "Not Found"
    assert data["message"] == "Проект не найден"


def test_get_project_positive():
    api_key = os.environ["YOUGILE_API_KEY"]

    headers = {
        "Authorization": f"Bearer {api_key}",
        "Content-Type": "application/json",
    }

    project_title = f"Get Test Project {uuid4()}"

    create_response = requests.post(
        BASE_URL,
        headers=headers,
        json={"title": project_title},
        timeout=20,
    )

    assert create_response.status_code == 201, (
        create_response.text
    )

    project_id = create_response.json()["id"]

    try:
        response = requests.get(
            f"{BASE_URL}/{project_id}",
            headers=headers,
            timeout=20,
        )

        assert response.status_code == 200, response.text

        data = response.json()

        assert data["title"] == project_title, (
            "Название полученного проекта не совпадает"
        )

    finally:
        cleanup = requests.put(
            f"{BASE_URL}/{project_id}",
            headers=headers,
            json={"deleted": True},
            timeout=20,
        )

        assert cleanup.status_code == 200, cleanup.text


def test_get_project_negative():
    load_dotenv("lesson_08/.env")

    api_key = os.getenv("YOUGILE_API_KEY")
    assert api_key, "Не найден API-ключ YouGile"

    project_id = str(uuid.uuid4())

    response = requests.get(
        f"https://ru.yougile.com/api-v2/projects/{project_id}",
        headers={
            "Authorization": f"Bearer {api_key}"
        },
        timeout=20,
    )

    assert response.status_code == 404, response.text

    data = response.json()

    assert data["statusCode"] == 404
    assert data["error"] == "Not Found"
    assert data["message"] == "Проект не найден"
