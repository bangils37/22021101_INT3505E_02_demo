from flask import Blueprint, jsonify
from ...database import get_db_connection

book_bp_v2 = Blueprint('book_bp_v2', __name__)

@book_bp_v2.route('/getbooks', methods=['GET'])
def get_books():
    conn = get_db_connection()
    books = conn.execute('SELECT * FROM books').fetchall()
    conn.close()
    return jsonify([dict(book) for book in books])