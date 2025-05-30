from flask import Flask, request, jsonify
import requests
import re

app = Flask(__name__)

def extract_video_id(tiktok_url):
    # Redirige para obtener la URL completa (si es un enlace corto como vm.tiktok.com)
    try:
        response = requests.get(tiktok_url, allow_redirects=True, timeout=10)
        full_url = response.url
        match = re.search(r'/video/(\d+)', full_url)
        if match:
            return match.group(1)
    except:
        pass
    return None

def get_tiktok_info(video_id):
    try:
        headers = {
            "User-Agent": "Mozilla/5.0"
        }
        api_url = f"https://api.tiktokv.com/aweme/v1/feed/?aweme_id={video_id}"
        response = requests.get(api_url, headers=headers, timeout=10)
        data = response.json()

        video_data = data['aweme_list'][0]['video']
        no_watermark_url = video_data['play_addr']['url_list'][0]
        thumbnail_url = video_data['origin_cover']['url_list'][0]

        return {
            'video_url': no_watermark_url,
            'thumbnail_url': thumbnail_url
        }
    except:
        return None

@app.route('/api/tiktok', methods=['GET'])
def download_tiktok():
    tiktok_url = request.args.get('url')
    if not tiktok_url:
        return jsonify({'error': 'Falta el parámetro URL'}), 400

    video_id = extract_video_id(tiktok_url)
    if not video_id:
        return jsonify({'error': 'No se pudo extraer el ID del video'}), 400

    info = get_tiktok_info(video_id)
    if info:
        return jsonify(info)
    else:
        return jsonify({'error': 'No se pudo obtener la información del video'}), 500

if __name__ == '__main__':
    app.run(debug=True)
