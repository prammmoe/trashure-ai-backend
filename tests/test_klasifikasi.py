from io import BytesIO
from PIL import Image

import pytest
from src.app import App  

def test_klasifikasi_success():
    image = Image.new("RGB", (299, 299))
    image_bytes = BytesIO()
    image.save(image_bytes, format="JPG")
    image_bytes.seek(0)

    app = App(None)
    with app.app.test_client() as test_client:
        response = test_client.post("/klasifikasi", data={"image": (image_bytes, "image.jpg")})

        assert response.status_code == 200
        data = response.json
        assert "nama_kelas" in data
        assert "confidence" in data

def test_klasifikasi_no_image():
    app = App(None)

    with app.app.test_client() as test_client:
        response = test_client.post("/klasifikasi")

        assert response.status_code == 400

# Low Confidence Test
        
# Wrong Image Format Test

