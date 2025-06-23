from flask import Flask, request, jsonify
import asyncio
from telethon import TelegramClient

app = Flask(__name__)

# Telegram App credentials
api_id = 21647330
api_hash = '7591f9c230e678835e8f82a13dd31e3e'

@app.route('/get_code', methods=['GET'])
def get_code():
    phone = request.args.get('sdt')
    if not phone:
        return jsonify({'error': 'Thiếu số điện thoại (sdt)'}), 400

    try:
        result = asyncio.run(fetch_code(phone))
        return result
    except Exception as e:
        return jsonify({'error': str(e)}), 500

async def fetch_code(phone):
    session_path = phone  # session sẽ được lưu tên giống số điện thoại
    client = TelegramClient(session_path, api_id, api_hash)

    await client.connect()

    if not await client.is_user_authorized():
        await client.disconnect()
        return jsonify({'error': f'Session lỗi với số {phone}'}), 401

    try:
        messages = await client.get_messages(777000, limit=1)
        for message in messages:
            msg = message.message
            if "code" in msg.lower():
                code = msg.split()[2].rstrip('.')
                await client.disconnect()
                return jsonify({'sdt': phone, 'code': code})
    except Exception as e:
        await client.disconnect()
        return jsonify({'error': f'Lỗi khi đọc tin nhắn: {str(e)}'}), 500

    await client.disconnect()
    return jsonify({'error': 'Không tìm thấy mã xác thực trong tin nhắn'}), 404

if __name__ == '__main__':
    app.run(debug=True)
