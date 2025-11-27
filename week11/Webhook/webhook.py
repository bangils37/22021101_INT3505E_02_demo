# webhook.py
from flask import Flask, request, jsonify

app = Flask(__name__)

@app.route('/webhook', methods=['POST'])
def webhook():
    data = request.json
    event = data.get('event')
    message = data.get('message')

    print('--- Webhook received ---')
    print(f'Event: {event}')
    print(f'Message: {message}')
    print(f'🔔 Thông báo: {message}')

    return jsonify({'status': 'received'}), 200

if __name__ == '__main__':
    app.run(port=5000)