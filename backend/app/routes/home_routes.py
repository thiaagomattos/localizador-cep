from flask import request, Blueprint, jsonify
from app.services.home_service import *

home_routes = Blueprint('home_routes', __name__)

@home_routes.route('/api/get', methods=['GET'])
def get():
    return handle_get()

@home_routes.route('/api/post', methods=['POST'])
def post():
    return handle_post(request)

@home_routes.route('/api/getCep', methods=['GET'])
def get_cep():
    return handle_buscar_cep(request)

@home_routes.route('/api/delete', methods=['POST'])
def delete():
    return handle_delete(request)
