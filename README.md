# PDF Parser API with Docling

This is a FastAPI application that uses Docling to parse PDF files and extract their content in various formats.

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

### Parse PDF File

**Endpoint**: `/file-handler`
**Method**: POST
**Content-Type**: multipart/form-data

**Parameters**:
- `file`: The PDF file to parse

**Example using curl**:
```bash
curl -X POST "http://localhost:5010/file-handler" -H "accept: application/json" -H "Content-Type: multipart/form-data" -F "file=@/path/to/your/file.pdf"
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
  "text": "Document Title\n\nContent in plain text format...",
  "metadata": {
    "pages": 5,
    "title": "Document Title"
  }
}
```

## Features

- Parses PDF documents using Docling
- Extracts content in multiple formats (markdown, text)
- Returns document metadata
- Handles file uploads efficiently with temporary file storage
