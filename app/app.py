from flask import Flask, request, render_template_string, send_from_directory
import os
from prometheus_flask_exporter import PrometheusMetrics

app = Flask(__name__)
metrics = PrometheusMetrics(app)

UPLOAD_FOLDER = '/uploads'
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

HTML = '''
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <title>File Upload on Kubernetes</title>
    <style>
        body {
            font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
            background-color: #f0f4f8;
            margin: 0;
            padding: 40px;
            text-align: center;
        }

        h1, h2 {
            color: #2c3e50;
        }

        form {
            margin: 20px auto;
            padding: 20px;
            background-color: #fff;
            border-radius: 12px;
            box-shadow: 0 0 15px rgba(0, 0, 0, 0.1);
            display: inline-block;
        }

        input[type="file"] {
            margin-bottom: 10px;
        }

        input[type="submit"] {
            background-color: #3498db;
            color: white;
            padding: 10px 20px;
            border: none;
            border-radius: 6px;
            cursor: pointer;
        }

        input[type="submit"]:hover {
            background-color: #2980b9;
        }

        ul {
            list-style-type: none;
            padding: 0;
        }

        li {
            padding: 5px 0;
            margin-bottom: 10px;
            display: flex;
            justify-content: center;
            align-items: center;
            gap: 20px;
        }

        a {
            color: #34495e;
            text-decoration: none;
        }

        a:hover {
            text-decoration: underline;
        }

        .message {
            color: green;
            margin-top: 10px;
        }

        .delete-btn {
            background-color: #e74c3c;
            color: white;
            padding: 5px 10px;
            border: none;
            border-radius: 4px;
            cursor: pointer;
        }

        .delete-btn:hover {
            background-color: #c0392b;
        }
    </style>
</head>
<body>
    <h1>Kubernetes File Uploader</h1>
    <form action="/" method="post" enctype="multipart/form-data">
        <input type="file" name="file" required/><br/>
        <input type="submit" value="Upload"/>
    </form>
    <div class="message">{{ msg }}</div>

    <h2>Uploaded Files</h2>
    <ul>
        {% for file in files %}
            <li>
                <a href="/uploads/{{ file }}" target="_blank">{{ file }}</a>
                <form action="/delete/{{ file }}" method="post" style="display:inline;">
                    <button type="submit" class="delete-btn">Delete</button>
                </form>
            </li>
        {% else %}
            <li>No files uploaded yet.</li>
        {% endfor %}
    </ul>
</body>
</html>
'''

@app.route("/", methods=["GET", "POST"])
def upload():
    msg = ""
    if request.method == "POST":
        f = request.files['file']
        if f:
            f.save(os.path.join(UPLOAD_FOLDER, f.filename))
            msg = "Uploaded successfully!"
    files = os.listdir(UPLOAD_FOLDER)
    return render_template_string(HTML, msg=msg, files=files)

@app.route("/uploads/<filename>")
def uploaded_file(filename):
    return send_from_directory(UPLOAD_FOLDER, filename)

@app.route("/delete/<filename>", methods=["POST"])
def delete_file(filename):
    try:
        os.remove(os.path.join(UPLOAD_FOLDER, filename))
        msg = f"File {filename} deleted successfully!"
    except FileNotFoundError:
        msg = f"File {filename} not found."
    files = os.listdir(UPLOAD_FOLDER)
    return render_template_string(HTML, msg=msg, files=files)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=80)
