$(document).ready(function () {
  $(".like-btn-form").submit(function (e) {
    e.preventDefault();

    const $form = $(this);
    const url = $form.data("url");
    const csrf_token = $form.find('input[name="csrfmiddlewaretoken"]').val();

    $.ajax({
      url: url,
      type: 'POST',
      headers: {
        'X-CSRFToken': csrf_token
      },
      success: function (data) {
        const $button = $form.find("button");
        const $icon = $button.find("i");
        const $count = $form.find("span");

        if (data["is_liked"] === true) {
          $button
              .removeClass("btn btn-sm text-light p-2 d-flex align-items-center")
            .addClass("btn btn-sm text-info p-2")
            .html('<i class="bi bi-heart-fill mr-1"></i> Liked');
        } else {
          $button
            .removeClass("btn btn-sm text-info p-2")
            .addClass("btn btn-sm text-light p-2 d-flex align-items-center")
            .html('<i class="bi bi-heart mr-1"></i> Like');
        }

        $count.text(data["likes"]);
      },
      error: function (xhr, status, error) {
        console.log("Error:", error);
      }
    });
  });
});


console.log("hello");
// open the comment form after click on the button
document.addEventListener("DOMContentLoaded", function () {
  document.addEventListener("click", function (event) {

    const openBtn = event.target.closest(".open-comment-form");
    const cancelBtn = event.target.closest(".cancel-comment");

    if (openBtn) {
      const postId = openBtn.getAttribute("data-post-id");
      const popup = document.getElementById(`comment-popup-${postId}`);
      if (popup) popup.classList.remove("d-none");
    }

    if (cancelBtn) {
      const postId = cancelBtn.getAttribute("data-post-id");
      const popup = document.getElementById(`comment-popup-${postId}`);
      if (popup) popup.classList.add("d-none");
    }

    // Close popup if clicking outside the form box
    const popupOverlay = event.target.closest(".comment-popup-overlay");
    if (popupOverlay && !event.target.closest(".comment-popup-box")) {
      popupOverlay.classList.add("d-none");
    }
  });
});


$(document).ready(function () {
  $(".follow-btn-form").submit(function (e) {
    e.preventDefault();

    const $form = $(this);
    const url = $form.data("url");
    const csrf_token = $form.find('input[name="csrfmiddlewaretoken"]').val();

    $.ajax({
      url: url,
      type: 'POST',
      headers: {
        'X-CSRFToken': csrf_token
      },
      success: function (data) {
        const $button = $form.find("button");
        const $icon = $button.find("i");
        const $count = $form.find("span");

        if (data["is_liked"] === true) {
          $button
              .removeClass("btn btn-sm text-light p-2 d-flex align-items-center")
            .addClass("btn btn-sm text-info p-2")
            .html('<i class="bi bi-heart-fill mr-1"></i> Liked');
        } else {
          $button
            .removeClass("btn btn-sm text-info p-2")
            .addClass("btn btn-sm text-light p-2 d-flex align-items-center")
            .html('<i class="bi bi-heart mr-1"></i> Like');
        }

        $count.text(data["likes"]);
      },
      error: function (xhr, status, error) {
        console.log("Error:", error);
      }
    });
  });
});

