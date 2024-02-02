from app import app, db
from flask import render_template, request, Response
from sqlalchemy import desc
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
        if bool(request.args):
            title = request.args.get('title')
            author = request.args.get('author')
            genre = request.args.get('genre')
            sort = request.args.get('sort')
            order = request.args.get('order')
            
            query = None

            if order == None:
                order = 'ASC'
            
            # Handle search fields 
            if title != None:
                query = Book.query.filter(Book.title == title)
            elif author != None:
                query = Book.query.filter(Book.author == author)
            elif genre != None:
                query = Book.query.filter(Book.genre == genre)
            else:
                query = Book.query
            
            # Handle sort fields
            if sort == 'title':
                if order == 'ASC':
                    query = query.order_by(Book.title)
                else:
                    query = query.order_by(desc(Book.title))
            elif sort == 'genre':
                if order == 'ASC':
                    query = query.order_by(Book.genre)
                else:
                    query = query.order_by(desc(Book.genre))
            elif sort == 'author':
                if order == 'ASC':
                    query = query.order_by(Book.author)
                else:
                    query = query.order_by(desc(Book.author))
            elif sort == 'price':
                if order == 'ASC':
                    query = query.order_by(Book.price)
                else:
                    query = query.order_by(desc(Book.price))
            else:
                if order == 'ASC':
                    query = query.order_by(Book.id)
                else:
                    query = query.order_by(desc(Book.id))
            mBooks = query.all()
            print(mBooks)

            mSerializedBooks = []

            for book in mBooks:
                mSerializedBooks.append(book.to_dict())
            
            mSerializedData = {
                'books': mSerializedBooks
            }

            return Response(json.dumps(mSerializedBooks), status=200, mimetype='application/json')
        else:
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

