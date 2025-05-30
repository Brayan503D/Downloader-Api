from flask import Flask, request, jsonify
import requests
import re
import html

app = Flask(__name__)

def get_tiktok_video_url(url):
    try:
        headers = {
            "User-Agent": "Mozilla/5.0"
        }
        response = requests.get(url, headers=headers)
        video_url = re.search(r'playAddr":"(.*?)"', response.text)
        if video_url:
            # Desescapa \u002F y otros caracteres
            raw_url = video_url.group(1)
            decoded_url = raw_url.replace("\\u0026", "&").replace("\\", "")
            decoded_url = html.unescape(decoded_url)  # decodifica cualquier entidad HTML
            return decoded_url
        return None
    except Exception as e:
        return None

@app.route('/api/tiktok', methods=['GET'])
def download_tiktok():
    tiktok_url = request.args.get('url')
    if not tiktok_url:
        return jsonify({'error': 'Falta el parámetro URL'}), 400

    video_url = get_tiktok_video_url(tiktok_url)
    if video_url:
        return jsonify({'video_url': video_url})
    else:
        return jsonify({'error': 'No se pudo obtener el video'}), 500

if __name__ == '__main__':
    app.run(debug=True)
