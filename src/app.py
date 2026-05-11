from sqlalchemy import select
import shutil

import uuid

from fastapi import FastAPI, HTTPException, File, UploadFile, Form, Depends
from src.schema import Postcreate
from src.db import Post, create_db_and_tables, get_async_session
from sqlalchemy.ext.asyncio import AsyncSession
from contextlib import asynccontextmanager
from src.image import imagekit

import os
import tempfile


@asynccontextmanager
async def lifespan(app: FastAPI):
    await create_db_and_tables()
    yield


app = FastAPI(lifespan=lifespan)


@app.post("/upload")
async def upload_file(
    file: UploadFile = File(...),
    caption: str = Form(""),
    session: AsyncSession = Depends(get_async_session)
):
    temp_file_path = None

    try:
        content = await file.read()

        suffix = os.path.splitext(file.filename)[1] if file.filename else ""

        with tempfile.NamedTemporaryFile(delete=False, suffix=suffix) as temp_file:
            temp_file_path = temp_file.name
            temp_file.write(content) 

  
        with open(temp_file_path, "rb") as f:
            upload_res = imagekit.files.upload(
                file=f,
                file_name=file.filename or f"upload{suffix}",
                use_unique_file_name=True,
                tags=["fastapi-upload"]
            )

        url = upload_res.url
        image_name = upload_res.name


        post = Post(
            caption=caption,
            url=url,
            file_name=image_name,
            file_type="video" if file.content_type.startswith("video/") else "image",
        )
        session.add(post)
        await session.commit()
        await session.refresh(post)
        return post

    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    finally:
        if temp_file_path and os.path.exists(temp_file_path):
            os.unlink(temp_file_path)


@app.get("/feed")
async def get_feed(
    session: AsyncSession = Depends(get_async_session)
):
    result = await session.execute(select(Post).order_by(Post.created_at.desc()))
    posts = [row[0] for row in result.all()]

    posts_data = [
        {
            "id": str(post.id),
            "caption": post.caption,
            "url": post.url,
            "file_type": post.file_type,
            "file_name": post.file_name,
            "created_at": post.created_at.isoformat()
        }
        for post in posts
    ]

    return {"posts": posts_data}


@app.delete("/posts/{post_id}")
async def delete_post(post_id: str, session: AsyncSession = Depends(get_async_session)):
    try:
        post_uuid = uuid.UUID(post_id)  # raises ValueError if invalid UUID
    except ValueError:
        raise HTTPException(status_code=400, detail="Invalid post ID format")

    result = await session.execute(select(Post).where(Post.id == post_uuid))
    post = result.scalars().first()

    if not post:
        raise HTTPException(status_code=404, detail="Post not found")

    try:
        await session.delete(post)
        await session.commit()
        return {"success": True, "message": "Post deleted successfully"}
    except Exception as e:
        await session.rollback()
        raise HTTPException(status_code=500, detail=str(e))