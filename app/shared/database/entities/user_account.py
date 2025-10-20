from sqlalchemy import Column, Date, DateTime, Integer, String, text
from sqlalchemy.dialects.postgresql import UUID

from ..database import Base

class UserAccount(Base):
    __tablename__ = "user_account"

    pk_uuid = Column(UUID(as_uuid=True), primary_key=True, server_default=text("uuid_generate_v4()"))
    created_at = Column(DateTime, nullable=False, server_default=text("current_timestamp"))
    changed_at = Column(DateTime, nullable=True)
    deactivated_at = Column(DateTime, nullable=True)

    name = Column(String(100), nullable=False)
    email = Column(String(100), unique=True, nullable=False)
    password = Column(String(100), nullable=False)
    date_of_birth = Column(Date, nullable=False)

    gender_id = Column(Integer, nullable=False)
    user_manager_uuid = Column(UUID(as_uuid=True), nullable=True)
    factory_id = Column(Integer, nullable=False)