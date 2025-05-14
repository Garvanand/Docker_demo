import requests

def test_pdf_processing():
    url = 'http://localhost:8000/api/v1/process-pdf'
    
    files = {
        'file': ('test.pdf', open('test.pdf', 'rb'), 'application/pdf')
    }
    
    try:
        response = requests.post(url, files=files)
        print(f"Status Code: {response.status_code}")
        print("\nResponse:")
        print(response.json())
        
    except Exception as e:
        print(f"Error: {str(e)}")
    finally:
        files['file'][1].close()

if __name__ == "__main__":
    test_pdf_processing() 