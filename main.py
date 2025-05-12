import io

from PIL import Image
from flask import Flask, request, make_response

HORIZONTAL_PIXELS = 160
VERTICAL_PIXELS = 120

app = Flask(__name__)

pixels = [0] * HORIZONTAL_PIXELS * VERTICAL_PIXELS


@app.route("/", methods=["GET"])
def home():
    return "TEST"


@app.route("/status/", methods=["GET", "POST"])
def status():
    pass


@app.route("/bitmap/", methods=["GET", "POST"])
def bitmap():
    if request.method == "GET":
        print(pixels)

        data = pixels2bmp(pixels)
        response = make_response(data)
        response.headers.set("Content-Type", "image/bmp")

        return response

    if request.method == "POST":
        data = request.data.decode("utf-8")

        filtered = [s for s in data.split(" ") if s.isdigit()]
        values = [int(s) for s in filtered]

        row = values.pop(0)
        for i in range(HORIZONTAL_PIXELS):
            pixels[row * HORIZONTAL_PIXELS + i] = values[i]

        print("============")
        print(row)
        print(values)
        print("============")

        return ""


def pixels2bmp(pixels):
    width = HORIZONTAL_PIXELS
    height = VERTICAL_PIXELS

    image = Image.frombytes("L", (width, height), bytes(pixels))

    bmp_buffer = io.BytesIO()
    image.save(bmp_buffer, format="BMP")

    return bmp_buffer.getvalue()


if __name__ == "__main__":
    app.run(debug=True)
