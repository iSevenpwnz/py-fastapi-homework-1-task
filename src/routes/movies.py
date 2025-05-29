import math

from fastapi import APIRouter, Depends, HTTPException, Query, status, Request
from sqlalchemy import select, func
from sqlalchemy.ext.asyncio import AsyncSession

from database import get_db, MovieModel
from schemas import MovieListResponseSchema, MovieDetailResponseSchema

router = APIRouter()


@router.get("/movies/, response_model=MovieListResponseSchema")
async def get_movie_list(
        request: Request,
        db: AsyncSession = Depends(get_db),
        page: int = Query(default=1, ge=1),
        per_page: int = Query(default=10, ge=1, le=20)
) -> MovieListResponseSchema:
    result = await db.execute(select(func.count(MovieModel.id)))
    total_items = result.scalar()
    if not total_items:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="No movies found.")
    total_pages = math.ceil(total_items / per_page)
    offset = (page - 1) * per_page
    result = await db.scalars(select(MovieModel).offset(offset).limit(per_page))
    movies = result.all()
    if not movies:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="No movies found.")
    base_url = request.url.path
    prev_page = (
        f"{base_url}?page={page - 1}&per_page={per_page}" if page > 1 else None
    )
    next_page = (
        f"{base_url}?page={page + 1}&per_page={per_page}" if page < total_pages else None
    )
    return MovieListResponseSchema(
        movies=movies,
        prev_page=prev_page,
        next_page=next_page,
        total_pages=total_pages,
        total_items=total_items
    )


@router.get("/movies/{movie_id}/", response_model=MovieDetailResponseSchema)
async def get_movie_by_id(movie_id: int, db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(MovieModel).where(MovieModel.id == movie_id))
    movie = result.scalar_one_or_none()
    if not movie:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Movie with the given ID was not found.")
    return MovieDetailResponseSchema.model_validate(movie)
