from fastapi import APIRouter
from src.dao.db_dao import get_download_counts, get_upload_counts
from src.services.s3_service import get_s3_file_count

dashboard_router = APIRouter()

@dashboard_router.get("/")
async def dashboard():
    total_files = get_s3_file_count()  # Get the total files from S3
    total_downloads = get_download_counts()  # Now returns total downloads
    total_uploads = get_upload_counts()  # Ensure this function is defined

    return {
        "total_files": total_files,
        "total_uploads": total_uploads,  # Include total uploads in the response
        "total_downloads": total_downloads  # Include total downloads in the response
    }
