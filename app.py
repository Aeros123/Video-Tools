from flask import Flask, render_template, request, send_file, flash, redirect, url_for
import yt_dlp
import os
from moviepy.editor import VideoFileClip
import shutil

app = Flask(__name__)
app.secret_key = 'your-secret-key'  # Required for flash messages
DOWNLOAD_FOLDER = "downloads"

# Create downloads folder
if not os.path.exists(DOWNLOAD_FOLDER):
    os.makedirs(DOWNLOAD_FOLDER)

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/download", methods=["POST"])
def download():
    url = request.form["url"]
    
    try:
        # YouTube download options
        ydl_opts = {
            'format': 'best[ext=mp4]',  # Best MP4 quality
            'outtmpl': os.path.join(DOWNLOAD_FOLDER, '%(title)s.%(ext)s'),
        }
        
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            # Get video info first
            info = ydl.extract_info(url, download=False)
            title = info.get('title', 'video')
            filename = f"{title}.mp4"
            filepath = os.path.join(DOWNLOAD_FOLDER, filename)
            
            # Download video
            ydl.download([url])
        
        return send_file(filepath, as_attachment=True, download_name=filename)
        
    except Exception as e:
        flash(f"Error: {str(e)}")
        return redirect(url_for('index'))

@app.route("/convert", methods=["POST"])
def convert():
    file = request.files["file"]
    if file:
        filepath = os.path.join(DOWNLOAD_FOLDER, file.filename)
        file.save(filepath)

        try:
            video = VideoFileClip(filepath)
            mp3_path = filepath.replace(".mp4", ".mp3").replace(".mkv", ".mp3")
            video.audio.write_audiofile(mp3_path)
            video.close()
            
            return send_file(mp3_path, as_attachment=True)
        except Exception as e:
            flash(f"Conversion error: {str(e)}")
            return redirect(url_for('index'))
    
    flash("No file selected")
    return redirect(url_for('index'))

if __name__ == "__main__":
    app.run(debug=True, host='0.0.0.0', port=5000)
echo "# Video-Tools" >> README.md
git init
git add README.md
git commit -m "first commit"
git branch -M main
git remote add origin https://github.com/Aeros123/Video-Tools.git
git push -u origin main
