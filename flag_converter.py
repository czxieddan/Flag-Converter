from PIL import Image, ImageFilter, ImageEnhance
from flask import Flask, render_template_string, request
import os
import webbrowser
import threading
import numpy as np  
app = Flask(__name__)
OUTPUT_FOLDER = "gfx/flags"
UPLOAD_FOLDER = "gfx/flags"
os.makedirs(UPLOAD_FOLDER, exist_ok=True)
os.makedirs(OUTPUT_FOLDER, exist_ok=True)
HTML_TEMPLATE = """
<!DOCTYPE html>
<html lang="zh">
<head>
    <meta charset="UTF-8">
    <title>Flag Converter</title>
    <link rel="icon" href="https://czxieddan.top/favicon.ico">
    <style>
        .container { display: flex; flex-wrap: wrap; gap: 20px; }
        .image-box { position: relative; display: inline-block; }
        .image-box img { max-width: 200px; border: 1px solid black; }
        .crop-box { position: absolute; border: 2px solid red; pointer-events: none; }
        .button-container button {
            padding: 10px 20px; background-color: #4395ff; color: white; border: none; border-radius: 5px; cursor: pointer; font-size: 16px;
            }
    </style>
</head>
<body>
    <h1>Flag Converter</h1>
    <h3>Upload flag images then click on the "Convert" button after typing in the information to go ahead and do the conversion.</h3>
    <form method="POST" enctype="multipart/form-data">
        <input type="file" name="files" accept=".png,.jpg,.dds,.tga" multiple><br>
        <div class="container" id="fileInputs"></div>
        
        <button type="submit" style="padding: 10px 20px; background-color: #4395ff; color: white; border: none; border-radius: 5px; cursor: pointer; font-size: 16px;">Convert</button>
    </form>
    <script>
        document.querySelector("input[name='files']").addEventListener("change", function(event) {
            let container = document.getElementById("fileInputs");
            container.innerHTML = "";
            for (let file of event.target.files) {
                let div = document.createElement("div");
                div.classList.add("image-box");
                let url = URL.createObjectURL(file);       
                div.innerHTML = `<b>${file.name}</b><br>
                                Flag: <input type='text' name='flag_name_${file.name}' required><br>
                                X1: <input type='number' name='crop_x1_${file.name}' class='crop' data-img='${file.name}' value='0'><br>
                                Y1: <input type='number' name='crop_y1_${file.name}' class='crop' data-img='${file.name}' value='0'><br>
                                X2: <input type='number' name='crop_x2_${file.name}' class='crop' data-img='${file.name}'><br>
                                Y2: <input type='number' name='crop_y2_${file.name}' class='crop' data-img='${file.name}'><br>
                                <div class="image-box">
                                   <img src='${url}' id='img_${file.name}'>
                                   <div class='crop-box' id='box_${file.name}'></div>
                                </div>`;
                container.appendChild(div);
                let img = document.getElementById(`img_${file.name}`);
                img.onload = function() {
                    document.querySelector(`[name='crop_x2_${file.name}']`).value = img.naturalWidth;
                    document.querySelector(`[name='crop_y2_${file.name}']`).value = img.naturalHeight;
                };
            }
        });       
        document.querySelector("form").addEventListener("submit", function(event) {
            let allInputs = document.querySelectorAll("input[type='text'], input[type='number']");
            for (let input of allInputs) {
                if (!input.value.trim()) {
                    alert("Required fields");
                    event.preventDefault();
                    return;
                }
            }
        });
        document.addEventListener("input", function(event) {
            if (event.target.classList.contains("crop")) {
                let imgName = event.target.getAttribute("data-img");
                let img = document.getElementById(`img_${imgName}`);
                let box = document.getElementById(`box_${imgName}`);
                let scaleX = img.clientWidth / img.naturalWidth; 
                let scaleY = img.clientHeight / img.naturalHeight; 
                let x1 = (document.querySelector(`[name='crop_x1_${imgName}']`).value || 0) * scaleX;
                let y1 = (document.querySelector(`[name='crop_y1_${imgName}']`).value || 0) * scaleY;
                let x2 = (document.querySelector(`[name='crop_x2_${imgName}']`).value || img.naturalWidth) * scaleX;
                let y2 = (document.querySelector(`[name='crop_y2_${imgName}']`).value || img.naturalHeight) * scaleY;
                box.style.left = `${x1}px`;
                box.style.top = `${y1}px`;
                box.style.width = `${x2 - x1}px`;
                box.style.height = `${y2 - y1}px`;
            }
        });        
    </script>
    <footer id="footer" class="footer">
        <div class="copyright" style="text-align: center;">
            <span><a href="https://czxieddan.top" target="_blank">© czxieddan</a></span>
        </div>
  

    </footer>
</body>
</html>
"""
def safe_int(value, default=0):
    try:
        return int(value) if value and value.strip() else default
    except ValueError:
        return default
from PIL import Image
def process_image(img_path, flag_name, crop_area):
    with Image.open(img_path) as img:
        img = img.convert("RGBA")
        img = img.crop(crop_area)
        alpha_channel = img.split()[-1]
        folders = ["gfx", "gfx/flags", "gfx/flags/medium", "gfx/flags/small"]
        for folder in folders:
            if not os.path.exists(folder):  
                os.makedirs(folder, mode=0o777)  
        sizes = [(82, 52), (41, 26), (10, 7)]
        paths = [
            os.path.join(OUTPUT_FOLDER, f"{flag_name}.tga"),
            os.path.join(OUTPUT_FOLDER, "medium", f"{flag_name}.tga"),
            os.path.join(OUTPUT_FOLDER, "small", f"{flag_name}.tga"),
        ]
        for size, path in zip(sizes, paths):
            
            img_resized = img.resize(size, Image.Resampling.LANCZOS)
            img_resized = img_resized.resize(size, Image.Resampling.BICUBIC) 
            img_resized = img_resized.filter(ImageFilter.GaussianBlur(radius=0.11))
            enhancer = ImageEnhance.Sharpness(img_resized)
            img_resized = enhancer.enhance(0.5)  
            img_resized = img_resized.convert("RGBA")
            img_resized.save(path, format="TGA", compression=None)
@app.route("/", methods=["GET", "POST"])
def index():
    if request.method == "POST":
        files = request.files.getlist("files")         
        for file in files:
            file_path = os.path.join(OUTPUT_FOLDER, file.filename)
            file.save(file_path) 
            flag_name = request.form.get(f"flag_name_{file.filename}", file.filename.split('.')[0])
            with Image.open(file_path) as img:
                crop_x2_default = img.size[0]  
                crop_y2_default = img.size[1]  
            x1 = safe_int(request.form.get(f"crop_x1_{file.filename}", "0"))
            y1 = safe_int(request.form.get(f"crop_y1_{file.filename}", "0"))
            x2 = safe_int(request.form.get(f"crop_x2_{file.filename}", str(crop_x2_default)))
            y2 = safe_int(request.form.get(f"crop_y2_{file.filename}", str(crop_y2_default)))           
            process_image(file_path, flag_name, (x1, y1, x2, y2))          
            os.remove(file_path)
        return f"{len(files)} image(s) converted"
    return render_template_string(HTML_TEMPLATE)
def open_browser():
    webbrowser.open("http://127.0.0.1:5000/")
if __name__ == "__main__":
    threading.Timer(1, open_browser).start()  
    app.run(debug=True)