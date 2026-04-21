from sqlmodel import Field, SQLModel


class FeedSourceUpdate(SQLModel):
    url: str = Field(max_length=255, nullable=True, unique=True)
    description: str = Field(max_length=255, nullable=True)
