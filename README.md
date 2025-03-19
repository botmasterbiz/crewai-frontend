# PDF Processing with Docling and CrewAI

This is a FastAPI application that uses Docling to parse PDF files and extract their content, then analyzes this content using CrewAI to generate structured reports and insights.

## Features

- **Document Parsing**: Uses Docling to extract text content from PDF files
- **AI Analysis**: Processes extracted content with CrewAI to generate structured reports
- **API Interface**: Simple REST API for file upload and processing
- **Markdown Export**: Returns parsed content in markdown format
- **Clean Implementation**: Proper error handling and temporary file management

## Requirements

- Python 3.9+
- FastAPI
- Docling
- CrewAI
- Other dependencies as specified in requirements.txt

## Setup

1. Clone the repository:

```bash
git clone <your-repository-url>
cd <repository-directory>
```

2. Set up a virtual environment (recommended):

```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. Install the required dependencies:

```bash
pip install -r requirements.txt
```

4. Environment variables (optional):
   
If you want to customize the CrewAI behavior or use specific LLM models, you can create a `.env` file with appropriate settings:

```
OPENAI_API_KEY=your_openai_api_key
MODEL_NAME=gpt-4-turbo
# Add other environment variables as needed
```

5. Run the application:

```bash
python app.py
```

The API will be available at `http://<your-local-ip>:5010`.

## API Endpoints

### Process PDF File

**Endpoint**: `/file-handler`  
**Method**: POST  
**Content-Type**: multipart/form-data

**Parameters**:
- `file`: The PDF file to parse and analyze

**Example using curl**:
```bash
curl -X POST "http://localhost:5010/file-handler" \
  -H "accept: application/json" \
  -H "Content-Type: multipart/form-data" \
  -F "file=@/path/to/your/file.pdf"
```

**Example using JavaScript/Fetch**:
```javascript
const formData = new FormData();
formData.append('file', pdfFile); // pdfFile is a File object

fetch('http://localhost:5010/file-handler', {
  method: 'POST',
  body: formData
})
.then(response => response.json())
.then(data => console.log(data))
.catch(error => console.error('Error:', error));
```

**Response**:
```json
{
  "filename": "example.pdf",
  "markdown": "# Document Title\n\nContent in markdown format...",
  "result": {
    "key_points": ["Point 1", "Point 2", "..."],
    "quick_summary": "Summary of the document...",
    "extended_summary": "Detailed analysis...",
    "actionable_insights": ["Insight 1", "Insight 2", "..."],
    "source_documents": ["Document title and description..."],
    "potential_biases": "Discussion of biases..."
  }
}
```

## Implementation Details

### How It Works

1. **PDF Processing**:
   - The application receives a PDF file through the `/file-handler` endpoint
   - Docling's DocumentConverter processes the PDF and extracts structured content
   - The content is converted to markdown format for further processing

2. **AI Analysis**:
   - The markdown content is passed to the CrewAI system
   - A researcher agent analyzes the content according to the task definition
   - The agent generates a structured report with key points, summaries, and insights

3. **Result Delivery**:
   - Both the original markdown and the AI-generated analysis are returned to the client
   - The response includes detailed sections as specified in the task configuration

### CrewAI Task Configuration

The CrewAI system is configured to analyze documents with a specific focus. The task configuration is defined in `file_crew/src/file_crew/config/tasks.yaml` and includes:

- Extracting key points from the document
- Creating executive summaries
- Providing detailed analysis
- Suggesting actionable insights
- Identifying potential biases in the source material

## Testing

You can use the included test script to try out the API:

```bash
python test_pdf_parser.py /path/to/your/file.pdf
```

This will:
1. Upload the specified PDF to the API
2. Process the file through both Docling and CrewAI
3. Display a summary of the results in the terminal
4. Save the full results to a JSON file

## Project Structure

```
.
├── app.py                  # FastAPI application
├── requirements.txt        # Project dependencies
├── test_pdf_parser.py      # Test script for the API
├── file_crew/
│   └── src/
│       └── file_crew/
│           ├── main.py     # CrewAI integration
│           └── config/
│               └── tasks.yaml  # Task definitions for the AI analysis
```

## Troubleshooting

- **PDF Parsing Issues**: Make sure the uploaded PDF is not corrupted and doesn't have DRM protection
- **CrewAI Errors**: Check that any required environment variables are set correctly
- **API Connection Issues**: Verify that the API is running and accessible from your client


## Acknowledgements

- [Docling](https://github.com/docling-project/docling) for PDF parsing
- [CrewAI](https://github.com/joaomdmoura/crewAI) for AI agent orchestration
