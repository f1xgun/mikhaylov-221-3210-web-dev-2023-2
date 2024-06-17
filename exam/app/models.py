import os
from typing import Optional
from datetime import datetime
from sqlalchemy.dialects.mysql import YEAR
from werkzeug.security import check_password_hash, generate_password_hash
from flask_login import UserMixin
from flask import url_for
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import DeclarativeBase
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import String, ForeignKey, Text, Integer, MetaData, Column, Table


class Base(DeclarativeBase):
    metadata = MetaData(naming_convention={
        "ix": 'ix_%(column_0_label)s',
        "uq": "uq_%(table_name)s_%(column_0_name)s",
        "ck": "ck_%(table_name)s_%(constraint_name)s",
        "fk": "fk_%(table_name)s_%(column_0_name)s_%(referred_table_name)s",
        "pk": "pk_%(table_name)s"
    })


db = SQLAlchemy(model_class=Base)

books_genres = Table(
    'books_genres',
    Base.metadata,
    Column('book_id', Integer, ForeignKey('books.id', ondelete="CASCADE"), primary_key=True),
    Column('genre_id', Integer, ForeignKey('genres.id', ondelete="CASCADE"), primary_key=True)
)


class Genre(Base):
    __tablename__ = 'genres'

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    name: Mapped[str] = mapped_column(String(50), nullable=False, unique=True)
    books: Mapped[list["Book"]] = relationship("Book", secondary=books_genres, back_populates="genres")

    def __repr__(self):
        return f'<Genre {self.name}>'


class Role(Base):
    __tablename__ = 'roles'

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    name: Mapped[str] = mapped_column(String(50), nullable=False, unique=True)
    description: Mapped[str] = mapped_column(Text, nullable=False)

    users: Mapped[list["User"]] = relationship("User", back_populates="role")

    def __repr__(self):
        return f'<Role {self.name}>'


class User(Base, UserMixin):
    __tablename__ = 'users'

    id: Mapped[int] = mapped_column(primary_key=True)
    login: Mapped[str] = mapped_column(String(100), unique=True)
    password_hash: Mapped[str] = mapped_column(String(200), nullable=False)
    last_name: Mapped[str] = mapped_column(String(100), nullable=False)
    first_name: Mapped[str] = mapped_column(String(100), nullable=False)
    middle_name: Mapped[Optional[str]] = mapped_column(String(100))
    role_id: Mapped[int] = mapped_column(ForeignKey("roles.id"), nullable=False)
    role: Mapped[Role] = relationship("Role", back_populates="users")

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

    @property
    def full_name(self):
        return ' '.join([self.last_name, self.first_name, self.middle_name or ''])

    def __repr__(self):
        return '<User %r>' % self.login

    def is_admin(self):
        return self.role.name == USER_ROLES[0]

    def is_moderator(self):
        return self.role.name == USER_ROLES[1]

    def is_user(self):
        return self.role.name == USER_ROLES[2]


class Book(Base):
    __tablename__ = 'books'

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    name: Mapped[str] = mapped_column(String(100), nullable=False)
    short_desc: Mapped[str] = mapped_column(Text, nullable=False)
    year: Mapped[int] = mapped_column(YEAR, nullable=False)
    publisher: Mapped[str] = mapped_column(String(100), nullable=False)
    author: Mapped[str] = mapped_column(String(100), nullable=False)
    pages_count: Mapped[int] = mapped_column(nullable=False)

    cover_image_id: Mapped[int] = mapped_column(ForeignKey("images.id"), nullable=False)

    created_at: Mapped[datetime] = mapped_column(default=datetime.now, nullable=False)

    cover_image: Mapped["Image"] = relationship("Image")
    genres: Mapped[list["Genre"]] = relationship("Genre", secondary=books_genres, back_populates="books")
    reviews: Mapped[list["Review"]] = relationship("Review", back_populates="book", cascade="all, delete")

    def __repr__(self):
        return f'<Book {self.name} {self.genres}>'

    def rating(self):
        if self.reviews:
            total_rating = sum(review.rating for review in self.reviews)
            average_rating = total_rating / len(self.reviews)
            return average_rating
        return 0


class Image(db.Model):
    __tablename__ = 'images'

    id: Mapped[str] = mapped_column(String(100), primary_key=True)
    file_name: Mapped[str] = mapped_column(String(100), nullable=False)
    mime_type: Mapped[str] = mapped_column(String(100), nullable=False)
    md5_hash: Mapped[str] = mapped_column(String(100), unique=True, nullable=False)

    def __repr__(self):
        return '<Image %r>' % self.file_name

    @property
    def storage_filename(self):
        _, ext = os.path.splitext(self.file_name)
        return self.id + ext

    @property
    def url(self):
        return url_for('image', image_id=self.id)


class Review(Base):
    __tablename__ = 'reviews'

    id: Mapped[int] = mapped_column(primary_key=True)
    book_id: Mapped[int] = mapped_column(ForeignKey("books.id", ondelete="CASCADE"))
    user_id: Mapped[int] = mapped_column(ForeignKey("users.id"))
    rating: Mapped[int] = mapped_column(default=5)
    text: Mapped[str] = mapped_column(Text)
    created_at: Mapped[datetime] = mapped_column(default=datetime.now)

    book: Mapped["Book"] = relationship()
    user: Mapped["User"] = relationship()

    def __repr__(self):
        return '<Review %r>' % self.text

    def get_rating_str(self):
        return REVIEW_GRADES[self.rating]


REVIEW_GRADES = [
    "Ужасно",
    "Плохо",
    "Неудовлетворительно",
    "Удовлетворительно",
    "Хорошо",
    "Отлично",
]

USER_ROLES = [
    "Администратор",
    "Модератор",
    "Пользователь"
]
