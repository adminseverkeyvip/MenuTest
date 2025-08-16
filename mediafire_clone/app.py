import os
import uuid
from flask import Flask, request, send_from_directory, redirect, url_for

app = Flask(__name__)

# Thư mục lưu file
UPLOAD_FOLDER = "uploads"
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

# Dictionary lưu map id -> filename
file_map = {}

@app.route("/", methods=["GET", "POST"])
def upload_file():
    if request.method == "POST":
        file = request.files["file"]
        if file:
            # Tạo tên id ngẫu nhiên (giống Mediafire link)
            file_id = uuid.uuid4().hex[:8]  # 8 ký tự random
            filename = file.filename
            path = os.path.join(UPLOAD_FOLDER, filename)
            file.save(path)

            # Lưu vào map
            file_map[file_id] = filename

            return f"""
            <h2>Upload thành công!</h2>
            <p>File: {filename}</p>
            <p>Link tải: <a href='/download/{file_id}'>https://your-render-url/download/{file_id}</a></p>
            <br><a href='/'>⬅️ Quay lại</a>
            """
    return '''
    <h1>Upload file (Mini Mediafire)</h1>
    <form method="post" enctype="multipart/form-data">
        <input type="file" name="file" required>
        <input type="submit" value="Upload">
    </form>
    '''

@app.route("/download/<file_id>")
def download_file(file_id):
    if file_id in file_map:
        filename = file_map[file_id]
        return send_from_directory(UPLOAD_FOLDER, filename, as_attachment=True)
    return "<h2>File không tồn tại hoặc đã bị xóa.</h2>"

if __name__ == "__main__":
    # Render yêu cầu host=0.0.0.0 và lấy port từ biến môi trường
    port = int(os.environ.get("PORT", 8000))
    app.run(host="0.0.0.0", port=port)
