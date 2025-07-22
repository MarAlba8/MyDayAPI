from uuid import UUID
from loguru import logger
from sqlalchemy import select
from sqlalchemy.exc import NoResultFound

from database.models.post import Post
from schemas.post import PostSchema


class PostService:
    def __init__(self, session):
        self.session = session

    def create(self, post: PostSchema):
        logger.info("Creating post")
        post = Post(**post.model_dump())
        self.session.add(post)
        self.session.commit()
        self.session.refresh(post)
        return post

    def get_by_id(self, post_uuid: UUID):
        logger.info("Getting post")
        query = select(Post).where(Post.id == post_uuid)
        post = self.session.execute(query).scalars().first()

        if not post:
            raise NoResultFound(f"Not post found with id: {(post_uuid)}")

        return post

    def get_all(self):
        query = select(Post)
        return self.session.execute(query).scalars().all()
