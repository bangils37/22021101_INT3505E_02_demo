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
    """[F8] Lấy danh sách các bản ghi mượn"""
    try:
        conn = get_db_connection()
        
        # Get query parameters for filtering
        user_id = request.args.get('user_id')
        status = request.args.get('status')
        
        query = '''
            SELECT b.*, books.title, books.author 
            FROM borrows b
            JOIN books ON b.book_id = books.id
            WHERE 1=1
        '''
        params = []
        
        if user_id:
            query += ' AND b.user_id = ?'
            params.append(user_id)
        
        if status:
            query += ' AND b.status = ?'
            params.append(status)
        
        query += ' ORDER BY b.borrow_date DESC'
        
        borrows = conn.execute(query, params).fetchall()
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
        
        return jsonify({
            'success': True,
            'data': borrows_list,
            'message': 'Borrow records retrieved successfully'
        }), 200
        
    except Exception as e:
        return jsonify({
            'success': False,
            'message': f'Error retrieving borrow records: {str(e)}'
        }), 500