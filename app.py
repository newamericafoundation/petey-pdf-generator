from io import BytesIO

import requests
from flask import Flask, request, abort, jsonify
from weasyprint import HTML

app = Flask("newamerica-pdfgen")

@app.route("/generate-pdf/", methods=["post"])
def generate_pdf():
    if not request.json:
        abort(400)

    for required_field in ['html', 'base_url', 'filename', 's3_upload']:
        if required_field not in request.json:
            abort(400)

    # Generate PDF
    output = BytesIO()
    HTML(string=request.json['html'], base_url=request.json['base_url']).write_pdf(output)

    # Upload to S3
    s3_upload_response = requests.post(request.json['s3_upload']['url'], data=request.json['s3_upload']['fields'], files={'file': (request.json['filename'], output.getvalue())})

    return jsonify({
        'filesize': len(output.getvalue()),
        's3_upload_response_status_code': s3_upload_response.status_code,
    })

if __name__ == "__main__":
    app.run()
