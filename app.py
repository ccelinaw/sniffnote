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

class CollectionItem(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    fragrance_id = db.Column(db.Integer, db.ForeignKey('fragrance.id'), nullable=False)
    date_added = db.Column(db.DateTime, server_default=db.func.now())

    fragrance = db.relationship('Fragrance', backref='collection_entries')

    def __repr__(self):
        return f'<CollectionItem {self.fragrance_id}>'

@app.route('/')
def home():
    return 'Sniffnote activated!'

@app.route('/search')
def search():
    query = request.args.get('q', '').strip()
    results = []
    if query:
        words = query.split()
        filters = []
        for word in words:
            filters.append(
                (Fragrance.name.ilike(f'%{word}%')) | (Fragrance.brand.ilike(f'%{word}%'))
            )
        # Require ALL words to match somewhere (name or brand)
        combined_filter = filters[0]
        for f in filters[1:]:
            combined_filter = combined_filter & f

        results = Fragrance.query.filter(combined_filter).order_by(
            # Exact/closer name matches first
            Fragrance.name.ilike(f'{query}%').desc(),
            Fragrance.rating_count.desc()
        ).limit(50).all()

    return render_template('search.html', results=results, query=query)

@app.route('/collection/add/<int:fragrance_id>', methods=['POST'])
def add_to_collection(fragrance_id):
    existing = CollectionItem.query.filter_by(fragrance_id=fragrance_id).first()
    if not existing:
        item = CollectionItem(fragrance_id=fragrance_id)
        db.session.add(item)
        db.session.commit()
    return redirect('/collection')

@app.route('/collection')
def collection():
    items = CollectionItem.query.all()
    return render_template('collection.html', items=items)

if __name__ == '__main__':
    app.run(debug=True)
    