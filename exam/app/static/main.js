'use strict';

function imagePreviewHandler(event) {
    if (event.target.files && event.target.files[0]) {
        let reader = new FileReader();
        reader.onload = function (e) {
            let img = document.querySelector('.cover-preview > img');
            img.src = e.target.result;
            if (img.classList.contains('d-none')) {
                let label = document.querySelector('.cover-preview > label');
                label.classList.add('d-none');
                img.classList.remove('d-none');
            }
        }
        reader.readAsDataURL(event.target.files[0]);
    }
}

function openLink(event) {
    let row = event.target.closest('.row');
    if (row.dataset.url) {
        window.location = row.dataset.url;
    }
}

function fillDeleteBookModalInfo(event) {
    let deleteUrl = event.relatedTarget.dataset.deleteUrl;
    let bookName = event.relatedTarget.dataset.name;

    let title = event.target.querySelector(".modal-book-name");
    title.innerHTML = "Вы действительно хотите удалить книгу " + bookName;

    let modalForm = event.target.querySelector("form");
    modalForm.action = deleteUrl;
}

function fillDeleteBookReviewModalInfo(event) {
    let deleteUrl = event.relatedTarget.dataset.deleteUrl;
    let username = event.relatedTarget.dataset.name;

    let title = event.target.querySelector(".modal-review-user-name");
    title.innerHTML = "Вы действительно хотите удалить отзыв от " + username;

    let modalForm = event.target.querySelector("form");
    modalForm.action = deleteUrl;
}


window.onload = function() {
    let background_img_field = document.getElementById('cover_img');
    if (background_img_field) {
        background_img_field.onchange = imagePreviewHandler;
    }
    for (let book_elm of document.querySelectorAll('.books-list .row')) {
        book_elm.onclick = openLink;
    }

    let deleteBookReviewModalInfo = document.getElementById("delete_review_modal");
    deleteBookReviewModalInfo.addEventListener("show.bs.modal", fillDeleteBookReviewModalInfo);

    let deleteBookModalWindow = document.getElementById("delete_book_modal");
    deleteBookModalWindow.addEventListener("show.bs.modal", fillDeleteBookModalInfo);
}