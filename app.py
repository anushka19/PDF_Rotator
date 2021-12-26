from flask import Flask, make_response, jsonify, request
from PyPDF2 import PdfFileReader,PdfFileWriter 
#from os import listdir, system
import os

app=Flask(__name__)

@app.route('/pdf-rotate', methods=["POST"])
def pdf_rotate():

    request_data = request.get_json()
    
    path = request_data['path']
    page_number = request_data['page_number']
    angle_of_rotation = request_data['angle_of_rotation']


    if not os.path.exists(path) or not path.endswith('.pdf'):
        return make_response(jsonify({"message":"file does not exit or is not a pdf"},400))

    
    reader = PdfFileReader(os.path.abspath(path),"rb")

    writer=PdfFileWriter()

    for p in range(reader.numPages):
        page=reader.getPage(p)

        if page_number - 1 == p:
            page.rotateClockwise(angle_of_rotation)
        writer.addPage(page)
    
    with open('output/'+ os.path.basename(path), 'wb') as fp:
        writer.write(fp)
    return make_response(jsonify({"path": 'output/'+ os.path.basename(path)}),200)
    

#pdf_rotate("input/blockchain-white-paper.pdf",3,270)

if __name__ == "__main__":
    app.run(debug=True)
