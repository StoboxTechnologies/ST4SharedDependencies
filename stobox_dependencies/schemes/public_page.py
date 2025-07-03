from pydantic import BaseModel


class PublicPageInfo(BaseModel):
    company_id: int
