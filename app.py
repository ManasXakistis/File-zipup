from flask import Flask, request, send_file, render_template
import os
from huffman import HuffmanCoding  # Import HuffmanCoding from your implementation

app = Flask(__name__)

# File directories
UPLOAD_FOLDER = 'uploads'
PROCESSED_FOLDER = 'processed'
os.makedirs(UPLOAD_FOLDER, exist_ok=True)       # Ensure upload folder exists
os.makedirs(PROCESSED_FOLDER, exist_ok=True)   # Ensure processed folder exists

@app.route('/')
def index():
    # Render the HTML template
    return render_template('index.html')

@app.route('/', methods=['POST'])
def compress_file():
    # Handle file upload
    file = request.files.get('file')  # Use `get` to avoid KeyErrors if no file is provided
    if file and file.filename.endswith('.txt'):  # Only accept .txt files
        input_path = os.path.join(UPLOAD_FOLDER, file.filename)
        file.save(input_path)

        # Perform Huffman compression
        huffman = HuffmanCoding(input_path)  # Instantiate HuffmanCoding with input file
        output_path = huffman.compress()  # Ensure your HuffmanCoding class has a `compress` method

        # Move the compressed file to the processed folder
        compressed_file_path = os.path.join(PROCESSED_FOLDER, 'compressed.bin')
        os.rename(output_path, compressed_file_path)

        # Send the compressed file for download
        return send_file(compressed_file_path, as_attachment=True, attachment_filename='compressed.bin')

    return "Invalid file format. Please upload a .txt file.", 400

if __name__ == '__main__':
    app.run(debug=True)
