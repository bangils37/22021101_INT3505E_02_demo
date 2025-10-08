from flask import Blueprint, jsonify, request, make_response
from ...database import get_db_connection
import hashlib

borrow_bp_v4 = Blueprint('borrow_bp_v4', __name__)

# Get all borrows
@borrow_bp_v4.route('/borrows', methods=['GET'])
def get_borrows():
    conn = get_db_connection()
    borrows = conn.execute('SELECT * FROM borrows').fetchall()
    conn.close()
    json_content = jsonify([dict(borrow) for borrow in borrows])
    etag = hashlib.md5(json_content.data).hexdigest()

    if 'If-None-Match' in request.headers and request.headers['If-None-Match'] == etag:
        return '', 304

    response = make_response(json_content)
    response.headers['Cache-Control'] = 'max-age=60'
    response.headers['ETag'] = etag
    return response

# Get a single borrow by ID
@borrow_bp_v4.route('/borrows/<int:borrow_id>', methods=['GET'])
def get_borrow(borrow_id):
    conn = get_db_connection()
    borrow = conn.execute('SELECT * FROM borrows WHERE id = ?', (borrow_id,)).fetchone()
    conn.close()
    if borrow:
        return jsonify(dict(borrow))
    return jsonify({'message': 'Borrow not found'}), 404

# Create a new borrow
@borrow_bp_v4.route('/borrows', methods=['POST'])
def create_borrow():
    new_borrow = request.get_json()
    book_id = new_borrow['book_id']
    borrower_name = new_borrow['borrower_name']
    borrow_date = new_borrow['borrow_date']
    return_date = new_borrow['return_date']
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute('INSERT INTO borrows (book_id, borrower_name, borrow_date, return_date) VALUES (?, ?, ?, ?)', (book_id, borrower_name, borrow_date, return_date))
    conn.commit()
    conn.close()
    return jsonify({'message': 'Borrow created successfully', 'id': cursor.lastrowid}), 201

# Update an existing borrow
@borrow_bp_v4.route('/borrows/<int:borrow_id>', methods=['PUT'])
def update_borrow(borrow_id):
    updated_borrow = request.get_json()
    book_id = updated_borrow['book_id']
    borrower_name = updated_borrow['borrower_name']
    borrow_date = updated_borrow['borrow_date']
    return_date = updated_borrow['return_date']
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute('UPDATE borrows SET book_id = ?, borrower_name = ?, borrow_date = ?, return_date = ? WHERE id = ?', (book_id, borrower_name, borrow_date, return_date, borrow_id))
    conn.commit()
    conn.close()
    if cursor.rowcount == 0:
        return jsonify({'message': 'Borrow not found'}), 404
    return jsonify({'message': 'Borrow updated successfully'}), 200

# Delete a borrow
@borrow_bp_v4.route('/borrows/<int:borrow_id>', methods=['DELETE'])
def delete_borrow(borrow_id):
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute('DELETE FROM borrows WHERE id = ?', (borrow_id,))
    conn.commit()
    conn.close()
    if cursor.rowcount == 0:
        return jsonify({'message': 'Borrow not found'}), 404
    return jsonify({'message': 'Borrow deleted successfully'}), 200