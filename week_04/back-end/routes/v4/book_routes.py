from flask import Blueprint, jsonify, request, make_response
from ...database import get_db_connection
import hashlib

book_bp_v4 = Blueprint('book_bp_v4', __name__)

# Get all books
@book_bp_v4.route('/books', methods=['GET'])
def get_books():
    conn = get_db_connection()
    books = conn.execute('SELECT * FROM books').fetchall()
    conn.close()
    json_content = jsonify([dict(book) for book in books])
    etag = hashlib.md5(json_content.data).hexdigest()

    if 'If-None-Match' in request.headers and request.headers['If-None-Match'] == etag:
        return '', 304

    response = make_response(json_content)
    response.headers['Cache-Control'] = 'max-age=60'
    response.headers['ETag'] = etag
    return response

# # Get a single book by ID
# @book_bp_v4.route('/books/<int:book_id>', methods=['GET'])
# def get_book(book_id):
#     conn = get_db_connection()
#     book = conn.execute('SELECT * FROM books WHERE id = ?', (book_id,)).fetchone()
#     conn.close()
#     if book:
#         return jsonify(dict(book))
#     return jsonify({'message': 'Book not found'}), 404

# # Create a new book
# @book_bp_v4.route('/books', methods=['POST'])
# def create_book():
#     new_book = request.get_json()
#     title = new_book['title']
#     author = new_book['author']
#     year = new_book['year']
#     conn = get_db_connection()
#     cursor = conn.cursor()
#     cursor.execute('INSERT INTO books (title, author, year) VALUES (?, ?, ?)', (title, author, year))
#     conn.commit()
#     conn.close()
#     return jsonify({'message': 'Book created successfully', 'id': cursor.lastrowid}), 201

# # Update an existing book
# @book_bp_v4.route('/books/<int:book_id>', methods=['PUT'])
# def update_book(book_id):
#     updated_book = request.get_json()
#     title = updated_book['title']
#     author = updated_book['author']
#     year = updated_book['year']
#     conn = get_db_connection()
#     cursor = conn.cursor()
#     cursor.execute('UPDATE books SET title = ?, author = ?, year = ? WHERE id = ?', (title, author, year, book_id))
#     conn.commit()
#     conn.close()
#     if cursor.rowcount == 0:
#         return jsonify({'message': 'Book not found'}), 404
#     return jsonify({'message': 'Book updated successfully'}), 200

# # Delete a book
# @book_bp_v4.route('/books/<int:book_id>', methods=['DELETE'])
# def delete_book(book_id):
#     conn = get_db_connection()
#     cursor = conn.cursor()
#     cursor.execute('DELETE FROM books WHERE id = ?', (book_id,))
#     conn.commit()
#     conn.close()
#     if cursor.rowcount == 0:
#         return jsonify({'message': 'Book not found'}), 404
#     return jsonify({'message': 'Book deleted successfully'}), 200