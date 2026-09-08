import os
from dotenv import load_dotenv
from flask import Flask
from flask_sqlalchemy import SQLAlchemy

load_dotenv()

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get('DATABASE_URL')
db = SQLAlchemy(app)

class Fragrance(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    brand = db.Column(db.String(100))
    notes = db.Column(db.String(500))
    family = db.Column(db.String(50))
    season = db.Column(db.String(50))
    occasion = db.Column(db.String(50))
    price = db.Column(db.Float)

    def __repr__(self):
        return f'<Fragrance {self.name}>'

@app.route('/')
def home():
    return 'Sniffnote activated!'

if __name__ == '__main__':
    app.run(debug=True)
    