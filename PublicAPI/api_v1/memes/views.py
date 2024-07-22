import base64
from json import dumps
from fastapi import APIRouter, File, Form, Response, UploadFile, status, Depends
from typing import Optional
from sqlalchemy.ext.asyncio import AsyncSession
from fastapi.responses import JSONResponse
from io import BytesIO

import zipfile

from .shemas import Meme, MemeCreate, MemeUpdate, MemeUpdatePartitial
from .dependencies import get_pagination_params, meme_by_id

from . import crud
from core.models import db_helper
from core.ext import download_file, upload_file, delete_file


router = APIRouter(tags=["Memes"])


@router.get("/", response_model=list[Meme])
async def get_memes(
    pagination: dict = Depends(get_pagination_params),
    session: AsyncSession = Depends(db_helper.session_dependency),

):
    offset = pagination["offset"]
    limit = pagination["limit"]

    memes: list[Meme] = await crud.get_memes(
        session=session,
        offset=offset,
        limit=limit,
    )

    images: list[tuple[str, bytes]] = [
        (meme.filename, await download_file(meme.filename))
        for meme in memes
    ]

    zip_buffer = BytesIO()
    with zipfile.ZipFile(zip_buffer, 'w') as zip_file:
        for filename, image in images:
            zip_file.writestr(filename, image)

    zip_buffer.seek(0)

    json_data = [
        {
            "id": meme.id,
            "description": meme.description,
            "filename": meme.filename
        }
        for meme in memes
    ]

    json_str = dumps(json_data)
    json_base64 = base64.b64encode(json_str.encode("utf-8")).decode("utf-8")

    headers = {
        "Content-Disposition": "attachment; filename=memes.zip",
        "X-JSON-Data": json_base64,
        # "X-JSON-Data": JSONResponse(json_data).body.decode("utf-8"),
        "X-Total-Count": str(len(images)),
        "X-Offset": str(offset),
        "X-Limit": str(limit)
    }

    return Response(
        content=zip_buffer.getvalue(),
        headers=headers,
        media_type="application/zip"
    )


@router.get("/{meme_id}", response_model=Meme)
async def get_meme(
    meme: Meme = Depends(meme_by_id)
):
    image = await download_file(meme.filename)
    if image is not None:
        headers = {
            "Content-Disposition": f"attachment; filename={meme.filename}",
            "X-JSON-Data": JSONResponse({
                "id": meme.id,
                "descriprion": meme.description,
                "filename": meme.filename,
            }).body.decode("utf-8")
        }

        return Response(
            content=image,
            headers=headers,
            media_type="application/octet-stream"
        )
    

@router.post("/", response_model=Meme)
async def create_meme(
    image: UploadFile,
    description: str = Form(...),
    session: AsyncSession = Depends(db_helper.session_dependency),
):
    meme_in = MemeCreate(
        description=description,
        filename=image.filename
    )
    await upload_file(image.file.read(), image.filename)
    meme: Meme = await crud.create_meme(session, meme_in)
    return meme


@router.put("/{meme_id}")
async def update_meme(
    image: UploadFile,
    description: str,
    # meme_update: MemeUpdate,
    meme: Meme = Depends(meme_by_id),
    session: AsyncSession = Depends(db_helper.session_dependency)
):
    meme_update = MemeUpdate(
        description=description,
        filename=image.filename
    )
    await delete_file(meme.filename)
    await upload_file(image.file.read(), image.filename)
    return await crud.update_meme(
        session=session,
        meme=meme,
        meme_update=meme_update,
    )


@router.patch("/{meme_id}")
async def update_meme_partial(
    image: UploadFile = File(None),
    description: str | None = None,
    meme: Meme = Depends(meme_by_id),
    session: AsyncSession = Depends(db_helper.session_dependency)
):
    meme_update = MemeUpdatePartitial(
        description=description,
        filename=image.filename if image is not None else None
    )

    if image is not None:
        await delete_file(meme.filename)
        await upload_file(image.file.read(), image.filename)
        meme_update.filename = image.filename
    return await crud.update_meme(
        session=session,
        meme=meme,
        meme_update=meme_update,
        partial=True
    )


@router.delete("/{meme_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_meme(
    meme: Meme = Depends(meme_by_id),
    session: AsyncSession = Depends(db_helper.session_dependency),
) -> None:
    await delete_file(meme.filename)
    await crud.delete_meme(session=session, meme=meme)