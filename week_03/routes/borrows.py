from flask import Blueprint, request, jsonify
from datetime import datetime
from database import get_db_connection

borrows_bp = Blueprint('borrows', __name__)

@borrows_bp.route('/api/v1/borrows', methods=['POST'])
def borrow_book():
    """[F6] Mượn sách (giảm số lượng available)"""
    try:
        data = request.get_json()
        
        if not data or not data.get('user_id') or not data.get('book_id'):
            return jsonify({
                'success': False,
                'message': 'user_id and book_id are required'
            }), 400
        
        user_id = data['user_id']
        book_id = data['book_id']
        
        conn = get_db_connection()
        
        # Check if book exists and is available
        book = conn.execute('SELECT * FROM books WHERE id = ?', (book_id,)).fetchone()
        if book is None:
            conn.close()
            return jsonify({
                'success': False,
                'message': 'Book not found'
            }), 404
        
        if book['available_copies'] <= 0:
            conn.close()
            return jsonify({
                'success': False,
                'message': 'No available copies of this book'
            }), 400
        
        # Create borrow record
        cursor = conn.cursor()
        cursor.execute('''
            INSERT INTO borrows (user_id, book_id, borrow_date, status)
            VALUES (?, ?, ?, 'borrowed')
        ''', (user_id, book_id, datetime.now().isoformat()))
        
        borrow_id = cursor.lastrowid
        
        # Update available copies
        conn.execute('''
            UPDATE books SET available_copies = available_copies - 1
            WHERE id = ?
        ''', (book_id,))
        
        conn.commit()
        conn.close()
        
        return jsonify({
            'success': True,
            'data': {
                'borrow_id': borrow_id,
                'user_id': user_id,
                'book_id': book_id,
                'borrow_date': datetime.now().isoformat(),
                'status': 'borrowed'
            },
            'message': 'Book borrowed successfully'
        }), 201
        
    except Exception as e:
        return jsonify({
            'success': False,
            'message': f'Error borrowing book: {str(e)}'
        }), 500

@borrows_bp.route('/api/v1/borrows/<int:borrow_id>/return', methods=['PUT'])
def return_book(borrow_id):
    """[F7] Trả sách (tăng số lượng available)"""
    try:
        conn = get_db_connection()
        
        # Check if borrow record exists and is active
        borrow = conn.execute('''
            SELECT * FROM borrows WHERE id = ? AND status = 'borrowed'
        ''', (borrow_id,)).fetchone()
        
        if borrow is None:
            conn.close()
            return jsonify({
                'success': False,
                'message': 'Borrow record not found or already returned'
            }), 404
        
        # Update borrow record
        return_date = datetime.now().isoformat()
        conn.execute('''
            UPDATE borrows 
            SET return_date = ?, status = 'returned'
            WHERE id = ?
        ''', (return_date, borrow_id))
        
        # Update available copies
        conn.execute('''
            UPDATE books SET available_copies = available_copies + 1
            WHERE id = ?
        ''', (borrow['book_id'],))
        
        conn.commit()
        conn.close()
        
        return jsonify({
            'success': True,
            'data': {
                'borrow_id': borrow_id,
                'user_id': borrow['user_id'],
                'book_id': borrow['book_id'],
                'borrow_date': borrow['borrow_date'],
                'return_date': return_date,
                'status': 'returned'
            },
            'message': 'Book returned successfully'
        }), 200
        
    except Exception as e:
        return jsonify({
            'success': False,
            'message': f'Error returning book: {str(e)}'
        }), 500

@borrows_bp.route('/api/v1/borrows', methods=['GET'])
def get_borrows():
    """[F8] Lấy danh sách các bản ghi mượn với pagination, filtering và sorting"""
    try:
        # Get query parameters for pagination
        page = request.args.get('page', 1, type=int)
        limit = request.args.get('limit', 10, type=int)
        offset = request.args.get('offset', type=int)
        
        # Get query parameters for filtering
        user_id = request.args.get('user_id')
        status = request.args.get('status')
        book_id = request.args.get('book_id')
        
        # Sorting parameters
        sort = request.args.get('sort', 'borrow_date')  # Default sort by borrow_date
        order = request.args.get('order', 'desc')  # desc or asc
        
        # Validate parameters
        if limit > 100:
            limit = 100  # Max limit
        if limit < 1:
            limit = 10
        if page < 1:
            page = 1
        if order not in ['asc', 'desc']:
            order = 'desc'
        if sort not in ['id', 'user_id', 'book_id', 'borrow_date', 'return_date', 'status']:
            sort = 'borrow_date'
        
        # Calculate offset if not provided
        if offset is None:
            offset = (page - 1) * limit
        
        conn = get_db_connection()
        
        # Build WHERE clause for filtering
        where_conditions = ["1=1"]  # Base condition
        params = []
        
        if user_id:
            where_conditions.append("b.user_id = ?")
            params.append(user_id)
        
        if status:
            where_conditions.append("b.status = ?")
            params.append(status)
            
        if book_id:
            where_conditions.append("b.book_id = ?")
            params.append(book_id)
        
        where_clause = " AND ".join(where_conditions)
        
        # Build ORDER BY clause
        sort_column = f"b.{sort}" if sort != 'id' else "b.id"
        order_clause = f"ORDER BY {sort_column} {order.upper()}"
        
        # Get total count for pagination
        count_query = f"""
            SELECT COUNT(*) as total 
            FROM borrows b
            JOIN books ON b.book_id = books.id
            WHERE {where_clause}
        """
        total_borrows = conn.execute(count_query, params).fetchone()['total']
        
        # Get borrows with pagination
        borrows_query = f"""
            SELECT b.*, books.title, books.author 
            FROM borrows b
            JOIN books ON b.book_id = books.id
            WHERE {where_clause}
            {order_clause}
            LIMIT ? OFFSET ?
        """
        params.extend([limit, offset])
        borrows = conn.execute(borrows_query, params).fetchall()
        conn.close()
        
        borrows_list = []
        for borrow in borrows:
            borrows_list.append({
                'id': borrow['id'],
                'user_id': borrow['user_id'],
                'book_id': borrow['book_id'],
                'book_title': borrow['title'],
                'book_author': borrow['author'],
                'borrow_date': borrow['borrow_date'],
                'return_date': borrow['return_date'],
                'status': borrow['status']
            })
        
        # Calculate pagination info
        total_pages = (total_borrows + limit - 1) // limit  # Ceiling division
        has_next = page < total_pages
        has_prev = page > 1
        
        return jsonify({
            'success': True,
            'data': borrows_list,
            'pagination': {
                'page': page,
                'limit': limit,
                'offset': offset,
                'total_items': total_borrows,
                'total_pages': total_pages,
                'has_next': has_next,
                'has_prev': has_prev
            },
            'filters': {
                'user_id': user_id,
                'status': status,
                'book_id': book_id
            },
            'sorting': {
                'sort': sort,
                'order': order
            },
            'message': f'Found {len(borrows_list)} borrow records (page {page} of {total_pages})'
        }), 200
        
    except Exception as e:
        return jsonify({
            'success': False,
            'message': f'Error retrieving borrow records: {str(e)}'
        }), 500