from io import BytesIO

import requests
from flask import Flask, request, abort
from weasyprint import HTML

app = Flask("newamerica-pdfgen")

@app.route("/generate-pdf/", methods=["post"])
def generate_pdf():
    if not request.json:
        abort(400)

    for required_field in ['html', 'base_url', 'filename', 's3_upload']:
        if required_field not in request.json:
            abort(400)

    output = BytesIO()
    HTML(string=request.json['html'], base_url=request.json['base_url']).write_pdf(output)

    # Upload to S3
    response = requests.post(request.json['s3_upload']['url'], data=request.json['s3_upload']['fields'], files={'file': (request.json['filename'], output.getvalue())})

    # Ping callback URL
    if 'callback_url' in request.json:
        data = {
            'filename': request.json['filename'],
            'filesize': len(output.getvalue()),
        }
        if 'request_id' in request.json:
            data['request_id'] = request.json['request_id']
        requests.post(request.json['callback_url'], json=data)

if __name__ == "__main__":
    app.run()
