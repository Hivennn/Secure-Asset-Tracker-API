from sqlalchemy import create_engine
from sqlalchemy.orm import declarative_base, sessionmaker

# Point to a file named 'app.db' inside your current directory
SQLALCHEMY_DATABASE_URL = "sqlite:///./app.db"

# Create the connection engine (connect__args is only required for SQLite)
engine = create_engine(
    SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False}
)

# Create a Session factory to handle transactions
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Create a Base class that our database tables will inherit from
Base = declarative_base()


# Helper function to open and close database connections automatically
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
