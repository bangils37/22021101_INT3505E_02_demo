from flask import Blueprint, jsonify, make_response, request
from ...database import get_db_connection
import hashlib

book_bp_v3 = Blueprint('book_bp_v3', __name__)

@book_bp_v3.route('/getbooks', methods=['GET'])
def get_books():
    conn = get_db_connection()
    books = conn.execute('SELECT * FROM books').fetchall()
    conn.close()

    # Generate ETag from content
    json_content = jsonify([dict(book) for book in books])
    etag = hashlib.md5(json_content.data).hexdigest()

    # Check If-None-Match header
    if 'If-None-Match' in request.headers and request.headers['If-None-Match'] == etag:
        return '', 304  # Not Modified

    response = make_response(json_content)
    response.headers['Cache-Control'] = 'max-age=60'
    response.headers['ETag'] = etag
    return response