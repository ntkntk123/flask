from flask import Flask, request, jsonify
import os
from telethon import TelegramClient
from telethon.errors import SessionPasswordNeededError
from telethon.tl.functions.messages import GetHistoryRequest

app = Flask(__name__)

# Telegram App credentials
api_id = 21647330
api_hash = '7591f9c230e678835e8f82a13dd31e3e'

@app.route('/get_code', methods=['GET'])
def get_code():
    phone = request.args.get('sdt')

    if not phone:
        return jsonify({'error': 'Thiếu số điện thoại (sdt)'}), 400

    # Save session file in the current folder
    session_path = phone

    client = TelegramClient(session_path, api_id, api_hash)

    try:
        client.connect()

        if not client.is_user_authorized():
            client.disconnect()
            return jsonify({'error': f'Session lỗi với số {phone}'}), 401

        messages = client.get_messages(777000, limit=1)
        for message in messages:
            msg = message.message
            if "code" in msg.lower():
                you_code = msg.split()[2].rstrip('.')
                client.disconnect()
                return jsonify({'sdt': phone, 'code': you_code})

        client.disconnect()
        return jsonify({'error': 'Không tìm thấy mã xác thực trong tin nhắn'}), 404

    except Exception as e:
        client.disconnect()
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True)
