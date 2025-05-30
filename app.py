from flask import Flask, request, jsonify
import requests
import re

app = Flask(__name__)

def get_tiktok_video_url(url):
    try:
        headers = {
            "User-Agent": "Mozilla/5.0"
        }
        response = requests.get(url, headers=headers)
        video_url = re.search(r'playAddr":"(.*?)"', response.text)
        if video_url:
            return video_url.group(1).replace("\\u0026", "&").replace("\\", "")
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
