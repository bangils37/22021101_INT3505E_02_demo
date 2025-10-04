from flask import Blueprint, jsonify, make_response, request
from ...database import get_db_connection
import hashlib

borrow_bp_v3 = Blueprint('borrow_bp_v3', __name__)

@borrow_bp_v3.route('/getborrows', methods=['GET'])
def get_borrows():
    conn = get_db_connection()
    borrows = conn.execute('SELECT * FROM borrows').fetchall()
    conn.close()

    # Generate ETag from content
    json_content = jsonify([dict(borrow) for borrow in borrows])
    etag = hashlib.md5(json_content.data).hexdigest()

    # Check If-None-Match header
    if 'If-None-Match' in request.headers and request.headers['If-None-Match'] == etag:
        return '', 304  # Not Modified

    response = make_response(json_content)
    response.headers['Cache-Control'] = 'max-age=60'
    response.headers['ETag'] = etag
    return response