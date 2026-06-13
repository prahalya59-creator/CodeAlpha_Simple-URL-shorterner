from flask import Flask, request, jsonify, redirect
from models import db, URL
import random
import string
import validators

app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.db'

db.init_app(app)


def generate_code():
    return ''.join(
        random.choices(
            string.ascii_letters + string.digits,
            k=6
        )
    )


@app.route('/')
def home():
    return "URL Shortener is Running!"


@app.route('/shorten', methods=['POST'])
def shorten():

    data = request.get_json()

    long_url = data['url']

    # Validate URL
    if not validators.url(long_url):
        return jsonify({
            "error": "Invalid URL"
        }), 400

    # Custom short code
    custom_code = data.get('custom')

    if custom_code:
        code = custom_code
    else:
        code = generate_code()

    # Check duplicate code
    existing = URL.query.filter_by(
        short_code=code
    ).first()

    if existing:
        return jsonify({
            "error": "Short code already exists"
        }), 400

    new_url = URL(
        original_url=long_url,
        short_code=code
    )

    db.session.add(new_url)
    db.session.commit()

    return jsonify({
        "short_url": f"http://127.0.0.1:5000/{code}"
    })



@app.route('/<code>')
def redirect_url(code):

    url = URL.query.filter_by(
        short_code=code
    ).first()

    if url:

        url.clicks += 1

        db.session.commit()

        return redirect(url.original_url)

    return "URL Not Found"


@app.route('/stats/<code>')
def stats(code):

    url = URL.query.filter_by(
        short_code=code
    ).first()

    if not url:
        return jsonify({
            "error": "URL Not Found"
        }), 404

    return jsonify({
        "original_url": url.original_url,
        "short_code": url.short_code,
        "clicks": url.clicks
    })


if __name__ == '__main__':

    with app.app_context():
        db.create_all()

    app.run(debug=True)
