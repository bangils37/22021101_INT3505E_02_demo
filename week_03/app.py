from flask import Flask, jsonify
from database import init_db
from routes.books import books_bp
from routes.borrows import borrows_bp

# Create Flask application
app = Flask(__name__)

# Register blueprints
app.register_blueprint(books_bp)
app.register_blueprint(borrows_bp)

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
        }
    })

if __name__ == '__main__':
    # Initialize database
    init_db()
    
    # Run the application
    app.run(debug=True, host='0.0.0.0', port=5000)