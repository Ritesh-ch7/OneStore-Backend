from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from src.routes.file_routes import file_router
from src.routes.dashboard import dashboard_router
from src.utils.constants import BasePaths
from src.config.logger_config import new_logger as logger
import uvicorn

app = FastAPI()

# Configure CORS to allow frontend-backend communication
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:8001"],  # Adjust for production domains
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

logger.info("Starting OneStore Application")

# Include the file and dashboard routers
app.include_router(file_router, prefix=BasePaths.FILES)
app.include_router(dashboard_router, prefix=BasePaths.DASHBOARD)

@app.get("/")
async def root():
    return {"message": "Welcome to the OneStore backend"}

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
