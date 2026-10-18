from sqlalchemy import Column, Integer, String
from database import Base


class DBAsset(Base):
    __tablename__ = "assets"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True)
    asset_type = Column(String)
    ip_address = Column(String)
    port = Column(Integer)

class DBUser(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    username = Column(String, unique=True, index=True)
    hashed_password = Column(String)