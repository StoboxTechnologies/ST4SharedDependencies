from pydantic import BaseModel


class UserFeatureConsumeSchema(BaseModel):
    user_id: int
    feature_name: str
