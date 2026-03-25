from pydantic import BaseModel,HttpUrl

class ExtractionRequestSchema(BaseModel):
    url: HttpUrl

class ExtractionResponseSchema(BaseModel):
    title: str
    word_count: int
    text: str


