from flask import Flask, render_template, request, jsonify
import yt_dlp as youtube_dl
import ssl
import certifi
import os

app = Flask(__name__)


@app.route('/')
def home():
    return render_template('index.html')


def download_youtube_video(url, output_path=''):
    # Ensure output_path ends with a slash
    if not output_path.endswith('/'):
        output_path += '/'

    ydl_opts = {
        'format': 'best',
        'outtmpl': output_path + '%(title)s.%(ext)s',
        'nocheckcertificate': True,
        'http': {
            'verify': certifi.where()
        }
    }
    try:
        ssl._create_default_https_context = ssl._create_unverified_context
        with youtube_dl.YoutubeDL(ydl_opts) as ydl:
            ydl.download([url])
        return f"Downloaded: {url}"
    except Exception as e:
        return str(e)


@app.route('/download', methods=['POST'])
def download_video():
    url = request.form['url']
    downloads_path = os.path.expanduser('~/Downloads/')
    result = download_youtube_video(url, output_path=downloads_path)
    if "Downloaded" in result:
        return jsonify({'message': result})
    else:
        return jsonify({'error': result}), 500


if __name__ == "__main__":
    app.run(debug=True)
