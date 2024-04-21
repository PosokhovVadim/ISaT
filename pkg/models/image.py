from sqlalchemy import Column, String
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()


class Image(Base):
    __tablename__ = "image"

    id = Column(String, primary_key=True)
    url = Column(String, nullable=False)
    local_path = Column(String, nullable=False)
    lab_color = Column([float, float, float], nullable=False, default=[0, 0, 0])
    hsv_color = Column([float, float, float], nullable=False, default=[0, 0, 0])

    # add tensor
    def __init__(self, id: str, url: str, local_path: str):
        self.id = id
        self.url = url
        self.local_path = local_path
