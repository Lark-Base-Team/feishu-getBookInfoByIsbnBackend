import requests
from flask import Flask, jsonify, request
from flask_cors import CORS

app = Flask(__name__)
CORS(app, resources={r"/*": {"origins": "*"}})
app.config['CORS_ALLOW_ORIGINS'] = '*'
app.config['CORS_ALLOW_METHODS'] = ['GET', 'POST']


@app.route('/')
def index():
    return 'Hello from Flask!'


@app.route('/fetch_book_info', methods=['GET'])
def fetch_book_info():
    isbn = request.args.get('isbn')
    appcode = request.args.get('appcode')
    print("isbn: ", isbn)
    print("appcode: ", appcode)
    if not isbn or not appcode:
        return jsonify({"error": "Missing ISBN or appcode"}), 400

    host = 'http://jisuisbn.market.alicloudapi.com'
    path = '/isbn/query'
    querys = f'isbn={isbn}'
    url = f"{host}{path}?{querys}"

    headers = {
        'Authorization': f'APPCODE {appcode}',
        'Content-Type': 'application/json; charset=UTF-8'
    }

    try:
        # Disable SSL certificate verification
        response = requests.get(url, headers=headers, verify=False)
        print("response", response)

        content = response.json()
        print("content", content)
        return jsonify(content)
    except Exception as e:
        return jsonify({"error": str(e)}), 500


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
