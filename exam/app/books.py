from flask import Blueprint, render_template, request, flash, redirect, url_for
from flask_login import login_required, current_user
from sqlalchemy import desc
from sqlalchemy.exc import IntegrityError, DataError

from check_rights_decorator import check_rights
from models import db, User, Review, REVIEW_GRADES, Genre, Book
from tools import ImageSaver, BooksFilter

bp = Blueprint('books', __name__, url_prefix='/books')

BOOK_PARAMS = [
    'name', 'short_desc', 'year', 'publisher', 'author', 'pages_count'
]


def params():
    return {p: request.form.get(p) or None for p in BOOK_PARAMS}


def search_params():
    return {
        'name': request.args.get('name'),
        'genre_ids': [x for x in request.args.getlist('genre_ids') if x],
    }


@bp.route('/')
def index():
    books = BooksFilter(**search_params()).perform()
    pagination = db.paginate(books)
    books = pagination.items
    genres = db.session.execute(db.select(Genre)).scalars()
    return render_template('books/index.html',
                           books=books,
                           genres=genres,
                           pagination=pagination,
                           search_params=search_params())


@bp.route('/new')
@login_required
@check_rights(need_admin_role=True)
def new():
    book = Book()
    genres = db.session.execute(db.select(Genre)).scalars()
    users = db.session.execute(db.select(User)).scalars()
    return render_template('books/new.html',
                           genres=genres,
                           users=users,
                           book=book)


@bp.route('/create', methods=['POST'])
@login_required
@check_rights(need_admin_role=True)
def create():
    f = request.files.get('cover_img')
    genres_ids = request.form.getlist('genres_id')
    img = None
    book = Book()
    try:
        if f and f.filename:
            img = ImageSaver(f).save()

        image_id = img.id if img else None
        book = Book(**params(), cover_image_id=image_id)
        genres = db.session.query(Genre).filter(Genre.id.in_(genres_ids)).all()
        book.genres = genres
        db.session.add(book)
        db.session.commit()
    except IntegrityError as err:
        flash(f'Возникла ошибка при записи данных в БД. Проверьте корректность введённых данных. ({err})', 'danger')
        db.session.rollback()
        genres = db.session.execute(db.select(Genre)).scalars()
        users = db.session.execute(db.select(User)).scalars()
        return render_template('books/new.html',
                               genres=genres,
                               users=users,
                               book=book)
    except DataError as err:
        flash(f'Возникла ошибка при записи данных в БД. Проверьте корректность введённых данных. ({err})', 'danger')
        db.session.rollback()
        genres = db.session.execute(db.select(Genre)).scalars()
        users = db.session.execute(db.select(User)).scalars()
        return render_template('books/new.html',
                               genres=genres,
                               users=users,
                               book=book)

    flash(f'Книга {book.name} был успешно добавлен!', 'success')

    return redirect(url_for('books.index'))


@bp.route("<int:book_id>/book/edit", methods=["POST", "GET"])
@login_required
@check_rights(need_moderator_role=True)
def edit_book(book_id):
    book = db.session.execute(
        db.select(Book).filter_by(id=book_id)).scalar_one_or_none()
    if request.method == "GET":

        if book is None:
            flash("Книга не найдена", 'warning')
            return redirect(url_for("books.idnex"))

        genres = db.session.execute(db.select(Genre)).scalars()
        return render_template('books/edit.html',
                               book=book,
                               genres=genres)

    try:
        genres_ids = request.form.getlist('genres_id')
        genres = db.session.query(Genre).filter(Genre.id.in_(genres_ids)).all()
        for key, value in params().items():
            setattr(book, key, value)
        book.genres = genres
        db.session.commit()
    except IntegrityError as err:
        flash(f'Возникла ошибка при записи данных в БД. Проверьте корректность введённых данных. ({err})', 'danger')
        db.session.rollback()
        genres = db.session.execute(db.select(Genre)).scalars()
        return render_template('books/edit.html',
                               genres=genres,
                               book=book)

    flash("Книга успешно обновлена", 'success')
    return redirect(url_for('books.index'))


