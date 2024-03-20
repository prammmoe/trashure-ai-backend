from flask import Flask, jsonify, render_template, request
import numpy as np
import tensorflow as tf
from PIL import Image

# Load model and class_names
model = tf.keras.models.load_model('models/model.h5')
class_names = np.load('models/nama_kelas.npy')
print('Model loaded. Start serving ...')

# Initiate Flask app
app = Flask(__name__)

# Home route
@app.route("/")
def home_page():
    data = {}  # Empty dictionary for initial rendering
    return render_template("index.html", data=data)

@app.route("/klasifikasi", methods=["POST"])
def klasifikasi():
    if request.method == "POST":
        uploaded_file = request.files["image"]
        if uploaded_file is not None:
            pil_image = Image.open(uploaded_file.stream)
            pil_image = pil_image.convert('RGB')
            pil_image = pil_image.resize((299, 299))
            image_array = np.array(pil_image) / 255.

            prediction = model.predict(np.expand_dims(image_array, axis=0))
            index = np.argmax(prediction)
            confidence = prediction[0][index]

            if confidence >= 0.6:
                nama_kelas = class_names[index]
                data = {
                    "nama_kelas": nama_kelas,
                    "confidence": confidence*100,
                    "solusi": solusi(nama_kelas, class_names)
                }
                return render_template("index.html", data=data)
            
            else:
                data = {
                    "error": "Sampah tidak ditemukan. Coba lagi."
                }
                return render_template("index.html", data=data)
                # return jsonify(data)

def solusi(nama_kelas, nama_kelas_all):
    solusi_dict = {
        nama_kelas_all[0]: "kardus",
        nama_kelas_all[1]: "kaca",
        nama_kelas_all[2]: "kaleng",
        nama_kelas_all[3]: "organic_fresh",
        nama_kelas_all[4]: "organic_common",
        nama_kelas_all[5]: "organic_rot",
        nama_kelas_all[6]: "kertas",
        nama_kelas_all[7]: "gelas",
        nama_kelas_all[8]: "kantong",
        nama_kelas_all[9]: "botol",
        nama_kelas_all[10]: "alat_makan",
    }
    return solusi_dict.get(nama_kelas, "solusi_umum")


if __name__ == '__main__':
    app.run(debug=True, port=8001)