from sqlalchemy import Column, Integer, String, JSON , ForeignKey
# from database import Base
from sqlalchemy.ext.declarative import declarative_base


Base = declarative_base()

class TenantProfile(Base):
    __tablename__ = "tenant_profile"

    tenant_id = Column(Integer, primary_key=True)
    tenant_name = Column(String(255), nullable=False)
    address = Column(String(255), nullable=False)
    city = Column(String(255), nullable=False)
    state = Column(String(255), nullable=True)
    country = Column(String(255), nullable=False)
    zip_code = Column(String(255), nullable=False)
    phone = Column(String(255), nullable=False)
    web_url = Column(String(255), nullable=False)

class UserProfile(Base):
    __tablename__ = "user_profile"

    user_id = Column(Integer, primary_key=True)
    first_name = Column(String(255), nullable=False)
    last_name = Column(String(255), nullable=False)
    department = Column(String(255), nullable=False)
    designation = Column(String(255), nullable=False)
    tenant_id = Column(Integer, ForeignKey("tenant_profile.tenant_id"),nullable=False)
    image_url = Column(String(255), nullable=False)
    city = Column(String(255), nullable=False)
    country = Column(String(255), nullable=False)
    bio = Column(String(255), nullable=False)
    social_links = Column(JSON)
    employee_id = Column(Integer, nullable=False)
