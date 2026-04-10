from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

db_url="mysql+pymysql://root:Dinesh%402006@localhost:3306/TODO_LIST"
engine=create_engine(db_url)
SessionLocal=sessionmaker(autocommit=False,autoflush=False,bind=engine)