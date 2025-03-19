import requests
import sys
import json
import os

def test_pdf_parsing(pdf_path, api_url="http://localhost:5010/file-handler"):
    """
    Test the PDF parsing API with a local PDF file.
    
    Args:
        pdf_path (str): Path to the PDF file to test
        api_url (str): URL of the API endpoint
    """
    if not os.path.exists(pdf_path):
        print(f"Error: File {pdf_path} does not exist.")
        return
    
    print(f"Testing PDF parsing with file: {pdf_path}")
    
    # Prepare the file for upload
    files = {'file': (os.path.basename(pdf_path), open(pdf_path, 'rb'), 'application/pdf')}
    
    try:
        # Send the request
        response = requests.post(api_url, files=files)
        
        # Check if the request was successful
        if response.status_code == 200:
            result = response.json()
            
            # Print a summary of the result
            print("\n=== PDF Parsing Result ===")
            print(f"Filename: {result.get('filename')}")
            print(f"Pages: {result.get('metadata', {}).get('pages', 'N/A')}")
            print(f"Title: {result.get('metadata', {}).get('title', 'N/A')}")
            
            # Print a preview of the text content
            text_content = result.get('text', '')
            preview_length = min(500, len(text_content))
            print(f"\nText Preview (first {preview_length} chars):")
            print(text_content[:preview_length] + "..." if len(text_content) > preview_length else text_content)
            
            # Save the full result to a JSON file
            output_file = f"{os.path.splitext(os.path.basename(pdf_path))[0]}_parsed.json"
            with open(output_file, 'w') as f:
                json.dump(result, f, indent=2)
            
            print(f"\nFull result saved to: {output_file}")
            
        else:
            print(f"Error: API returned status code {response.status_code}")
            print(f"Response: {response.text}")
    
    except Exception as e:
        print(f"Error occurred: {str(e)}")
    
    finally:
        # Close the file
        files['file'][1].close()

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python test_pdf_parser.py <path_to_pdf_file>")
        sys.exit(1)
    
    pdf_path = sys.argv[1]
    test_pdf_parsing(pdf_path) 