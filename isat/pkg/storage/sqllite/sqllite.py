from sqlalchemy import create_engine
from isat.pkg.models.image import Image
from sqlalchemy.orm import sessionmaker
import logging

log = logging.getLogger("scraper.log")


class Storage:
    def __init__(self, db_path: str):
        self.engine = create_engine(db_path, echo=True)
        self.Session = sessionmaker(bind=self.engine)
        self.session = self.Session()
        Image.metadata.create_all(self.engine)

    def add_image(self, image: Image):
        self.session.add(image)
        self.session.commit()

    def get_all_images(self):
        return self.session.query(Image).all()

    def close_session(self):
        self.session.close()
