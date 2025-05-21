import io
from time import time

from PIL import Image
from flask import Flask, request, make_response, redirect, url_for

HORIZONTAL_PIXELS = 80
VERTICAL_PIXELS = 60
SAMPLING_FREQ = 50

app = Flask(__name__)

pixels = [0] * HORIZONTAL_PIXELS * VERTICAL_PIXELS

last_status = None
shoot = False


@app.route("/", methods=["GET"])
def home():
    with open("index.html", "r") as file:
        content = file.read()

    if last_status != None and time() - last_status < 5:
        camera_status = "PŘIPRAVENA FOTIT"
    else:
        camera_status = "ČEKÁ NA PŘIPOJENÍ NEBO PRÁVĚ FOTÍ"

    return content.format(camera_status)


@app.route("/status/", methods=["POST"])
def status():
    global last_status

    last_status = time()
    return ""


@app.route("/shoot/", methods=["GET", "POST"])
def capture():
    global shoot
    global HORIZONTAL_PIXELS
    global VERTICAL_PIXELS
    global SAMPLING_FREQ

    if request.method == "GET":
        print(f"SHOOT: {shoot}")
        if shoot:
            return f"Y\n{HORIZONTAL_PIXELS}\n{VERTICAL_PIXELS}\n{SAMPLING_FREQ}"
        else:
            return "N\n0\n0\n0"

    if request.method == "POST":
        data = request.data.decode("utf-8")

        if data == "OK":
            shoot = False
        else:
            HORIZONTAL_PIXELS = request.form["HORIZONTAL_PIXELS"]
            VERTICAL_PIXELS = request.form["VERTICAL_PIXELS"]
            SAMPLING_FREQ = request.form["SAMPLING_FREQ"]
            shoot = True

        return redirect(url_for("home"))


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
