from sqlalchemy import Column, Integer, String, Date
from app.core.database import Base


class Phone(Base):
    __tablename__ = "phones"

    id = Column(Integer, primary_key=True, index=True)
    model_name = Column(String, nullable=False, index=True)
    release_date = Column(String)

    display = Column(String)
    battery = Column(Integer)

    camera = Column(String)
    ram = Column(String)
    storage = Column(String)

    price = Column(Integer)

    def __repr__(self):
        return f"<Phone(model_name={self.model_name})>"
