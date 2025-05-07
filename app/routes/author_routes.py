from flask import Blueprint, request, Response
from app.models.author import Author
from .route_utilities import validate_model, create_model, get_models_with_filters
from ..db import db

bp = Blueprint("authors_bp", __name__, url_prefix="/authors")


@bp.post("")
def create_author():
    request_body = request.get_json()
    return create_model(Author, request_body)


@bp.post("/<author_id>/books")
def create_book_with_author(author_id):
    author = validate_model(Author, author_id)

    request_body = request.get_json()
    request_body["author_id"] = author.id

    return create_model(Author, request_body)


@bp.get("")
def get_all_authors():
    return get_models_with_filters(Author, request.args)


@bp.get("/<author_id>/books")
def get_all_books_by_author(author_id):
    author = validate_model(Author, author_id)
    response = [book.to_dict() for book in author.books]

    return response


@bp.get("/<author_id>")
def get_one_author(author_id):
    author = validate_model(Author, author_id)

    return author.to_dict()


@bp.put("/<author_id>")
def update_author(author_id):
    author = validate_model(Author, author_id)
    request_body = request.get_json()

    author.name = request_body["name"]
    db.session.commit()

    return Response(status=204, mimetype="application/json")


@bp.delete("/<author_id>")
def delete_author(author_id):
    book = validate_model(Author, author_id)
    db.session.delete(book)
    db.session.commit()

    return Response(status=204, mimetype="application/json")
