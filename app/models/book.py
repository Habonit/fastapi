from sqlalchemy import Column, Integer, String
from app.models import Base



class BookModel(Base):
    __tablename__ = "books"  # Table name

    id = Column(Integer, primary_key=True, autoincrement=True)  # Primary Key
    keyword = Column(String(255), nullable=False)  # Search Keyword
    publisher = Column(String(255), nullable=False)  # Publisher
    price = Column(Integer, nullable=False)  # Price
    image = Column(String(255), nullable=True)  # Item Image