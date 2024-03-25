from flask import jsonify, request
import numpy as np
import tensorflow as tf
from PIL import Image


class App:
    def __init__(self, app):
        self.app = app

        # Load model and class_names
        self.model = tf.keras.models.load_model('../src/models/model.h5')
        self.class_names = np.load('../src/models/nama_kelas.npy')
        print('Model loaded. Start serving ...')

        # Define routes
        self.app.route("/", methods=["GET"])(self.home_page)
        self.app.route("/predict", methods=["POST", "GET"])(self.predict)

    def home_page(self):
        return "Trashure Backend API"

    def predict(self):
        if request.method == "POST":
            uploaded_file = request.files["image"]
            if uploaded_file is not None:
                pil_image = Image.open(uploaded_file.stream)
                pil_image = pil_image.convert('RGB')
                pil_image = pil_image.resize((299, 299))
                image_array = np.array(pil_image) / 255.

                prediction = self.model.predict(np.expand_dims(image_array, axis=0))
                index = np.argmax(prediction)
                confidence = prediction[0][index]

                if confidence >= 0.6:
                    nama_kelas = self.class_names[index]
                    data = {
                        "status": "success",
                        "data": {
                            "nama_kelas": nama_kelas,
                            "confidence": confidence*100,
                            "jenis_sampah": self.sampah(nama_kelas, self.class_names)
                        }
                    }
                    return jsonify(data) # return JSON 
                else:
                    data = {
                        "status": "error",
                        "data": {
                            "message": "Sampah tidak dikenali.",
                        }
                    }
                    return jsonify(data) # return JSON
                
        elif request.method == "GET":
            data = {
                        "status": "",
                        "data": {
                            "message": "",
                        }
                    }
            return jsonify(data) # return JSON

    def sampah(self, nama_kelas, nama_kelas_all):
        sampah_dict = {
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
        return sampah_dict.get(nama_kelas, "jenis_sampah_umum")
    
    def run(self):
        self.app.run(debug=True, host="0.0.0.0", port=8001)