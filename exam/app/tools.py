import hashlib
import uuid
import os
from enum import Enum

from sqlalchemy.orm import contains_eager
from werkzeug.utils import secure_filename
from flask import current_app
from models import db, Image, Review, Book, Genre


class BooksFilter:
    def __init__(self, name, genre_ids):
        self.name = name
        self.genre_ids = genre_ids
        self.query = db.session.query(Book).outerjoin(Book.genres)

    def perform(self):
        self.__filter_by_name()
        self.__filter_by_genre_ids()
        return self.query.order_by(Book.year.desc())

    def __filter_by_name(self):
        if self.name:
            self.query = self.query.filter(
                Book.name.ilike('%' + self.name + '%'))

    def __filter_by_genre_ids(self):
        if self.genre_ids:
            self.query = self.query.filter(
                Genre.id.in_(self.genre_ids)).options(contains_eager(Book.genres))


class ImageSaver:
    def __init__(self, file):
        self.file = file

    def save(self):
        self.img = self.__find_by_md5_hash()
        if self.img is not None:
            return self.img
        file_name = secure_filename(self.file.filename)
        self.img = Image(
            id=str(uuid.uuid4()),
            file_name=file_name,
            mime_type=self.file.mimetype,
            md5_hash=self.md5_hash)
        self.file.save(
            os.path.join(current_app.config['UPLOAD_FOLDER'],
                         self.img.storage_filename))
        db.session.add(self.img)
        db.session.commit()
        return self.img

    def __find_by_md5_hash(self):
        self.md5_hash = hashlib.md5(self.file.read()).hexdigest()
        self.file.seek(0)
        return db.session.execute(db.select(Image).filter(Image.md5_hash == self.md5_hash)).scalar()