import io

from PIL import Image
from flask import Flask, request, make_response

HORIZONTAL_PIXELS = 80
VERTICAL_PIXELS = 60

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
    global pixels

    if request.method == "GET":
        data = pixels2bmp(pixels)
        response = make_response(data)
        response.headers.set("Content-Type", "image/bmp")

        return response

    if request.method == "POST":
        data = request.data.decode("utf-8")

        filtered = [s for s in data.split(" ") if s.isdigit()]
        values = [int(s) for s in filtered]

        row = values.pop(0)
        for i in range(row * HORIZONTAL_PIXELS, (row + 1) * HORIZONTAL_PIXELS):
            pixels[i] = values[i % HORIZONTAL_PIXELS]

        print("============")
        print(row)
        print(values)
        print("============")

        return ""


def pixels2bmp(pixels):
    width = HORIZONTAL_PIXELS
    height = VERTICAL_PIXELS

    image = Image.frombytes('L', (width, height), bytes(pixels))

    bmp_buffer = io.BytesIO()
    image.save(bmp_buffer, format='BMP')

    return bmp_buffer.getvalue()


if __name__ == "__main__":
    app.run(debug=True)
