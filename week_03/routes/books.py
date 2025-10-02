from flask import Blueprint, request, jsonify
from database import get_db_connection

books_bp = Blueprint('books', __name__)

@books_bp.route('/api/v1/books', methods=['GET'])
def get_books():
    """[F4] Lấy danh sách tất cả sách"""
    try:
        conn = get_db_connection()
        books = conn.execute('SELECT * FROM books ORDER BY id').fetchall()
        conn.close()
        
        books_list = []
        for book in books:
            books_list.append({
                'id': book['id'],
                'title': book['title'],
                'author': book['author'],
                'available_copies': book['available_copies'],
                'total_copies': book['total_copies'],
                'created_at': book['created_at']
            })
        
        return jsonify({
            'success': True,
            'data': books_list,
            'message': 'Books retrieved successfully'
        }), 200
        
    except Exception as e:
        return jsonify({
            'success': False,
            'message': f'Error retrieving books: {str(e)}'
        }), 500

@books_bp.route('/api/v1/books', methods=['POST'])
def add_book():
    """[F1] Thêm sách mới"""
    try:
        data = request.get_json()
        
        # Validate input
        if not data or not data.get('title') or not data.get('author'):
            return jsonify({
                'success': False,
                'message': 'Title and author are required'
            }), 400
        
        title = data['title']
        author = data['author']
        total_copies = data.get('total_copies', 1)
        available_copies = total_copies
        
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute('''
            INSERT INTO books (title, author, available_copies, total_copies)
            VALUES (?, ?, ?, ?)
        ''', (title, author, available_copies, total_copies))
        
        book_id = cursor.lastrowid
        conn.commit()
        conn.close()
        
        return jsonify({
            'success': True,
            'data': {
                'id': book_id,
                'title': title,
                'author': author,
                'available_copies': available_copies,
                'total_copies': total_copies
            },
            'message': 'Book added successfully'
        }), 201
        
    except Exception as e:
        return jsonify({
            'success': False,
            'message': f'Error adding book: {str(e)}'
        }), 500

@books_bp.route('/api/v1/books/<int:book_id>', methods=['GET'])
def get_book(book_id):
    """[F5] Lấy thông tin chi tiết của một sách"""
    try:
        conn = get_db_connection()
        book = conn.execute('SELECT * FROM books WHERE id = ?', (book_id,)).fetchone()
        conn.close()
        
        if book is None:
            return jsonify({
                'success': False,
                'message': 'Book not found'
            }), 404
        
        return jsonify({
            'success': True,
            'data': {
                'id': book['id'],
                'title': book['title'],
                'author': book['author'],
                'available_copies': book['available_copies'],
                'total_copies': book['total_copies'],
                'created_at': book['created_at']
            },
            'message': 'Book retrieved successfully'
        }), 200
        
    except Exception as e:
        return jsonify({
            'success': False,
            'message': f'Error retrieving book: {str(e)}'
        }), 500

@books_bp.route('/api/v1/books/<int:book_id>', methods=['PUT'])
def update_book(book_id):
    """[F2] Sửa thông tin sách"""
    try:
        data = request.get_json()
        
        if not data:
            return jsonify({
                'success': False,
                'message': 'No data provided'
            }), 400
        
        conn = get_db_connection()
        
        # Check if book exists
        book = conn.execute('SELECT * FROM books WHERE id = ?', (book_id,)).fetchone()
        if book is None:
            conn.close()
            return jsonify({
                'success': False,
                'message': 'Book not found'
            }), 404
        
        # Update fields
        title = data.get('title', book['title'])
        author = data.get('author', book['author'])
        total_copies = data.get('total_copies', book['total_copies'])
        
        # Adjust available copies if total copies changed
        if total_copies != book['total_copies']:
            borrowed_copies = book['total_copies'] - book['available_copies']
            available_copies = max(0, total_copies - borrowed_copies)
        else:
            available_copies = book['available_copies']
        
        conn.execute('''
            UPDATE books 
            SET title = ?, author = ?, available_copies = ?, total_copies = ?
            WHERE id = ?
        ''', (title, author, available_copies, total_copies, book_id))
        
        conn.commit()
        conn.close()
        
        return jsonify({
            'success': True,
            'data': {
                'id': book_id,
                'title': title,
                'author': author,
                'available_copies': available_copies,
                'total_copies': total_copies
            },
            'message': 'Book updated successfully'
        }), 200
        
    except Exception as e:
        return jsonify({
            'success': False,
            'message': f'Error updating book: {str(e)}'
        }), 500

@books_bp.route('/api/v1/books/<int:book_id>', methods=['DELETE'])
def delete_book(book_id):
    """[F3] Xóa sách"""
    try:
        conn = get_db_connection()
        
        # Check if book exists
        book = conn.execute('SELECT * FROM books WHERE id = ?', (book_id,)).fetchone()
        if book is None:
            conn.close()
            return jsonify({
                'success': False,
                'message': 'Book not found'
            }), 404
        
        # Check if book is currently borrowed
        borrowed_count = conn.execute('''
            SELECT COUNT(*) as count FROM borrows 
            WHERE book_id = ? AND status = 'borrowed'
        ''', (book_id,)).fetchone()['count']
        
        if borrowed_count > 0:
            conn.close()
            return jsonify({
                'success': False,
                'message': 'Cannot delete book that is currently borrowed'
            }), 400
        
        # Delete the book
        conn.execute('DELETE FROM books WHERE id = ?', (book_id,))
        conn.commit()
        conn.close()
        
        return jsonify({
            'success': True,
            'message': 'Book deleted successfully'
        }), 200
        
    except Exception as e:
        return jsonify({
            'success': False,
            'message': f'Error deleting book: {str(e)}'
        }), 500