# app/database.py

# SQLAlchemy is an ORM (Object Relational Mapper) — it lets us interact
# with the database using Python objects instead of writing raw SQL
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

# SQLite is a lightweight database that lives in a single file on disk
# no installation or setup needed — SQLAlchemy creates the file automatically
# the /// means relative path — so this creates url_shortener.db in your project root
DATABASE_URL = "sqlite:///./url_shortener.db"

# the engine is the core connection to the database
# connect_args is needed for SQLite specifically to allow multiple threads
engine = create_engine(
    DATABASE_URL,
    connect_args={"check_same_thread": False}
)

# a SessionLocal is a factory for database sessions
# each request gets its own session — think of it like a temporary workspace
# for reading and writing to the database
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Base is the parent class all our database models will inherit from
# it keeps track of all the tables we define
Base = declarative_base()

# this is a dependency — FastAPI will call this function to get a database
# session for each request, and automatically close it when the request is done
def get_db():
    db = SessionLocal()
    try:
        yield db      # hand the session to the route that needs it
    finally:
        db.close()    # always close the session when done, even if an error occurred