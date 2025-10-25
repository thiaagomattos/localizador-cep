from app import create_app
from flask import Flask, request, jsonify
from database import init_db

app = create_app()

init_db()
if __name__ == '__main__':
    app.run(debug=True, port=5000)