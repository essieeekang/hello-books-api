import pytest
from app.models.book import Book


def test_get_all_books_with_no_records(client):
    # Act
    response = client.get("/books")
    response_body = response.get_json()

    # Assert
    assert response.status_code == 200
    assert response_body == []


def test_get_one_book(client, two_saved_books):
    # Act
    response = client.get("/books/1")
    response_body = response.get_json()

    # Assert
    assert response.status_code == 200
    assert response_body == {
        "id": 1,
        "title": "Ocean Book",
        "description": "watr 4evr"
    }


def test_create_one_book(client):
    # Act
    response = client.post("/books", json={
        "title": "New Book",
        "description": "The Best!"
    })
    response_body = response.get_json()

    # Assert
    assert response.status_code == 201
    assert response_body == {
        "id": 1,
        "title": "New Book",
        "description": "The Best!"
    }


def test_create_one_book_no_title(client):
    # Arrange
    test_data = {"description": "The Best!"}

    # Act
    response = client.post("/books", json=test_data)
    response_body = response.get_json()

    # Assert
    assert response.status_code == 400
    assert response_body == {'message': 'Invalid request: missing title'}


def test_create_one_book_no_description(client):
    # Arrange
    test_data = {"title": "New Book"}

    # Act
    response = client.post("/books", json=test_data)
    response_body = response.get_json()

    # Assert
    assert response.status_code == 400
    assert response_body == {'message': 'Invalid request: missing description'}


def test_create_one_book_with_extra_keys(client):
    # Arrange
    test_data = {
        "extra": "some stuff",
        "title": "New Book",
        "description": "The Best!",
        "another": "last value"
    }

    # Act
    response = client.post("/books", json=test_data)
    response_body = response.get_json()

    # Assert
    assert response.status_code == 201
    assert response_body == {
        "id": 1,
        "title": "New Book",
        "description": "The Best!"
    }


def test_from_dict_returns_book():
    # Arrange
    book_data = {
        "title": "New Book",
        "description": "The Best!"
    }

    # Act
    new_book = Book.from_dict(book_data)

    # Assert
    assert new_book.title == "New Book"
    assert new_book.description == "The Best!"


def test_from_dict_with_no_title():
    # Arrange
    book_data = {
        "description": "The Best!"
    }

    # Act & Assert
    with pytest.raises(KeyError, match='title'):
        new_book = Book.from_dict(book_data)


def test_from_dict_with_no_description():
    # Arrange
    book_data = {
        "title": "New Book"
    }

    # Act & Assert
    with pytest.raises(KeyError, match='description'):
        new_book = Book.from_dict(book_data)


def test_from_dict_with_extra_keys():
    # Arrange
    book_data = {
        "extra": "some stuff",
        "title": "New Book",
        "description": "The Best!",
        "another": "last value"
    }

    # Act
    new_book = Book.from_dict(book_data)

    # Assert
    assert new_book.title == "New Book"
    assert new_book.description == "The Best!"
