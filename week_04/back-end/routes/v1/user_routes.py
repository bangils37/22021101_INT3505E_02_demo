from flask import Blueprint, jsonify, request
from ...database import get_db_connection

user_bp_v1 = Blueprint('user_bp_v1', __name__)

@user_bp_v1.route('/users/<int:user_id>/borrows', methods=['GET'])
def get_user_borrows(user_id):
    conn = get_db_connection()
    cursor = conn.cursor()

    page = request.args.get('page', 1, type=int)
    page_size = request.args.get('page_size', 10, type=int)
    offset = (page - 1) * page_size

    cursor.execute(
        '''SELECT borrows.id, books.title, books.author, borrows.borrow_date, borrows.return_date
           FROM borrows
           JOIN books ON borrows.book_id = books.id
           WHERE borrows.user_id = ?
           LIMIT ? OFFSET ?''',
        (user_id, page_size, offset)
    )
    borrows = cursor.fetchall()
    conn.close()

    return jsonify({
        'success': True,
        'data': [dict(row) for row in borrows],
        'page': page,
        'page_size': page_size
    })