from os import environ
from unittest.mock import Base
import sys
sys.path.insert(0,"app")
from fastapi import FastAPI, HTTPException, Depends
import models
import schemas
from database import engine , SessionLocal , create_tables
from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError



app = FastAPI()
create_tables()
# models.Base.metadata.create_all(bind = engine)

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()



@app.get("/")
def read_root():
    return {"message": f"App is running on port. {environ.get('SOCIAL_PORT')}"}


@app.post("/add_tenant_profiles/")
async def create_tenant_profile(tenant_profile: schemas.TenantProfileBase, db: Session = Depends(get_db)):
    db_tenant_profile = models.TenantProfile(**tenant_profile.dict())
    db.add(db_tenant_profile)
    db.commit()
    db.refresh(db_tenant_profile)
    return db_tenant_profile


@app.post("/add_user_profiles/")
async def create_user_profile(user_profile: schemas.UserProfileBase, db: Session = Depends(get_db)):

    tenant_profile = db.query(models.TenantProfile).filter(models.TenantProfile.tenant_id == user_profile.tenant_id).first()
    if tenant_profile is None:
        raise HTTPException(status_code=404, detail="Tenant with provided ID does not exist")


    db_user_profile = models.UserProfile(**user_profile.dict())
    db.add(db_user_profile)
    db.commit()
    db.refresh(db_user_profile)
    return db_user_profile


@app.get("/get_tenant_profiles/")
async def get_all_tenant_profiles(db: Session = Depends(get_db)):
    tenant_profiles = db.query(models.TenantProfile).all()
 
    if not tenant_profiles:
        raise HTTPException(status_code=404, detail="No tenant profiles found")
    return tenant_profiles


@app.get("/get_user_profiles/")
async def get_all_user_profiles(db: Session = Depends(get_db)):
    user_profiles = db.query(models.UserProfile).all()

    if not user_profiles:
        raise HTTPException(status_code=404, detail="No user profiles found")
    return user_profiles


@app.get("/tenant_profiles/{tenant_id}")
async def get_tenant_profile_by_id(tenant_id: int, db: Session = Depends(get_db)):
    tenant_profile = db.query(models.TenantProfile).filter(models.TenantProfile.tenant_id == tenant_id).first()

    if not tenant_profile:
        raise HTTPException(status_code=404, detail="Tenant profile not found")
    return tenant_profile

@app.get("/user_profiles/{user_id}")
async def get_user_profile_by_id(user_id: int, db: Session = Depends(get_db)):
    user_profile = db.query(models.UserProfile).filter(models.UserProfile.user_id == user_id).first()
    if not user_profile:
        raise HTTPException(status_code=404, detail="User profile not found")
    return user_profile



@app.delete("/delete_user_profiles/{user_id}")
async def delete_user_profile(user_id: int, db: Session = Depends(get_db)):
    user_profile = db.query(models.UserProfile).filter(models.UserProfile.user_id == user_id).first()
    if not user_profile:
        raise HTTPException(status_code=404, detail="User profile not found")

    db.delete(user_profile)
    db.commit()
    return {"message": "User profile deleted successfully"}




@app.delete("/delete_tenant_profiles/{tenant_id}")
async def delete_tenant_profile(tenant_id: int, db: Session = Depends(get_db)):
    tenant_profile = db.query(models.TenantProfile).filter(models.TenantProfile.tenant_id == tenant_id).first()
    if not tenant_profile:
        raise HTTPException(status_code=404, detail="Tenant profile not found")

    try:
        db.delete(tenant_profile)
        db.commit()
    except IntegrityError as e:
        
        raise HTTPException(status_code=400, detail="Cannot delete tenant profile because it is still referenced by other tables. You may need to delete associated user profiles first.")

    return {"message": "Tenant profile deleted successfully"}



@app.patch("/update_tenant_profile/{tenant_id}")
async def update_tenant_profile(tenant_id: int, tenant_data: schemas.TenantProfileBase, db: Session = Depends(get_db)):
  
    tenant_profile = db.query(models.TenantProfile).filter(models.TenantProfile.tenant_id == tenant_id).first()
    if not tenant_profile:
        raise HTTPException(status_code=404, detail="Tenant profile not found")

   
    for attr, value in tenant_data.dict().items():
        setattr(tenant_profile, attr, value)

    try:
        db.commit()
    except Exception as e:
        
        db.rollback()
        raise HTTPException(status_code=500, detail="Failed to update tenant profile")

    return {"message": "Tenant profile updated successfully"}


from fastapi import HTTPException

@app.patch("/update_user_profile/{user_id}")
async def update_user_profile(user_id: int, user_data: schemas.UserProfileBase, db: Session = Depends(get_db)):
    
    user_profile = db.query(models.UserProfile).filter(models.UserProfile.user_id == user_id).first()
    if not user_profile:
        raise HTTPException(status_code=404, detail="User profile not found")

  
    for attr, value in user_data.dict().items():
        setattr(user_profile, attr, value)

    try:
        db.commit()
    except Exception as e:
       
        db.rollback()
        raise HTTPException(status_code=500, detail="Failed to update user profile")

    return {"message": "User profile updated successfully"}

