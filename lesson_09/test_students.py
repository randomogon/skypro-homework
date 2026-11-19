import os
from pathlib import Path
from uuid import uuid4

import pytest
from dotenv import load_dotenv
from sqlalchemy import create_engine, text
from sqlalchemy.engine import URL


@pytest.fixture
def database():
    load_dotenv(Path(__file__).with_name(".env"))

    password = os.getenv("DB_PASSWORD")
    assert password, "Укажи DB_PASSWORD в lesson_09/.env"

    url = URL.create(
        drivername="postgresql+psycopg2",
        username=os.getenv("DB_USER", "postgres"),
        password=password,
        host=os.getenv("DB_HOST", "localhost"),
        port=int(os.getenv("DB_PORT", "5432")),
        database=os.getenv("DB_NAME", "skypro_lesson9"),
    )
    engine = create_engine(url)
    created_ids = []

    try:
        yield engine, created_ids
    finally:
        try:
            with engine.begin() as connection:
                for student_id in created_ids:
                    connection.execute(
                        text("DELETE FROM students WHERE id = :id"),
                        {"id": student_id},
                    )
        finally:
            engine.dispose()


def create_student(engine, created_ids):
    first_name = f"Student_{uuid4().hex[:12]}"
    last_name = "Test"

    with engine.begin() as connection:
        student_id = connection.execute(
            text(
                "INSERT INTO students (first_name, last_name) "
                "VALUES (:first_name, :last_name) RETURNING id"
            ),
            {"first_name": first_name, "last_name": last_name},
        ).scalar_one()

    created_ids.append(student_id)
    return student_id, first_name, last_name


def test_add_student(database):
    engine, created_ids = database
    student_id, first_name, last_name = create_student(
        engine, created_ids
    )

    with engine.connect() as connection:
        student = connection.execute(
            text(
                "SELECT first_name, last_name FROM students "
                "WHERE id = :id"
            ),
            {"id": student_id},
        ).mappings().one()

    assert student["first_name"] == first_name
    assert student["last_name"] == last_name


def test_update_student(database):
    engine, created_ids = database
    student_id, _, _ = create_student(engine, created_ids)
    updated_name = f"Updated_{uuid4().hex[:12]}"

    with engine.begin() as connection:
        result = connection.execute(
            text(
                "UPDATE students SET first_name = :first_name "
                "WHERE id = :id"
            ),
            {"first_name": updated_name, "id": student_id},
        )
        assert result.rowcount == 1

    with engine.connect() as connection:
        actual_name = connection.execute(
            text("SELECT first_name FROM students WHERE id = :id"),
            {"id": student_id},
        ).scalar_one()

    assert actual_name == updated_name


def test_delete_student(database):
    engine, created_ids = database
    student_id, _, _ = create_student(engine, created_ids)

    with engine.begin() as connection:
        result = connection.execute(
            text("DELETE FROM students WHERE id = :id"),
            {"id": student_id},
        )
        assert result.rowcount == 1

    with engine.connect() as connection:
        remaining_id = connection.execute(
            text("SELECT id FROM students WHERE id = :id"),
            {"id": student_id},
        ).scalar_one_or_none()

    assert remaining_id is None
