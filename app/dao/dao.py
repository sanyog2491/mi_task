from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from app.models.models import Video
from app.schemas.videos import VideoCreate

class VideoDAO:
    def __init__(self, session: AsyncSession):
        self.session = session

    async def add_video(self, video_create: VideoCreate) -> Video:
        video = Video(
            name=video_create.name,
            size=video_create.size,
            path=video_create.path,
        )
        self.session.add(video)
        await self.session.commit()
        await self.session.refresh(video)
        return video

    async def search_videos(self, name: str = None, size: int = None):
        query = select(Video)
        if name:
            query = query.filter(Video.name.ilike(f"%{name}%"))
        if size:
            query = query.filter(Video.size == size)
        result = await self.session.execute(query)
        return result.scalars().all()