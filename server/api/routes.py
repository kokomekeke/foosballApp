import io
import os
from datetime import datetime

import cv2
import numpy as np
import piexif
from PIL import Image
from flask import Blueprint, request, jsonify, send_file

from server.algos.image_processing import process_image
from server.algos.img_metadata import img_geoloc

api = Blueprint('api', __name__)

SAVE_FOLDER = './static/img'

image = None


@api.route('/edit-image', methods=['POST'])
def edit_image():
    if 'image' not in request.files:
        return jsonify({"error": "Nincs feltöltött kép"}), 400

    image_file = request.files['image']

    pil_image = Image.open(io.BytesIO(image_file.read()))

    global image
    image = pil_image

    image_np = np.array(pil_image)

    # 2️⃣ Ha a kép tartalmaz alfacsatornát (RGBA), akkor alakítsuk BGR-re
    if image_np.shape[-1] == 4:  # RGBA esetén
        image_np = cv2.cvtColor(image_np, cv2.COLOR_RGBA2BGR)
    elif image_np.shape[-1] == 3:  # RGB esetén
        image_np = cv2.cvtColor(image_np, cv2.COLOR_RGB2BGR)

    # Kép szerkesztése (példa: életlenítés)
    edited_image_np = process_image(image_np)

    edited_image_pil = Image.fromarray(cv2.cvtColor(edited_image_np, cv2.COLOR_BGR2RGB))

    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    filename = f"edited_{timestamp}.png"
    save_path = os.path.join(SAVE_FOLDER, filename)
    edited_image_pil.save(save_path)
    print(f"Kép mentve: {save_path}")

    # 5️⃣ Kép visszaküldése byte formátumban
    img_io = io.BytesIO()
    edited_image_pil.save(img_io, format="PNG")
    img_io.seek(0)

    return send_file(img_io, mimetype='image/png')


@api.route('/posterize', methods=['POST'])
def posterize():
    if 'image' not in request.files:
        return jsonify({"error": "Nincs feltöltött kép"}), 400

    image_file = request.files['image']

    pil_image = Image.open(io.BytesIO(image_file.read()))
    image_np = np.array(pil_image)

    # 2️⃣ Ha a kép tartalmaz alfacsatornát (RGBA), akkor alakítsuk BGR-re
    if image_np.shape[-1] == 4:  # RGBA esetén
        image_np = cv2.cvtColor(image_np, cv2.COLOR_RGBA2BGR)
    elif image_np.shape[-1] == 3:  # RGB esetén
        image_np = cv2.cvtColor(image_np, cv2.COLOR_RGB2BGR)

    # Kép szerkesztése (példa: életlenítés)
    edited_image_np = process_image(image_np)

    edited_image_pil = Image.fromarray(cv2.cvtColor(edited_image_np, cv2.COLOR_BGR2RGB))

    # 5️⃣ Kép visszaküldése byte formátumban
    img_io = io.BytesIO()
    edited_image_pil.save(img_io, format="PNG")
    img_io.seek(0)

    return send_file(img_io, mimetype='image/png')


@api.route('/geoloc', methods=['GET', 'POST'])
def get_geoloc():
    global image
    print(image)

    exif_dict = piexif.load(image.info.get('exif'))
    exif_dict = img_geoloc(exif_dict)
    # result = img_geoloc(image)
    result = exif_dict
    print("resultt", result)

    if "warning" in result:  # Ha nincs EXIF adat, ne 400-at küldjünk, csak figyelmeztetést
        return jsonify(result), 200  # A frontend így megkapja az üzenetet

    return jsonify({"exif_data": result}), 200