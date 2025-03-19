from fastapi import FastAPI, HTTPException, Body, File, Form, UploadFile
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
import socket
import json
from typing import List
import uvicorn
import tempfile
import os
from docling.document_converter import DocumentConverter
from file_crew.src.file_crew.main import run

def get_local_ip():
    try:
        # Create a socket object
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        # Doesn't actually connect, just helps us get local IP
        s.connect(('8.8.8.8', 80))
        ip = s.getsockname()[0]
        s.close()
        return ip
    except Exception:
        return '127.0.0.1'  # Fallback to localhost if can't get IP

app = FastAPI(title="CrewAI API")

# Configure CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Allows all origins
    allow_credentials=True,
    allow_methods=["*"],  # Allows all methods
    allow_headers=["*"],  # Allows all headers
)

@app.post("/file-handler")
async def file_handler_endpoint(
    file: UploadFile = File(...)
):
    try:
        print(f"Received file: {file}")
        
        # Create a temporary file to save the uploaded PDF
        with tempfile.NamedTemporaryFile(delete=False, suffix='.pdf') as temp_file:
            # Write the uploaded file content to the temporary file
            content = await file.read()
            temp_file.write(content)
            temp_file_path = temp_file.name
        
        try:
            # Initialize the DocumentConverter
            converter = DocumentConverter()
            
            # Convert the PDF document
            result = converter.convert(temp_file_path)
            
            # Get the parsed content in different formats
            markdown_content = result.document.export_to_markdown()
            
            # Clean up the temporary file
            os.unlink(temp_file_path)
            
            print(f"Markdown content: {markdown_content}")
            result = run(markdown_content)
            print(f"Result: {result}")
            
            # Return the parsed content
            return {
                "filename": file.filename,
                "markdown": markdown_content,
                "result": result.model_dump()
            }
        
        except Exception as e:
            # Clean up the temporary file in case of error
            if os.path.exists(temp_file_path):
                os.unlink(temp_file_path)
            raise e
            
    except json.JSONDecodeError as e:
        print(f"JSON decode error: {str(e)}")
        raise HTTPException(status_code=400, detail=f"Invalid JSON payload: {str(e)}")
    except Exception as e:
        print(f"Error in file_handler: {str(e)}")
        import traceback
        traceback.print_exc()
        raise HTTPException(status_code=500, detail=str(e))

if __name__ == "__main__":
    host_ip = get_local_ip()
    uvicorn.run("app:app", host=host_ip, port=5010, reload=True)
