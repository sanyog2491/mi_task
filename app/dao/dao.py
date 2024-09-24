from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from app.models.models import Video
from app.schemas.videos import VideoCreate

class VideoDAO:
    def __init__(self, session: AsyncSession):
        self.session = session

    async def add_video(self, video_create: VideoCreate) -> Video:
        """
        Adds a new video to the database.

        Args:
            video_create (VideoCreate): A schema object containing video details (name, size, and path).

        Returns:
            Video: The newly added video record from the database.
        """
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
        """
        Searches videos in the database based on name and/or size.

        Args:
            name (str, optional): Filter by video name (partial matches allowed).
            size (int, optional): Filter by video size (exact match).

        Returns:
            List[Video]: A list of videos that match the search criteria.
        """
        query = select(Video)
        if name:
            query = query.filter(Video.name.ilike(f"%{name}%"))
        if size:
            query = query.filter(Video.size == size)
        result = await self.session.execute(query)
        return result.scalars().all()