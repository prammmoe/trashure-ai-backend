from flask import Flask, jsonify, render_template, request, redirect, url_for, flash
import numpy as np
import requests
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
    # Mengambil data JSON dari klasifikasi
    data = requests.get("http://127.0.0.1:8001/klasifikasi").json()

    # Menampilkan hasil klasifikasi
    return render_template("index.html", data=data)

@app.route("/klasifikasi", methods=["POST"])
def klasifikasi():
    if request.method == "POST":
        # Mengambil gambar
        uploaded_file = request.files["image"]
        if uploaded_file is not None:
            # Konversi gambar ke format yang sesuai
            pil_image = Image.open(uploaded_file.stream)
            pil_image = pil_image.convert('RGB')
            pil_image = pil_image.resize((299, 299))
            image_array = np.array(pil_image) / 255.

            # Prediksi
            prediction = model.predict(np.expand_dims(image_array, axis=0))
            index = np.argmax(prediction)
            confidence = prediction[0][index]

            # Tampilkan hasil

            if confidence >= 0.6:
                nama_kelas = solusi(index, class_names)
                data = {
                    "nama_kelas": nama_kelas,
                    "confidence": confidence*100,
                    "solusi": solusi(nama_kelas)
                }
                return jsonify(data)
            
            else:
                data = {
                    "error": "Sampah tidak ditemukan. Coba lagi."
                }
                return jsonify(data)

# Solusi berdasarkan jenis sampah
def solusi(nama_kelas_index, nama_kelas):
    solusi_dict = {
        nama_kelas[0]: "kardus",
        nama_kelas[1]: "kaca",
        nama_kelas[2]: "kaleng",
        nama_kelas[3]: "organic_fresh",
        nama_kelas[4]: "organic_common",
        nama_kelas[5]: "organic_rot",
        nama_kelas[6]: "kertas",
        nama_kelas[7]: "gelas",
        nama_kelas[8]: "kantong",
        nama_kelas[9]: "botol",
        nama_kelas[10]: "alat_makan",
    }
    return solusi_dict.get(nama_kelas_index, "solusi_umum")

if __name__ == '__main__':
    app.run(debug=True, port=8001)