from sqlmodel import create_engine, Session

DATABASE_URL = "mysql+pymysql://root@localhost/2025_M1"
engine = create_engine(DATABASE_URL, echo=True)

def get_session():
    with Session(engine) as session:
        yield session