@bp.route("<int:book_id>/book/delete", methods=["POST"])
@login_required
@check_rights(need_admin_role=True)
def delete_book(book_id):
    book = db.session.execute(
        db.select(Book).filter_by(id=book_id)).scalar_one_or_none()
    if book is None:
        flash("Книга не найдена", 'danger')
        return redirect(url_for('books.index'))

    db.session.delete(book)
    db.session.commit()
    flash("Книга успешно удалена", 'success')
    return redirect(url_for('books.index'))


@bp.route('/<int:book_id>')
def show(book_id):
    book = db.session.execute(
        db.select(Book).filter_by(id=book_id)).scalar_one_or_none()
    if book is None:
        flash("Книга не найдена", 'danger')
        return redirect(url_for('books.index'))

    reviews = db.session.execute(
        db.select(Review).filter_by(book_id=book_id).order_by(desc(Review.created_at))).scalars().all()
    user_review = None
    if current_user.is_authenticated:
        user_review = db.session.execute(
            db.select(Review).filter_by(book_id=book_id, user_id=current_user.id)).scalar_one_or_none()

    return render_template('books/show.html',
                           book=book,
                           reviews=reviews,
                           user_review=user_review)


REVIEW_PARAMS = ["user_id", "rating", "text", "book_id"]


def create_review_params():
    return {p: request.form.get(p) or None for p in REVIEW_PARAMS}


@bp.route('/<int:book_id>/review/create', methods=["GET", "POST"])
@login_required
def create_review(book_id):
    book = db.session.execute(
        db.select(Book).filter_by(id=book_id)).scalar_one_or_none()
    existed_review = db.session.execute(
        db.select(Review).filter_by(book_id=book_id, user_id=current_user.id)).scalar_one_or_none()

    if request.method == "GET":
        if book is None:
            flash("Книга не найдена", 'danger')
            return redirect(url_for('books.index'))

        if existed_review is not None:
            flash("Вы уже оставляли рецензию на эту книгу", 'danger')
            return redirect(url_for('books.show', book_id=book_id))

        return render_template("reviews/new.html",
                               book=book,
                               grades=REVIEW_GRADES,
                               review=None)

    if existed_review is not None:
        flash("Вы уже оставляли отзыв для данного курса", 'danger')
        reviews = db.session.execute(
            db.select(Review).filter_by(book_id=book_id).order_by(desc(Review.created_at)).limit(5)).scalars().all()
        return render_template('books/show.html',
                               book=book,
                               reviews=reviews,
                               user_review=existed_review,
                               grades=REVIEW_GRADES,
                               )

    review = Review(**create_review_params())
    try:
        db.session.add(review)
        db.session.commit()
    except IntegrityError as err:
        flash(f'Возникла ошибка при записи данных в БД. Проверьте корректность введённых данных. ({err})', 'danger')
        db.session.rollback()
        reviews = db.session.execute(
            db.select(Review).filter_by(book_id=book_id).order_by(desc(Review.created_at)).limit(5)).scalars().all()
        return render_template('books/show.html',
                               book=book,
                               reviews=reviews,
                               user_review=review,
                               grades=REVIEW_GRADES,
                               )

    flash(f'Отзыв был успешно добавлен!', 'success')

    return redirect(url_for('books.show', book_id=book_id))


@bp.route('/<int:book_id>/review/<int:review_id>/delete', methods=["POST"])
@login_required
@check_rights(need_moderator_role=True)
def delete_review(book_id, review_id):
    existed_review = db.session.execute(
        db.select(Review).filter_by(id=review_id)).scalar_one_or_none()

    if existed_review is None:
        flash('Возникла ошибка при удалении отзыва, отзыв не найден.', 'danger')
        return redirect(url_for('books.show', book_id=book_id))

    try:
        db.session.delete(existed_review)
        db.session.commit()
        flash("Отзыв успешно удален", 'success')
    except IntegrityError as err:
        flash(f"Возникла ошибка при удалении отзыва. ({err})", 'danger')
        db.session.rollback()

    return redirect(url_for('books.show', book_id=book_id))
