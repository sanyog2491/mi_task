from fastapi import APIRouter, File, HTTPException, UploadFile
from app.schemas.videos import VideoCreate, VideoSearch, VideoResponse
from app.services.service import upload_video, get_videos, convert_to_mp4
from app.core.config import redis_cache

router = APIRouter()
print("hello world!")

@router.post("/upload/", response_model=VideoResponse)
async def upload_video_endpoint(file: UploadFile = File(...)):
    try:
        print("hello world!")
        video = await upload_video(file)
        return video
    except Exception as e:
        raise HTTPException(status_code=500, detail="Internal Server Error")


@router.get("/search/", response_model=list[VideoResponse])
async def search_videos_endpoint(search_params: VideoSearch):
    videos = await get_videos(search_params)
    return videos

@router.post("/block/")
async def block_video(video_id: int):
    await redis_cache.set(f"blocked_{video_id}", "blocked")
    return {"message": "Video blocked from downloading."}

@router.get("/download/{video_id}")
async def download_video(video_id: int):
    blocked = await redis_cache.get(f"blocked_{video_id}")
    if blocked:
        raise HTTPException(status_code=403, detail="Video is blocked for download.")
    # Proceed with download logic
    return {"message": "Video download started."}
