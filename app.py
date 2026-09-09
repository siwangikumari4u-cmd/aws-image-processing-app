from flask import Flask, render_template, request
import boto3
from PIL import Image
import os

app = Flask(__name__)

BUCKET_NAME = "my-image-processing-bucket-132"

s3 = boto3.client("s3")

@app.route("/", methods=["GET", "POST"])
def upload():

    if request.method == "POST":

        file = request.files["image"]

        if file:

            original = "original_" + file.filename

            file.save(original)

            img = Image.open(original)

            img = img.resize((500, 500))

            processed = "processed_" + file.filename

            img.save(processed)

            s3.upload_file(
                processed,
                BUCKET_NAME,
                processed
            )

            return "Image processed and uploaded successfully!"

    return render_template("index.html")

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
