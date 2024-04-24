from sqlalchemy import create_engine
from pkg.models.image import Image
from sqlalchemy.orm import sessionmaker
from typing import List


class Storage:
    def __init__(self, db_path: str):
        self.engine = create_engine(db_path, echo=True)
        self.Session = sessionmaker(bind=self.engine)
        self.session = self.Session()
        Image.metadata.create_all(self.engine)

    def add_images(self, images: List[Image]):
        self.session.add_all(images)
        self.session.commit()

    def get_all_images(self):
        return self.session.query(Image).all()

    def open_sessions(self):
        return self.session

    def close_session(self):
        self.session.close()

    def update_colors(self, id, lab_color, hsv_colors):
        update_data = {
            "lab_color_1": lab_color[0],
            "lab_color_2": lab_color[1],
            "lab_color_3": lab_color[2],
            "hsv_color_1": hsv_colors[0],
            "hsv_color_2": hsv_colors[1],
            "hsv_color_3": hsv_colors[2],
        }
        self.session.query(Image).filter(Image.id == id).update(update_data)
        self.session.commit()

    def update_tensor(self, id, tensor):
        self.session.query(Image).filter(Image.id == id).update({"tensor": tensor})
        self.session.commit()

    def get_image_by_id(self, id):
        return self.session.query(Image).filter(Image.id == id).first()

    def get_all_lab_colors(self):
        return self.session.query(
            Image.id, Image.url, Image.lab_color_1, Image.lab_color_2, Image.lab_color_3
        ).all()

    def get_all_hsv_colors(self):
        return self.session.query(
            Image.id, Image.url, Image.hsv_color_1, Image.hsv_color_2, Image.hsv_color_3
        ).all()
