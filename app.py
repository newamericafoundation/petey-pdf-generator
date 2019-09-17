from io import BytesIO

import requests
from flask import Flask, request, abort
from weasyprint import HTML

app = Flask("newamerica-pdfgen")

@app.route("/generate-pdf/", methods=["post"])
def generate_pdf():
    if not request.json:
        abort(400)

    output = BytesIO()
    HTML(string=request.json['html'], base_url=request.json['base_url']).write_pdf(output)

    # Upload to S3
    response = requests.post(request.json['s3_upload']['url'], data=request.json['s3_upload']['fields'], files={'file': (request.json['filename'], output.getvalue())})

    # Ping callback URL
    requests.post(request.json['callback_url'], json={
        'request_id': request.json['request_id'],
        'filename': request.json['filename'],
        'filesize': len(output.getvalue()),
    })

if __name__ == "__main__":
    app.run()
