import io
from time import time

from PIL import Image
from flask import Flask, request, make_response

HORIZONTAL_PIXELS = 80
VERTICAL_PIXELS = 60

app = Flask(__name__)

pixels = [0] * HORIZONTAL_PIXELS * VERTICAL_PIXELS

last_status = None
shoot = False


@app.route("/", methods=["GET"])
def home():
    with open("index.html", "r") as file:
        content = file.read()

    if last_status != None and time() - last_status > 5:
        camera_status = "PŘIPRAVENA FOTIT"
    else:
        camera_status = "ČEKÁ NA PŘIPOJENÍ NEBO PRÁVĚ FOTÍ"

    return content.format(camera_status)


@app.route("/status/", methods=["POST"])
def status():
    last_status = time()


@app.route("/shoot/", methods=["GET", "POST"])
def shoot():
    if request.method == "GET":
        if shoot:
            return "Y"
        else:
            return "N"

    if request.method == "POST":
        data = request.data.decode("utf-8")

        if data == "OK":
            shoot = False
        else:
            shoot = True

        return home()


@app.route("/bitmap/", methods=["GET", "POST"])
def bitmap():
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
