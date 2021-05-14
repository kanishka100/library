from flask import Flask, render_template, request, url_for
from flask_sqlalchemy import SQLAlchemy
from werkzeug.utils import redirect

""" creating sqlite database,this database comes with python """
# db = sqlite3.connect("books-collection.db")
# cursor = db.cursor()
# # cursor.execute(
# #     "CREATE TABLE books(id INTEGER PRIMARY KEY, title varchar(250) NOT NULL UNIQUE,author varchar(250) NOT NULL,rating FLOAT NOT NULL)")
# cursor.execute("INSERT INTO books VALUES(1,'Harry Potter','J.J. Rowling','9.3')")
# db.commit()


app = Flask(__name__)
all_books = []
# creating database
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///new-books-collection.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)


# creating table model
class Book(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(250), unique=True, nullable=False)
    author = db.Column(db.String(250), nullable=False)
    rating = db.Column(db.Float, nullable=False)

    # this is optional,helps in identifing each book object
    def __repr__(self):
        my_books = {'title': self.title,
                    'id': self.id,
                    'rating': float(self.rating)}
        return f'{my_books}'


# create table
db.create_all()

# new_book = Book(id=1, title='Harry Potter', author="J.K.Rowlings", rating=9.2)
# db.session.add(new_book)
# db.session.commit()

"""Home page"""


@app.route('/')
def home():
    """The data type of the result returned on querying the database is a list."""
    return render_template("index.html", books=Book.query.all())


""" deleting a certain book and then redirecting to home again"""


@app.route("/<int:id>", methods=["GET", "POST"])
def abc(id):
    book_to_delete = Book.query.get(id)
    db.session.delete(book_to_delete)
    db.session.commit()
    return redirect(url_for("home"))


"""to add new books"""


@app.route("/add", methods=["GET", "POST"])
def add():
    if request.method == "POST":
        title = request.form['title']
        author = request.form['author']
        rating = request.form['rating']
        # all_books.append(new_book)

        # adding new book into database
        new_book = Book(title=title, author=author, rating=rating)
        db.session.add(new_book)
        db.session.commit()
        print((Book.query.all()))
        return render_template("index.html", books=Book.query.all())
    else:
        return render_template("add.html")


"""to edit the rating of books"""


@app.route('/edit/<int:id>', methods=['GET', 'POST'])
def edit(id):
    book = Book.query.filter_by(id=id).first()
    if request.method == "POST":
        book_to_update = Book.query.get(id)
        book_to_update.rating = request.form['new_rating']
        db.session.commit()
        return redirect(url_for('home'))
    return render_template("rating_edit.html", book=book)


if __name__ == "__main__":
    app.run(debug=True)
