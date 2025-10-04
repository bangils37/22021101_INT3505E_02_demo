from flask import Blueprint, jsonify, session
from ...database import get_db_connection

book_bp = Blueprint('book_bp', __name__)

@book_bp.route('/getbooks', methods=['GET'])
def get_books():
    if 'visits' in session:
        session['visits'] = session.get('visits') + 1
    else:
        session['visits'] = 1
    print(f"Số lượt truy cập: {session['visits']}")
    conn = get_db_connection()
    books = conn.execute('SELECT * FROM books').fetchall()
    conn.close()
    return jsonify([dict(book) for book in books])