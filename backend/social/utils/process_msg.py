from app.models import TenantProfile
from app.database import engine, SessionLocal
import app.schemas as schemas
from sqlalchemy.orm import Session
from pydantic import ValidationError




# Function to create and save tenant profile
def create_tenant_profile(db: Session, tenant_profile: schemas.TenantProfileBase):
    try:
        db_tenant_profile = TenantProfile(**tenant_profile.dict())
        db.add(db_tenant_profile)
        db.commit()
        db.refresh(db_tenant_profile)
      
        return db_tenant_profile
    except ValidationError as e:
        raise e
    



def process_msg(msg):
    db = SessionLocal()
    try:
        tenant_data = schemas.TenantProfileBase(**msg)
        created_profile = create_tenant_profile(db, tenant_data)
        print("Tenant Profile created successfully:", created_profile)
    except ValidationError as e:
        print("Validation Error:", e)
    