import os
from flask import Flask, render_template, request, jsonify
from werkzeug.utils import secure_filename
from PIL import Image
import numpy as np
from collections import Counter

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = 'uploads'
os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)

# ฟังก์ชันแยกประเภทขยะจากสีหลักในภาพ
def classify_by_color(image_path):
    img = Image.open(image_path).resize((100, 100)).convert('RGB')
    pixels = np.array(img).reshape(-1, 3)
    most_common = Counter([tuple(pixel) for pixel in pixels]).most_common(1)[0][0]
    r, g, b = most_common

    if g > r and g > b:
        return "Organic Waste (ขยะอินทรีย์)"
    elif r > 150 and g > 150 and b > 150:
        return "Plastic (ขยะพลาสติก)"
    elif b > r and b > g:
        return "Metal (ขยะโลหะ)"
    else:
        return "General Waste (ขยะทั่วไป)"

@app.route('/', methods=['GET', 'POST'])
def index():
    result = None
    image_path = None

    if request.method == 'POST':
        file = request.files['image']
        if file:
            filename = secure_filename(file.filename)
            filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
            file.save(filepath)

            result = classify_by_color(filepath)
            image_path = filepath

    return render_template('index.html', result=result, image=image_path)

# 🔧 ทำให้รองรับ Render.com และ localhost
if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))  # Render จะใช้ PORT จาก environment
    app.run(host='0.0.0.0', port=port)
