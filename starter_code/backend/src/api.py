import os
from flask import Flask, request, jsonify, abort
from sqlalchemy import exc
import json
from flask_cors import CORS

from .database.models import db_drop_and_create_all, setup_db, Drink
from .auth.auth import AuthError, requires_auth

app = Flask(__name__)
setup_db(app)
CORS(app)

db_drop_and_create_all()

## ROUTES
@app.route('/drinks', methods=['GET'])
def get_drinks():
    drinks = Drink.query.all()
    formatted_drinks = [drink.short() for drink in drinks]
    return jsonify({
        "success": True, 
        "drinks": formatted_drinks
    }), 200

@app.route('/drinks', methods=['POST'])
@requires_auth('post:drinks')
def add_drink(payload):
    print("here")
    data = request.get_json()
    try:
        drink = Drink(
            title=data.get('title', None),
            recipe=json.dumps(data.get('recipe', None))
        )
        drink.insert()
        formatted_drink = Drink.long(drink)
        return jsonify({
            "success": True,
            "drinks": [formatted_drink]
        }), 200
    except:
        abort(422)


@app.route('/drinks-detail')
@requires_auth('get:drinks-detail')
def drink_details(payload):
    drinks = Drink.query.all()
    formatted_drinks = [drink.long() for drink in drinks]
    return jsonify({
        "success": True, 
        "drinks": formatted_drinks
    }), 200

@app.route('/drinks/<int:drink_id>', methods=['PATCH'])
@requires_auth('patch:drinks')
def update_drink(payload, drink_id):
    print(drink_id)
    drink = Drink.query.filter_by(id=drink_id).one_or_none()

    if drink is None:
        abort(404)
    
    try:
        data = request.get_json()
        drink.recipe = json.dumps(data.get('recipe', None))
        drink.update()

        formatted_drink = drink.long()
        return jsonify({
            "success": True,
            "drinks": [formatted_drink]
        }), 200

    except:
        abort(422)


@app.route('/drinks/<int:drink_id>', methods=['DELETE'])
@requires_auth('delete:drinks')
def delete_drink(payload, drink_id):
    drink = Drink.query.filter_by(id=drink_id).one_or_none()

    if drink is None:
        abort(404)

    try:
        drink.delete()
        
        formatted_drink = drink.long()
        return jsonify({
            "success": True,
            "drinks": [formatted_drink]
        }), 200

    except:
        abort(422)

## Error Handling
@app.errorhandler(422)
def unprocessable(error):
    return jsonify({
        "success": False, 
        "error": 422,
        "message": "unprocessable"
    }), 422


@app.errorhandler(404)
def not_found(error):
    return jsonify({
        'success': False,
        'error': 404,
        'message': 'resource not found'
    }), 404


@app.errorhandler(405)
def method_not_allowed(error):
    return jsonify({
        'success': False,
        'error': 405,
        'message': 'method not allowed'
    }), 405


@app.errorhandler(500)
def server_error(error):
    return jsonify({
        'success': False,
        'error': 500,
        'message': 'server error'
    }), 500


@app.errorhandler(400)
def bad_request(error):
    return jsonify({
        'success': False,
        'error': 400,
        'message': 'bad request'
    }), 400

@app.errorhandler(401)
def auth_error(error):
    return jsonify({
        'success': False,
        'error': 401,
        'message': 'Unauthorized'
    }), 401


@app.errorhandler(403)
def forbidden(error):
    return jsonify({
        'success': False,
        'error': 403,
        'message': 'Forbidden'
    }), 403