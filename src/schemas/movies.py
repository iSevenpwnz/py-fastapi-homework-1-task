from datetime import date

from pydantic import BaseModel, ConfigDict


class BaseMovieSchema(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    name: str
    date: date
    score: float
    genre: str
    overview: str
    crew: str
    orig_title: str
    status: str
    orig_lang: str
    budget: float
    revenue: float
    country: str


class MovieDetailResponseSchema(BaseMovieSchema):
    id: int


class MovieListResponseSchema(BaseModel):
    model_config = ConfigDict(
        from_attributes=True,
        json_schema_extra={
            "examples": [
                {
                    "movies": [
                        {
                            "id": 1,
                            "name": "Creed III",
                            "date": "2023-03-02",
                            "score": 73,
                            "genre": "Drama,Action",
                            "overview": "After dominating the boxing world, Adonis Creed has been thriving in both "
                                        "his career and family life...",
                            "crew": "Michael B. Jordan, Tessa Thompson",
                            "orig_title": "Creed III",
                            "status": "Released",
                            "orig_lang": "English",
                            "budget": 75000000,
                            "revenue": 271616668,
                            "country": "AU"
                        }
                    ],
                    "prev_page": "/theater/movies/?page=1&per_page=10",
                    "next_page": "/theater/movies/?page=3&per_page=10",
                    "total_pages": 1000,
                    "total_items": 9999
                }
            ]
        }
    )
    movies: list[MovieDetailResponseSchema]
    prev_page: str | None = None
    next_page: str | None = None
    total_pages: int
    total_items: int
