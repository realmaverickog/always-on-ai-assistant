from pydantic import BaseModel


class MockDataType(BaseModel):
    id: str
    name: str
