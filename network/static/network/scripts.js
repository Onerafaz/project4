document.addEventListener("DOMContentLoaded", function() {
    const likeButtons = document.querySelectorAll(".like-button");

    likeButtons.forEach(button => {
        const postId = button.id;
        const isLiked = button.getAttribute('data-liked') === 'true';
        const likesCount = parseInt(document.querySelector(`#likes-count-${postId} strong`).textContent);

        button.addEventListener("click", function(event) {
            event.preventDefault();
            postLike(postId, isLiked, likesCount);
        });
    });

});

// JavaScript to handle the search functionality
document.getElementById("search-button").addEventListener("click", function() {
    performSearch();
});

document.getElementById("search-input").addEventListener("keypress", function(event) {
    if (event.key === "Enter") {
        performSearch();
    }
});

function performSearch() {
    const searchQuery = document.getElementById("search-input").value;
    window.location.href = `/search/?q=${encodeURIComponent(searchQuery)}`;
    highlight(searchQuery);
}

function highlight(param) {
    var comments = document.querySelectorAll(".comment-message"); // Target the comment message elements
    comments.forEach(comment => {
        var ob = new Mark(comment);
        ob.unmark();
        ob.mark(param, { className: 'highlighted' });
    });
}




// Handle the edit post and hide modal refreshing HTML asynchronously
function getCookie(name) {
    const value = `; ${document.cookie}`;
    const parts = value.split(`; ${name}=`);
    if(parts.length == 2) return parts.pop().split(';').shift();
}

function submitEdit(id) {
    const textAreaValue = document.getElementById(`textArea${id}`).value
    const content = document.getElementById(`content${id}`);
    const modal = document.getElementById(`editPostModal${id}`);
    fetch(`/edit/${id}`, {
        method: "POST",
        headers: {"Content-type": "application/json", "X-CSRFToken": getCookie("csrftoken")},
        body: JSON.stringify({
            content: textAreaValue
        })
    })
    .then(response => response.json())
    .then(result => {
        content.innerHTML = result.data;
        modal.classList.remove('show');
        modal.setAttribute('aria-hidden', 'true');
        modal.setAttribute('style', 'display: none');

        // get modal backdrops
        const modalsBackDrops = document.getElementsByClassName('modal-backdrop');

        // remove every modal backdrop
        for(let i = 0; i < modalsBackDrops.length; i ++) {
            document.body.removeChild(modalsBackDrops[i]);
        }
    })
}

// Function to update the likes count in the HTML
function updateLikesCount(postId, likesCount) {
    const likesCountElement = document.getElementById(`likes-count-${postId}`);
    if (likesCountElement) {
        const strongElement = likesCountElement.querySelector('strong');
        if (strongElement) {
            strongElement.textContent = likesCount;
        }
    }
}

// Function to handle the like button click
function postLike(postId) {
    const btn = document.getElementById(postId);
    const isLiked = btn.getAttribute('data-liked') === 'true';

    if (!btn.classList.contains('processing')) {
        btn.classList.add('processing');

        const endpoint = isLiked ? `/removelike/${postId}` : `/addlike/${postId}`;

        fetch(endpoint)
            .then(response => response.json())
            .then(result => {
                console.log(result.message);
                console.log('Likes count from server:', result.likes_count);

                btn.setAttribute('data-liked', !isLiked);
                btn.classList.toggle('liked');

                // Update likes count in the HTML
                updateLikesCount(postId, result.likes_count);

            })
            .catch(error => {
                console.error(error);
            })
            .finally(() => {
                btn.classList.remove('processing');
            });
    }
}
