<div align="center">
<!-- Title: -->
  <a href="https://github.com/czxieddan/">
    <img src="https://czxieddan.top/favicon.ico" height="200">
  </a>
  <h1><a href="https://github.com/czxieddan/">CzXieDdan</a> - <a href="https://czxieddan.top">czxieddan.top</a></h1>
</div>
<div align="center">
<!-- Title: -->
  <a href="https://github.com/czxieddan/Flag-Converter">
    <img src="https://github.com/czxieddan/Flag-Converter/blob/main/Flag_Converter.png?raw=true" height="200">
  </a>
  <h1><a href="https://github.com/czxieddan/Flag-Converter">Flag Converter</a> - <a href="https://github.com/czxieddan/Beat-down-the-Sun#tools">Beat down the sun Tools</a></h1>
</div>

**Description:**
This tool supports the quick conversion of the required .tga files for flags and can automatically generate three sizes needed for the game, storing them in the corresponding folders. You can upload multiple files in bulk, and the program supports one-click conversion.

[v0.0.0.1](https://github.com/czxieddan/Flag-Converter/releases/tag/v0.0.0.1)

by [czxieddan ](https://czxieddan.top)

# Flag Converter

This tool supports the quick conversion of the required .tga files for flags and can automatically generate three sizes needed for the game, storing them in the corresponding folders. You can upload multiple files in bulk, and the program supports one-click conversion.

## ENVIRONMENT

[![pypi supported versions](https://img.shields.io/pypi/pyversions/kubernetes.svg)](https://pypi.python.org/pypi/kubernetes)

```python
from PIL import Image, ImageFilter, ImageEnhance
from flask import Flask, render_template_string, request
import os
import webbrowser
import threading
import numpy as np  
```

**The above environment needs to be configured.**

```
Python: Create Environment
```

```pip
pip install -r requirements.txt
```

```pip
altgraph==0.17.4
auto-py-to-exe==2.46.0
blinker==1.9.0
bottle==0.13.3
bottle-websocket==0.2.9
certifi==2025.4.26
cffi==1.17.1
charset-normalizer==3.4.2
click==8.2.0
colorama==0.4.6
Eel==0.18.1
Flask==3.1.1
future==1.0.0
gevent==25.5.1
gevent-websocket==0.10.1
greenlet==3.2.2
idna==3.10
imageio==2.37.0
imageio-ffmpeg==0.6.0
itsdangerous==2.2.0
Jinja2==3.1.6
MarkupSafe==3.0.2
Nuitka==2.7.3
numpy==2.2.6
opencv-python==4.11.0.86
ordered-set==4.1.0
packaging==25.0
pefile==2023.2.7
pillow==11.2.1
psutil==7.0.0
pycparser==2.22
pyinstaller==6.13.0
pyinstaller-hooks-contrib==2025.4
pyparsing==3.2.3
pywin32-ctypes==0.2.3
requests==2.32.3
setuptools==80.7.1
typing_extensions==4.13.2
urllib3==2.4.0
Werkzeug==3.1.3
zope.event==5.0
zope.interface==7.2
zstandard==0.23.0
```

## PROCESS IMAGES

```py
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
```

### BLURRING

Blurring of images to optimise the look and feel, with the freedom to adjust the parameters to achieve a preferred effect.Blurring of images to optimise the look and feel, with the freedom to adjust the parameters to achieve a preferred effect.

```py
img_resized = img_resized.filter(ImageFilter.GaussianBlur(radius=0.11))
img_resized = enhancer.enhance(0.5)  
```

## CONTACTS

You can reach me via **[my personal blog](https://czxieddan.top)** or directly by sending an email to **czxieddan@czxieddan.top**.




