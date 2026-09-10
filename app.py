import os
from dotenv import load_dotenv
from flask import Flask
from flask import render_template, request, redirect
from flask_sqlalchemy import SQLAlchemy

load_dotenv()

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get('DATABASE_URL')
db = SQLAlchemy(app)

class Fragrance(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(200), nullable=False)
    brand = db.Column(db.String(100))
    country = db.Column(db.String(100))
    gender = db.Column(db.String(20))
    rating_value = db.Column(db.Float)
    rating_count = db.Column(db.Integer)
    year = db.Column(db.Integer)
    top_notes = db.Column(db.String(500))
    middle_notes = db.Column(db.String(500))
    base_notes = db.Column(db.String(500))
    perfumer1 = db.Column(db.String(100))
    perfumer2 = db.Column(db.String(100))
    main_accord1 = db.Column(db.String(50))
    main_accord2 = db.Column(db.String(50))
    main_accord3 = db.Column(db.String(50))
    main_accord4 = db.Column(db.String(50))
    main_accord5 = db.Column(db.String(50))
    url = db.Column(db.String(500))
    def __repr__(self):
        return f'<Fragrance {self.name}>'

@app.route('/')
def home():
    return 'Sniffnote activated!'

@app.route('/add', methods=['GET', 'POST'])
def add_fragrance():
    if request.method == 'POST':
        new_fragrance = Fragrance(
            name=request.form['name'],
            brand=request.form['brand'],
            notes=request.form['notes'],
            family=request.form['family'],
            season=request.form['season'],
            occasion=request.form['occasion'],
            price=request.form['price'] or None
        )
        db.session.add(new_fragrance)
        db.session.commit()
        return redirect('/collection')
    return render_template('add.html')

@app.route('/collection')
def collection():
    fragrances = Fragrance.query.all()
    return render_template('collection.html', fragrances=fragrances)

if __name__ == '__main__':
    app.run(debug=True)
    