from flask import Flask, jsonify
from .database import init_db, get_db_connection
from .routes.v1.book_routes import book_bp
from .routes.v1.borrow_routes import borrow_bp
from .routes.v2.book_routes import book_bp_v2
from .routes.v2.borrow_routes import borrow_bp_v2
from .routes.v3.book_routes import book_bp_v3
from .routes.v3.borrow_routes import borrow_bp_v3
from .routes.v4.book_routes import book_bp_v4
from .routes.v4.borrow_routes import borrow_bp_v4

# Create Flask application
app = Flask(__name__)
app.secret_key = 'your_secret_key'

# Register blueprints
app.register_blueprint(book_bp, url_prefix='/api/v1')
app.register_blueprint(borrow_bp, url_prefix='/api/v1')
app.register_blueprint(book_bp_v2, url_prefix='/api/v2')
app.register_blueprint(borrow_bp_v2, url_prefix='/api/v2')
app.register_blueprint(book_bp_v3, url_prefix='/api/v3')
app.register_blueprint(borrow_bp_v3, url_prefix='/api/v3')
app.register_blueprint(book_bp_v4, url_prefix='/api/v4')
app.register_blueprint(borrow_bp_v4, url_prefix='/api/v4')

# Error handlers
@app.errorhandler(404)
def not_found(error):
    return jsonify({
        'success': False,
        'message': 'Endpoint not found'
    }), 404

@app.errorhandler(405)
def method_not_allowed(error):
    return jsonify({
        'success': False,
        'message': 'Method not allowed'
    }), 405

@app.errorhandler(500)
def internal_error(error):
    return jsonify({
        'success': False,
        'message': 'Internal server error'
    }), 500

# Root endpoint
@app.route('/')
def home():
    return jsonify({
        'success': True,
        'message': 'Library Management API',
        'version': 'v1',
        'endpoints': {
            'books': '/api/v1/books',
            'borrows': '/api/v1/borrows'
        },
        'v4_endpoints': {
            'books': '/api/v4/books',
            'borrows': '/api/v4/borrows'
        }
    })

if __name__ == '__main__':
    # Initialize database
    init_db()
    
    # Run the application
    app.run(debug=True, host='0.0.0.0', port=5000)