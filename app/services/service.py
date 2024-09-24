import os
from fastapi import HTTPException, UploadFile
from app.dao.dao import VideoDAO
from app.schemas.videos import VideoCreate, VideoResponse, VideoSearch
from sqlalchemy.ext.asyncio import AsyncSession
from app.core.config import async_session
import asyncio
from app.core.config import redis_cache
import asyncio
import subprocess


async def upload_video(file: UploadFile) -> VideoResponse:
    """
    Upload a video, save it to the file system, convert it to MP4 format, and store its metadata in the database.

    Args:
        file (UploadFile): The video file being uploaded.

    Returns:
        VideoResponse: Metadata of the uploaded and converted video.

    Raises:
        HTTPException: If any error occurs during upload or processing.
    """
    try:
        if not os.path.exists('videos'):
            os.makedirs('videos')
        
        file_path = f"videos/{file.filename}"
        
        with open(file_path, "wb") as buffer:
            buffer.write(file.file.read())
        
        new_path = await convert_to_mp4(file_path)
        print("new_path",new_path)
        video_create = VideoCreate(name=file.filename, size=file.size, path=new_path)
        
        async with async_session() as session:
            video_dao = VideoDAO(session)
            video = await video_dao.add_video(session, video_create)
        
        async with redis_cache as cache:
            await cache.set(f"video:{video.id}:blocked", "false")

        converted_status = "true" if new_path.endswith(".mp4") else "false"

        return VideoResponse(id=video.id, name=video.name, path=video.path, size=video.size, converted=converted_status)
    
    except Exception as e:
        print(f"Error during video upload: {e}")
        raise HTTPException(status_code=500, detail="Internal Server Error")


    
async def get_videos(search_params: VideoSearch):
    """
    Search for videos in the database based on provided filters (name, size).

    Args:
        search_params (VideoSearch): The search filters for video metadata (name and size).

    Returns:
        List[VideoResponse]: A list of videos matching the search criteria.
    """
    async with async_session() as session:
        video_dao = VideoDAO(session)
        videos = await video_dao.search_videos(session, search_params.name, search_params.size)
        return videos

async def convert_to_mp4(file_path: str) -> str:
    """
    Simulates the conversion of a video to MP4 format.

    Args:
        file_path (str): The original path of the video file.

    Returns:
        str: The new path of the converted MP4 file.

    Raises:
        Exception: If an error occurs during conversion.
    """
    new_path = file_path.rsplit('.', 1)[0] + ".mp4"
    command = ['ffmpeg', '-i', file_path, new_path]
    
    # Run the conversion command
    process = await asyncio.create_subprocess_exec(*command, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    stdout, stderr = await process.communicate()

    if process.returncode != 0:
        raise Exception(f"ffmpeg error: {stderr.decode()}")

    return new_path