import requests
import sys
import json
import os

def test_pdf_parsing(pdf_path, api_url="http://localhost:5010/file-handler"):
    """
    Test the PDF parsing and AI analysis API with a local PDF file.
    
    Args:
        pdf_path (str): Path to the PDF file to test
        api_url (str): URL of the API endpoint
    """
    if not os.path.exists(pdf_path):
        print(f"Error: File {pdf_path} does not exist.")
        return
    
    print(f"Testing PDF processing with file: {pdf_path}")
    
    # Prepare the file for upload
    files = {'file': (os.path.basename(pdf_path), open(pdf_path, 'rb'), 'application/pdf')}
    
    try:
        # Send the request
        print("Sending request to API...")
        response = requests.post(api_url, files=files)
        
        # Check if the request was successful
        if response.status_code == 200:
            result = response.json()
            
            # Print a summary of the result
            print("\n=== PDF Processing Result ===")
            print(f"Filename: {result.get('filename')}")
            
            # Print a preview of the markdown content
            markdown_content = result.get('markdown', '')
            markdown_preview_length = min(300, len(markdown_content))
            print(f"\nMarkdown Content Preview (first {markdown_preview_length} chars):")
            print(markdown_content[:markdown_preview_length] + "..." if len(markdown_content) > markdown_preview_length else markdown_content)
            
            # Print a summary of the CrewAI analysis
            crew_result = result.get('result', {})
            print("\n=== CrewAI Analysis ===")
            
            if 'key_points' in crew_result:
                print("\nKey Points:")
                for i, point in enumerate(crew_result['key_points'], 1):
                    print(f"  {i}. {point}")
            
            if 'quick_summary' in crew_result:
                print("\nQuick Summary:")
                print(crew_result['quick_summary'])
            
            if 'actionable_insights' in crew_result:
                print("\nActionable Insights:")
                for i, insight in enumerate(crew_result['actionable_insights'], 1):
                    print(f"  {i}. {insight}")
            
            # Save the full result to a JSON file
            output_file = f"{os.path.splitext(os.path.basename(pdf_path))[0]}_processed.json"
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