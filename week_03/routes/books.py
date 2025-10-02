from flask import Blueprint, request, jsonify
from database import get_db_connection

books_bp = Blueprint('books', __name__)

@books_bp.route('/api/v1/books', methods=['GET'])
def get_books():
    """[F4] Lấy danh sách sách với pagination, filtering và sorting"""
    try:
        # Get query parameters
        page = request.args.get('page', 1, type=int)
        limit = request.args.get('limit', 10, type=int)
        offset = request.args.get('offset', type=int)
        
        # Filtering parameters
        author = request.args.get('author')
        title = request.args.get('title')
        status = request.args.get('status')  # available, unavailable
        
        # Sorting parameters
        sort = request.args.get('sort', 'id')  # Default sort by id
        order = request.args.get('order', 'asc')  # asc or desc
        
        # Validate parameters
        if limit > 100:
            limit = 100  # Max limit
        if limit < 1:
            limit = 10
        if page < 1:
            page = 1
        if order not in ['asc', 'desc']:
            order = 'asc'
        if sort not in ['id', 'title', 'author', 'available_copies', 'total_copies', 'created_at']:
            sort = 'id'
        
        # Calculate offset if not provided
        if offset is None:
            offset = (page - 1) * limit
        
        conn = get_db_connection()
        
        # Build WHERE clause for filtering
        where_conditions = []
        params = []
        
        if author:
            where_conditions.append("author LIKE ?")
            params.append(f"%{author}%")
        
        if title:
            where_conditions.append("title LIKE ?")
            params.append(f"%{title}%")
            
        if status:
            if status == 'available':
                where_conditions.append("available_copies > 0")
            elif status == 'unavailable':
                where_conditions.append("available_copies = 0")
        
        where_clause = ""
        if where_conditions:
            where_clause = "WHERE " + " AND ".join(where_conditions)
        
        # Build ORDER BY clause
        order_clause = f"ORDER BY {sort} {order.upper()}"
        
        # Get total count for pagination
        count_query = f"SELECT COUNT(*) as total FROM books {where_clause}"
        total_books = conn.execute(count_query, params).fetchone()['total']
        
        # Get books with pagination
        books_query = f"""
            SELECT * FROM books 
            {where_clause} 
            {order_clause} 
            LIMIT ? OFFSET ?
        """
        params.extend([limit, offset])
        books = conn.execute(books_query, params).fetchall()
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
        
        # Calculate pagination info
        total_pages = (total_books + limit - 1) // limit  # Ceiling division
        has_next = page < total_pages
        has_prev = page > 1
        
        return jsonify({
            'success': True,
            'data': books_list,
            'pagination': {
                'page': page,
                'limit': limit,
                'offset': offset,
                'total_items': total_books,
                'total_pages': total_pages,
                'has_next': has_next,
                'has_prev': has_prev
            },
            'filters': {
                'author': author,
                'title': title,
                'status': status
            },
            'sorting': {
                'sort': sort,
                'order': order
            },
            'message': f'Found {len(books_list)} books (page {page} of {total_pages})'
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