from fastapi import APIRouter, HTTPException, UploadFile
from src.services.s3_service import upload_file, download_file, get_s3_file_count
from src.dao.db_dao import add_file_metadata, increment_download_count, get_download_counts, get_all_file_metadata_with_counts
from io import BytesIO

file_router = APIRouter()

@file_router.post("/upload")
async def upload(file: UploadFile):
    file_name = file.filename
    file_content = BytesIO(await file.read())  # Read the content into BytesIO
    file_content.seek(0)  # Reset the pointer to the beginning of the BytesIO object

    # Get the size of the file in bytes
    file_size = file_content.getbuffer().nbytes
    
    # Upload the file to S3
    upload_file(file_name, file_content)

    # Add metadata after the upload
    add_file_metadata(file_name, file_size)

    return {"message": f"File {file_name} uploaded successfully with metadata"}

@file_router.get("/file_count")
async def file_count():
    count = get_s3_file_count()
    return {"total_files": count}

@file_router.get("/download/{file_name}")
async def download(file_name: str):
    # Get the response from the download_file function
    response = download_file(file_name)  # This function should return StreamingResponse
    increment_download_count(file_name)  # Increment download count after successful download

    return response

@file_router.get("/download_counts")
async def download_counts():
    return get_download_counts()

@file_router.get("/files")
async def list_files():
    # Fetch all uploaded files metadata including download counts
    files_metadata = get_all_file_metadata_with_counts()
    return files_metadata
