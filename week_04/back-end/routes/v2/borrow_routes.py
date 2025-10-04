from flask import Blueprint, jsonify
from ...database import get_db_connection

borrow_bp_v2 = Blueprint('borrow_bp_v2', __name__)

@borrow_bp_v2.route('/getborrows', methods=['GET'])
def get_borrows():
    conn = get_db_connection()
    borrows = conn.execute('SELECT * FROM borrows').fetchall()
    conn.close()
    return jsonify([dict(borrow) for borrow in borrows])