import os
from fastapi import UploadFile
from app.dao.dao import add_video, search_videos
from app.schemas.videos import VideoCreate, VideoResponse, VideoSearch
from sqlalchemy.ext.asyncio import AsyncSession
from app.core.config import async_session
import asyncio
from app.core.config import redis_cache
import asyncio
import subprocess


async def upload_video(file: UploadFile) -> VideoResponse:
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
            video = await add_video(session, video_create)
        
        async with redis_cache as cache:
            await cache.set(f"video:{video.id}:blocked", "false")

        # Assuming `converted` is a field you want to include, you need to set it correctly
        converted_status = "true" if new_path.endswith(".mp4") else "false"

        return VideoResponse(id=video.id, name=video.name, path=video.path, size=video.size, converted=converted_status)
    
    except Exception as e:
        print(f"Error during video upload: {e}")
        raise HTTPException(status_code=500, detail="Internal Server Error")


    
async def get_videos(search_params: VideoSearch):
    async with async_session() as session:
        videos = await search_videos(session, search_params.name, search_params.size)
        return videos

async def convert_to_mp4(file_path: str) -> str:
    new_path = file_path.rsplit('.', 1)[0] + ".mp4"
    command = ['ffmpeg', '-i', file_path, new_path]
    
    # Run the conversion command
    process = await asyncio.create_subprocess_exec(*command, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    stdout, stderr = await process.communicate()

    if process.returncode != 0:
        raise Exception(f"ffmpeg error: {stderr.decode()}")

    return new_path