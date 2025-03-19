# PDF Processing with Docling and CrewAI

This is a FastAPI application that uses Docling to parse PDF files and extract their content, then analyzes this content using CrewAI.

## Features

- **Document Parsing**: Uses Docling to extract text content from PDF files
- **AI Analysis**: Processes extracted content with CrewAI to generate structured reports
- **API Interface**: Simple REST API for file upload and processing
- **Markdown Export**: Returns parsed content in markdown format
- **Clean Implementation**: Proper error handling and temporary file management

## Setup

1. Install the required dependencies:

```bash
pip install -r requirements.txt
```

2. Run the application:

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

- The application first uses Docling to extract text content from the uploaded PDF
- The extracted markdown content is then processed by CrewAI with a researcher agent
- The researcher agent analyzes the content and generates a structured report
- Both the original markdown and the AI-generated analysis are returned to the client

## Testing

You can use the included test script to try out the API:

```bash
python test_pdf_parser.py /path/to/your/file.pdf
```
