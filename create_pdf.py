from fpdf import FPDF
import os

class PDF(FPDF):
    def header(self):
        self.set_font('Arial', 'B', 15)
        self.cell(0, 10, 'Test PDF Document', 0, 1, 'C')
        self.ln(10)

def create_test_pdf():
    pdf = PDF()
    pdf.add_page()
    pdf.set_font("Arial", size=12)
    pdf.set_auto_page_break(auto=True, margin=15)
    
    content = """This is a sample PDF file for testing.
This was a demo project hope you like it

Here's a simple table:"""
    
    for line in content.split('\n'):
        pdf.cell(0, 10, txt=line, ln=True)
    
    pdf.ln(10)
    
    table_data = [
        ['Name', 'Age', 'City'],
        ['Garv', '21', 'New Delhi'],
        ['Garv2', '21', 'Faridabad'],
        ['Friends', '65', 'Gurgaon']
    ]
    
    col_width = pdf.w / 4
    row_height = 10
    
    for header in table_data[0]:
        pdf.cell(col_width, row_height, header, 1, 0, 'C')
    pdf.ln()
    
    for row in table_data[1:]:
        for item in row:
            pdf.cell(col_width, row_height, item, 1, 0, 'C')
        pdf.ln()
    
    pdf.output("test.pdf")
    print(f"PDF created successfully at {os.path.abspath('test.pdf')}")

if __name__ == "__main__":
    create_test_pdf() 