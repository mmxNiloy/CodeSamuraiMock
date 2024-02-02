from app import app, db
from flask import render_template, request, Response
from models import Book
import json

@app.route('/', methods=['GET'])
def index():
    return {
        'message': 'Hello from team Schadenfreude',
    }

@app.route('/api/books', methods=['POST', 'GET'])
def add():
    if request.method == 'POST':
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
    elif request.method == 'GET':
        books = Book.query.order_by(Book.id).all()
        print(books)
        # Serialize data
        serializedBooks = []

        for book in books:
            serializedBooks.append(book.to_dict())
        
        sData = {
            'books': serializedBooks
        }

        return Response(json.dumps(sData), status=200, mimetype='application/json')

@app.route('/api/books/<int:id>', methods=['GET', 'PUT'])
def get_book(id):
    print(id)
    b = Book.query.filter(Book.id == id).first()
    
    if b == None:
        return Response(json.dumps({'message': f'book with id: {id} was not found'}), status=404, content_type='application/json')

    print(b)
    
    if request.method == 'GET':
        return Response(json.dumps(b.to_dict()), status=200, mimetype='application/json')
    if request.method == 'PUT':
        # Change database
        data = request.get_json()
        
        title = data.get('title')
        author = data.get('author')
        genre = data.get('genre')
        price = data.get('price')

        b.title = title
        b.author = author
        b.genre = genre
        b.price = price

        db.session.commit()

        return Response(json.dumps(b.to_dict()), status=200, mimetype='application/json')

