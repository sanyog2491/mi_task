import os
from fastapi import UploadFile
from app.dao.dao import add_video, search_videos
from app.schemas.videos import VideoCreate, VideoResponse, VideoSearch
from sqlalchemy.ext.asyncio import AsyncSession
from app.core.config import async_session
import asyncio
from app.core.config import redis_cache


async def upload_video(file: UploadFile) -> VideoResponse:
    try:
        # Ensure the 'videos' directory exists
        if not os.path.exists('videos'):
            os.makedirs('videos')
        
        file_path = f"videos/{file.filename}"
        
        # Save file temporarily
        with open(file_path, "wb") as buffer:
            buffer.write(file.file.read())
        
        # Convert video asynchronously
        new_path = await convert_to_mp4(file_path)
        
        # Create a VideoCreate object
        video_create = VideoCreate(name=file.filename, size=file.size, path=new_path)
        
        # Add video to database
        async with async_session() as session:
            video = await add_video(session, video_create)
        
        # Cache logic to block video downloads
        async with redis_cache as cache:
            await cache.set(f"video:{video.id}:blocked", "false")

        return VideoResponse(name=video.name, path=video.path, size=video.size)
    
    except Exception as e:
        print(f"Error during video upload: {e}")
        raise

    
async def get_videos(search_params: VideoSearch):
    async with async_session() as session:
        videos = await search_videos(session, search_params.name, search_params.size)
        return videos

async def convert_to_mp4(file_path: str) -> str:
    try:
        await asyncio.sleep(5)  # Simulate conversion
        return file_path.replace('.mp4', ".mp4")
    except Exception as e:
        print(f"Error during conversion: {e}")
        raise