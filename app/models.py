# app/models.py

from sqlalchemy import Column, String, DateTime
from datetime import datetime, timezone

# import Base from database.py — our model inherits from it
# which registers it as a database table
from app.database import Base

# each class here = one table in the database
# each class attribute = one column in that table
class URL(Base):

    # the name of the table in the database
    __tablename__ = "urls"

    # the short code — e.g. "abc123"
    # primary_key=True means this is the unique identifier for each row
    # index=True makes lookups by short_code fast
    short_code = Column(String, primary_key=True, index=True)

    # the original long URL the user submitted
    original_url = Column(String, nullable=False)

    # when this short URL was created — defaults to now
    created_at = Column(DateTime, default=lambda: datetime.now(timezone.utc))