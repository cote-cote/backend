from datetime import datetime

from pydantic import BaseModel, Field


class CoteResponse(BaseModel):
    cote_id: str = Field(alias='id')
    cote_name: str = Field(alias='name')
    cote_problem_url: str = Field(alias='problem_url')
    cote_capacity: int = Field(alias='capacity')
    cote_created_date: datetime = Field(alias='created_at')
    cote_updated_date: datetime = Field(alias='updated_at')

    class Config:
        from_attributes = True
        populate_by_name = True
        revalidate_instances = 'always'
