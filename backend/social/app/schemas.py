from pydantic import BaseModel
from typing import List, Annotated , Optional

class UserProfileBase(BaseModel):
    user_id: int
    first_name: str
    last_name: str
    department: str
    designation: str
    tenant_id: int
    image_url: str
    city: str
    country: str
    bio: str
    social_links: Optional[dict]
    employee_id: int


class TenantProfileBase(BaseModel):
    tenant_id: int
    tenant_name: str
    address: str
    city: str
    state: Optional[str]
    country: str
    zip_code: str
    phone: str
    web_url: str