from flask import Flask, render_template, request, send_from_directory, jsonify
import os
import youtube_dl
import ssl
import certifi

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
    video_title = None
    try:
        ssl._create_default_https_context = ssl._create_unverified_context
        with youtube_dl.YoutubeDL(ydl_opts) as ydl:
            info_dict = ydl.extract_info(url, download=True)
            video_title = ydl.prepare_filename(info_dict)
        return video_title
    except Exception as e:
        return str(e)

@app.route('/download', methods=['POST'])
def download_video():
    url = request.form['url']
    downloads_path = os.path.expanduser('~/Downloads/')  # Ensure this path is accessible on the server
    video_path = download_youtube_video(url, output_path=downloads_path)
    if video_path and os.path.exists(video_path):
        directory = os.path.dirname(video_path)
        filename = os.path.basename(video_path)
        return send_from_directory(directory, filename, as_attachment=True)
    else:
        return jsonify({'error': 'Failed to download the video.'}), 500

if __name__ == "__main__":
    app.run(debug=True, host='0.0.0.0', port=5000)  # Make sure to run on all interfaces
