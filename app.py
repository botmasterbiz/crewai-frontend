from fastapi import FastAPI, HTTPException, Body, File, Form, UploadFile
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
import socket
import json
from typing import List, Dict, Any
import uvicorn
import tempfile
import os
import logging
from docling.document_converter import DocumentConverter
from file_crew.src.file_crew.main import run

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Define allowed origins
ALLOWED_ORIGINS = [
    "https://dreamy-selkie-c16179.netlify.app",
    "http://localhost:3000",  # For local development
    "http://localhost:5173",  # For Vite development
    "https://content-topical-tomcat.ngrok-free.app",  # ngrok URL
]

def get_local_ip() -> str:
    """
    Get the local IP address of the machine.
    
    Returns:
        str: The local IP address, or '127.0.0.1' if it can't be determined.
    """
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        s.connect(('8.8.8.8', 80))
        ip = s.getsockname()[0]
        s.close()
        return ip
    except Exception:
        return '127.0.0.1'

app = FastAPI(
    title="CrewAI API",
    description="API for processing documents with Docling and CrewAI",
    version="1.0.0"
)

# Configure CORS for ngrok and Netlify
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Allow all origins temporarily for testing
    allow_credentials=True,
    allow_methods=["*"],  # Allow all methods
    allow_headers=["*"],  # Allow all headers
    expose_headers=["*"],
    max_age=3600,
)

# Add OPTIONS handler for /file-handler
@app.options("/file-handler")
async def options_file_handler():
    return JSONResponse(
        content={},
        headers={
            "Access-Control-Allow-Origin": "*",
            "Access-Control-Allow-Methods": "POST, OPTIONS",
            "Access-Control-Allow-Headers": "*",
            "Access-Control-Allow-Credentials": "true"
        }
    )

@app.post("/file-handler", response_model=Dict[str, Any])
async def file_handler_endpoint(
    file: UploadFile = File(...)
):
    """
    Process a PDF file using Docling and CrewAI.
    
    Args:
        file (UploadFile): The PDF file to process
        
    Returns:
        Dict[str, Any]: The processed results including markdown content and CrewAI analysis
        
    Raises:
        HTTPException: If there's an error processing the file
    """
    temp_file_path = None
    
    try:
        logger.info(f"Received file: {file.filename} (type: {file.content_type}, size: {file.size})")
        
        # Validate file type
        if not file.content_type.startswith('application/pdf'):
            raise HTTPException(
                status_code=400, 
                detail=f"Invalid file type: {file.content_type}. Please upload a PDF file."
            )
        
        # Create a temporary file to save the uploaded PDF
        with tempfile.NamedTemporaryFile(delete=False, suffix='.pdf') as temp_file:
            # Write the uploaded file content to the temporary file
            content = await file.read()
            temp_file.write(content)
            temp_file_path = temp_file.name
            logger.info(f"Saved temporary file at: {temp_file_path}")
        
        # Process the file
        try:
            # Initialize the DocumentConverter
            logger.info("Initializing DocumentConverter")
            converter = DocumentConverter()
            
            # Convert the PDF document
            logger.info("Converting PDF document")
            docling_result = converter.convert(temp_file_path)
            
            # Get the parsed content in markdown format
            logger.info("Exporting to markdown")
            markdown_content = docling_result.document.export_to_markdown()
            
            # Process with CrewAI
            logger.info("Processing with CrewAI")
            try:
                crew_result = run(markdown_content)
                logger.info("CrewAI processing completed successfully")
            except Exception as e:
                logger.error(f"CrewAI processing failed: {str(e)}", exc_info=True)
                raise HTTPException(
                    status_code=500,
                    detail=f"CrewAI processing failed: {str(e)}"
                )
            
            # Return the results
            try:
                result_dict = crew_result.model_dump()
                logger.info("Successfully converted result to dictionary")
                return JSONResponse(
                    content={
                        "filename": file.filename,
                        "markdown": markdown_content,
                        "result": result_dict
                    },
                    headers={
                        "Access-Control-Allow-Origin": "*",
                        "Access-Control-Allow-Methods": "POST, OPTIONS",
                        "Access-Control-Allow-Headers": "*",
                        "Access-Control-Allow-Credentials": "true"
                    }
                )
            except Exception as e:
                logger.error(f"Error converting result to dictionary: {str(e)}", exc_info=True)
                raise HTTPException(
                    status_code=500,
                    detail=f"Error processing results: {str(e)}"
                )
        
        except Exception as e:
            logger.error(f"Error processing file: {str(e)}", exc_info=True)
            raise HTTPException(
                status_code=500,
                detail=f"Error processing file: {str(e)}"
            )
        finally:
            # Always clean up the temporary file
            if temp_file_path and os.path.exists(temp_file_path):
                try:
                    os.unlink(temp_file_path)
                    logger.info("Cleaned up temporary file")
                except Exception as e:
                    logger.error(f"Error cleaning up temporary file: {str(e)}")
            
    except HTTPException as e:
        # Re-raise HTTP exceptions
        raise e
    except json.JSONDecodeError as e:
        logger.error(f"JSON decode error: {str(e)}")
        raise HTTPException(status_code=400, detail=f"Invalid JSON payload: {str(e)}")
    except Exception as e:
        logger.error(f"Unexpected error in file_handler: {str(e)}", exc_info=True)
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/")
async def root():
    """Root endpoint that returns basic API information."""
    return JSONResponse(
        content={
            "message": "Welcome to the CrewAI Document Processing API",
            "endpoints": {
                "/file-handler": "POST endpoint for processing PDF files"
            }
        },
        headers={
            "Access-Control-Allow-Origin": "*",
            "Access-Control-Allow-Methods": "GET, OPTIONS",
            "Access-Control-Allow-Headers": "*",
            "Access-Control-Allow-Credentials": "true"
        }
    )

if __name__ == "__main__":
    # Use 0.0.0.0 to allow external connections
    logger.info("Starting server on 0.0.0.0:8000")
    uvicorn.run(
        "app:app",
        host="0.0.0.0",
        port=8000,
        reload=True,
        log_level="info"
    )
