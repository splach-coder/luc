import fitz
from flask import Blueprint, jsonify, request
import os

search_blueprint = Blueprint('search', __name__)

def search_text_with_coords(pdf_path, search_text):
    results = []
    pdf_document = fitz.open(pdf_path)

    for page in pdf_document:
        blocks = page.get_text("blocks")
        for block in blocks:
            text = block[4]  # Accessing the text content of the block (index 4)
            if search_text in text:
                # Access coordinates by index (avoiding unpacking issue)
                x0 = block[0]
                y0 = block[1]
                x1 = block[2]
                y1 = block[3]

                result = {
                    "text": text,
                    "x0": x0,
                    "y0": y0,
                    "x1": x1,
                    "y1": y1,
                }
                results.append(result)

    return results
    


@search_blueprint.route('/api/invoice/search', methods=['POST'])
def search_data():
    if 'file' not in request.files or 'text' not in request.form:
        return jsonify({"error": "Missing 'file' or 'text' in request data"}), 400

    file = request.files['file']
    search_text = request.form['text']

    if file.filename == '':
        return jsonify({"error": "No selected file"}), 400

    try:
        pdf_path = os.path.join('./temp', file.filename)
        file.save(pdf_path)
        
        results = search_text_with_coords(pdf_path, search_text)
        
        # Optionally, remove the saved file after processing
        os.remove(pdf_path)
        
        return jsonify(results), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500