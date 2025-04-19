import io

from PIL import Image
from flask import Flask, request, make_response

app = Flask(__name__)

pixels = [[0] * 40 for _ in range(40)]


@app.route("/lpe/", methods=["GET"])
def home():
    return "TEST"


@app.route("/lpe/status/", methods=["GET", "POST"])
def camera_status():
    pass


@app.route("/lpe/last/", methods=["GET", "POST"])
def last_photo():
    if request.method == "GET":
        data = pixels2bmp(pixels)
        response = make_response(data)
        response.headers.set("Content-Type", "image/bmp")

        return response

    if request.method == "POST":
        data = request.data.decode("utf-8")
        print(data)


def pixels2bmp(pixels):
    width = len(pixels[0])
    height = len(pixels)
    flat = []

    for row in pixels:
        for pixel in row:
            flat.append(pixel)

    image = Image.frombytes('L', (width, height), bytes(flat))

    bmp_buffer = io.BytesIO()
    image.save(bmp_buffer, format='BMP')

    return bmp_buffer.getvalue()


if __name__ == "__main__":
    app.run(debug=True)
