from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from app.models.models import Video
from app.schemas.videos import VideoCreate

async def add_video(session: AsyncSession, video_create: VideoCreate) -> Video:
    video = Video(name=video_create.name, size=video_create.size, path=video_create.path)
    session.add(video)
    await session.commit()
    await session.refresh(video)
    return video


async def search_videos(session: AsyncSession, name: str = None, size: int = None):
    query = select(Video)
    if name:
        query = query.filter(Video.name.ilike(f"%{name}%"))
    if size:
        query = query.filter(Video.size == size)
    result = await session.execute(query)
    return result.scalars().all()
