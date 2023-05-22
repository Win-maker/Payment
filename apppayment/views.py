from django.shortcuts import render
from pytesseract import pytesseract
import os
import re
from PIL import Image

class OCR:
    def __init__(self):
        self.path = r'C:\Program Files\Tesseract-OCR\tesseract.exe'

    def extract(self, filename):
        pytesseract.tesseract_cmd = self.path
        img = Image.open(filename)
        text = pytesseract.image_to_string(img)
        return text

def getPayment(request):
    if request.method == 'POST' and request.FILES.get('image'):
        img = request.FILES['image']
        # Extract text from image
        ocr = OCR()
        text = ocr.extract(img)

        split_text = text.split('\n')

        for item in split_text:
            if re.findall("^Ma |^Mg | ^Daw | ^U", item):
                transfer_name = item[0:len(item)-11]

            if re.findall("^(0[1-9]|[12][0-9]|3[01])/(0[1-9]|1[012])/(19|20)", item):
                transfer_time = item

            if re.findall("Ks$", item):
                transfer_amount = item

            if re.findall("[0123456789]", item) and len(item) == 20:
                transfer_id = item

        return render(request, 'result.html', {'name':transfer_name, 'time':transfer_time, 'id':transfer_id,
                                               'amount':transfer_amount})

    return render(request, 'getPayment.html')








