from flask import Blueprint, jsonify, session
from ...database import get_db_connection

borrow_bp = Blueprint('borrow_bp', __name__)

@borrow_bp.route('/getborrows', methods=['GET'])
def get_borrows():
    if 'visits' in session:
        session['visits'] = session.get('visits') + 1
    else:
        session['visits'] = 1
    print(f"Số lượt truy cập: {session['visits']}")
    conn = get_db_connection()
    borrows = conn.execute('SELECT * FROM borrows').fetchall()
    conn.close()
    return jsonify([dict(borrow) for borrow in borrows])