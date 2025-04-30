from flask import Flask, request, jsonify
import pytesseract
from PIL import Image
import re
import os

app = Flask(__name__)

# Configurer PyTesseract (si nécessaire)
pytesseract.pytesseract.tesseract_cmd = '/usr/bin/tesseract'  # Linux (Render)

@app.route('/upload', methods=['POST'])
def upload_file():
    if 'file' not in request.files:
        return jsonify({"error": "Aucun fichier uploadé"}), 400

    file = request.files['file']
    if file.filename == '':
        return jsonify({"error": "Fichier vide"}), 400

    # Sauvegarder temporairement le fichier
    filepath = os.path.join("uploads", file.filename)
    file.save(filepath)

    # Extraire le texte avec OCR
    try:
        text = pytesseract.image_to_string(Image.open(filepath))
        os.remove(filepath)  # Nettoyer

        # Exemple d'extraction de données avec regex
        invoice_data = {
            "date": re.search(r'\d{2}/\d{2}/\d{4}', text).group() if re.search(r'\d{2}/\d{2}/\d{4}', text) else "Non trouvé",
            "total": re.search(r'Total\s+\$\d+\.\d{2}', text).group() if re.search(r'Total\s+\$\d+\.\d{2}', text) else "Non trouvé"
        }
        return jsonify(invoice_data)

    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    os.makedirs("uploads", exist_ok=True)
    app.run(debug=True)
