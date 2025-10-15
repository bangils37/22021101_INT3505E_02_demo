from flask import Blueprint, jsonify, request
from ...database import get_db_connection

book_bp_v1 = Blueprint('book_bp_v1', __name__)

@book_bp_v1.route('/books', methods=['GET'])
def get_books():
    conn = get_db_connection()
    cursor = conn.cursor()

    page = request.args.get('page', 1, type=int)
    page_size = request.args.get('page_size', 10, type=int)
    offset = (page - 1) * page_size

    title = request.args.get('title')
    author = request.args.get('author')

    query = "SELECT id, title, author FROM books"
    params = []

    if title:
        query += " WHERE title LIKE ?"
        params.append(f'%{title}%')
    elif author:
        query += " WHERE author LIKE ?"
        params.append(f'%{author}%')

    query += " LIMIT ? OFFSET ?"
    params.append(page_size)
    params.append(offset)

    print(f"Executing query: {query} with params: {params}")
    cursor.execute(query, tuple(params))
    books = cursor.fetchall()
    print(f"Fetched books: {books}")
    conn.close()

    return jsonify({
        'success': True,
        'data': [dict(row) for row in books],
        'page': page,
        'page_size': page_size
    })