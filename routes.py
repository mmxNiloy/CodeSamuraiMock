from app import app, db
from flask import render_template, request, Response
from models import Book
import json

@app.route('/', methods=['GET'])
def index():
    return {
        'message': 'Hello from team Schadenfreude',
    }

@app.route('/api/books', methods=['POST'])
def add():
    data = request.get_json()
    # jData = json.loads(data)
    
    id = data.get('id')
    title = data.get('title')
    author = data.get('author')
    genre = data.get('genre')
    price = data.get('price')

    # print(id)
    rec = Book(id=id, title=title, author=author, genre=genre, price=price)
    # print(rec)

    db.session.add(rec)
    db.session.commit()

    return Response(json.dumps(rec.to_dict()), status=201, mimetype='application/json')

@app.route('/api/books/<int:id>', methods=['GET'])
def get_book(id):
    print(id)
    
    b = Book.query.filter(Book.id == id).first()

    print(b)

    if b == None:
        return Response(json.dumps({'message': f'book with id: {id} was not found'}), status=404, content_type='application/json')

    return Response(json.dumps(b.to_dict()), status=200, mimetype='application/json')