from flask import Flask, jsonify
from flask_swagger_ui import get_swaggerui_blueprint
from .database import init_db, get_db_connection, add_sample_data
from .routes.v1.book_routes import book_bp_v1
from .routes.v1.borrow_routes import borrow_bp_v1
from .routes.v1.user_routes import user_bp_v1

# Create Flask application
app = Flask(__name__)
app.secret_key = 'your_secret_key'

# Initialize database
init_db()
add_sample_data()

# Register blueprints
app.register_blueprint(book_bp_v1, url_prefix='/api/v1')
app.register_blueprint(borrow_bp_v1, url_prefix='/api/v1')
app.register_blueprint(user_bp_v1, url_prefix='/api/v1')

# Swagger UI Blueprint
SWAGGER_URL = '/api/docs'
API_URL = '/static/openapi_v1.yaml'
swaggerui_blueprint = get_swaggerui_blueprint(
    SWAGGER_URL,
    API_URL,
    config={
        'app_name': "Library API v1 Documentation"
    }
)
app.register_blueprint(swaggerui_blueprint, url_prefix=SWAGGER_URL)

# Serve OpenAPI YAML file
@app.route('/static/openapi_v1.yaml')
def serve_openapi_yaml():
    return app.send_static_file('openapi_v1.yaml')

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
            'borrows': '/api/v1/borrows',
            'users_borrows': '/api/v1/users/{id}/borrows'
        }
    })

if __name__ == '__main__':
    # Run the application
    app.run(debug=True, host='0.0.0.0', port=5000)