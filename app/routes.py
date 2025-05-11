from flask import Blueprint, jsonify, request
import logging

main_bp = Blueprint('main', __name__)
logger = logging.getLogger(__name__)

@main_bp.route('/health')
def health_check():
    """Health check endpoint"""
    return jsonify({
        'status': 'healthy',
        'message': 'Garv API is running'
    }), 200

@main_bp.route('/items', methods=['GET'])
def get_items():
    """Sample endpoint to demonstrate API functionality"""
    return jsonify({
        'items': [
            {'id': 1, 'name': 'Garv Anand'},
            {'id': 2, 'name': 'Garv Projects'},
            {'id': 3, 'name': 'Garv Docker Demo'}
        ]
    }), 200 