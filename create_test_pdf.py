from fpdf import FPDF
import numpy as np
from PIL import Image
import io
import os

def create_test_image():
    img_array = np.random.randint(0, 255, (100, 100, 3), dtype=np.uint8)
    img = Image.fromarray(img_array)
    temp_path = "temp_image.png"
    img.save(temp_path)
    return temp_path

def create_test_pdf():
    pdf = FPDF()
    pdf.add_page()
    
    pdf.set_font("Arial", size=16)
    pdf.cell(200, 10, txt="Test PDF Document", ln=1, align="C")
    
    pdf.set_font("Arial", size=12)
    pdf.cell(200, 10, txt="This is a test document with various elements:", ln=1, align="L")
    
    pdf.set_font("Arial", size=10)
    pdf.multi_cell(0, 10, txt="This is a paragraph of text that will be used to test text extraction. It contains multiple sentences and testing usage ke liye")
    
    pdf.ln(10)
    pdf.cell(200, 10, txt="Sample Table:", ln=1, align="L")
    
    pdf.set_font("Arial", size=10)
    headers = ["Name", "Age", "City"]
    data = [
        ['Garv', '21', 'New Delhi'],
        ['Garv2', '21', 'Faridabad'],
        ['Friends', '65', 'Gurgaon']
    ]
    
    col_width = pdf.w / 3
    for header in headers:
        pdf.cell(col_width, 10, header, 1)
    pdf.ln()
    
    for row in data:
        for item in row:
            pdf.cell(col_width, 10, item, 1)
        pdf.ln()
    
    pdf.ln(10)
    pdf.cell(200, 10, txt="Sample Image:", ln=1, align="L")
    
    img_path = create_test_image()
    pdf.image(img_path, x=10, y=pdf.get_y(), w=50)
    
    pdf.output("test.pdf")
    
    if os.path.exists(img_path):
        os.remove(img_path)

if __name__ == "__main__":
    create_test_pdf() 