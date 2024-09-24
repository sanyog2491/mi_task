from fastapi import APIRouter, File, HTTPException, UploadFile,Query
from app.schemas.videos import VideoCreate, VideoSearch, VideoResponse
from app.services.service import upload_video, get_videos, convert_to_mp4
from app.core.config import redis_cache
from typing import Optional
from pydantic import BaseModel

router = APIRouter()
print("hello world!")

@router.post("/upload/", response_model=VideoResponse)
async def upload_video_endpoint(file: UploadFile = File(...)):
    """
    Endpoint to upload a video file. The video is processed 
    and stored, then a response with video details is returned.

    Args:
        file (UploadFile): The video file being uploaded.

    Returns:
        VideoResponse: Details of the uploaded video.
    """
    try:
        print("hello world!")
        video = await upload_video(file)
        return video
    except Exception as e:
        raise HTTPException(status_code=500, detail="Internal Server Error")


@router.get("/search/", response_model=list[VideoResponse])
async def search_videos_endpoint(
    name: Optional[str] = Query(None, description="Filter videos by name"),
    size: Optional[int] = Query(None, description="Filter videos by size")
):
    """
    Endpoint to search for videos based on optional name and size filters.

    Args:
        name (Optional[str]): Name filter for the video.
        size (Optional[int]): Size filter for the video in bytes.

    Returns:
        list[VideoResponse]: List of videos matching the search criteria.
    """
    search_params = VideoSearch(name=name, size=size)
    videos = await get_videos(search_params)
    return videos

class BlockVideoRequest(BaseModel):
    video_id: int

@router.post("/block/")
async def block_video(request: BlockVideoRequest):
    """
    Endpoint to block a video from being downloaded by adding it 
    to the blocklist in the Redis cache.

    Args:
        request (BlockVideoRequest): The video ID to be blocked.

    Returns:
        dict: Confirmation message.
    """
    await redis_cache.set(f"blocked_{request.video_id}", "blocked")
    return {"message": "Video blocked from downloading."}

@router.get("/download/{video_id}")
async def download_video(video_id: int):
    """
    Endpoint to download a video if it is not blocked.
    
    Args:
        video_id (int): ID of the video to be downloaded.

    Raises:
        HTTPException: If the video is blocked.

    Returns:
        dict: Confirmation message indicating the download started.
    """
    blocked = await redis_cache.get(f"blocked_{video_id}")
    if blocked:
        raise HTTPException(status_code=403, detail="Video is blocked for download.")
    return {"message": "Video download started."}

@router.post("/unblock/")
async def unblock_video(request: BlockVideoRequest):
    """
    Endpoint to unblock a video by removing it from the blocklist 
    in the Redis cache.

    Args:
        request (BlockVideoRequest): The video ID to be unblocked.

    Raises:
        HTTPException: If the video ID is not found in the blocklist.

    Returns:
        dict: Confirmation message indicating the video was successfully unblocked.
    """
    key = f"blocked_{request.video_id}"
    if await redis_cache.get(key):
        await redis_cache.delete(key)
        return {"message": "Video unblocked successfully."}
    else:
        raise HTTPException(status_code=404, detail="Video ID not found in blocklist.")
