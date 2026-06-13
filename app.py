from flask import Flask,request,jsonify,redirect
from models import db,URL
import random
import string

app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.db'

db.init_app(app)
def generate_code():
    return ''.join(
        random.choices(
            string.ascii_letters+string.digits,
            k=6
        )
    )
@app.route('/')
def home():
    return "Database Connected!"
@app.route('/shorten', methods=['POST'])
def shorten():

    data = request.get_json()

    long_url = data['url']

    code = generate_code()

    new_url = URL(
        original_url=long_url,
        short_code=code
    )

    db.session.add(new_url)

    db.session.commit()

    return jsonify({
        "short_url":
        f"http://127.0.0.1:5000/{code}"
    })
@app.route('/test')
def test():

    code = generate_code()

    new_url = URL(
        original_url="https://google.com",
        short_code=code
    )

    db.session.add(new_url)
    db.session.commit()

    return f"http://127.0.0.1:5000/{code}"
@app.route('/<code>')
def redirect_url(code):

    url = URL.query.filter_by(
        short_code=code
    ).first()

    if url:
        return redirect(url.original_url)

    return "URL Not Found"
if __name__ == '__main__':
    with app.app_context():
        db.create_all()

    app.run(debug=True)
