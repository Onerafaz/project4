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

// JavaScript to handle the search functionality on click
document.getElementById("search-button").addEventListener("click", function() {
    performSearch();
});

// JavaScript to handle the search functionality on key press "Enter"
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

document.addEventListener("DOMContentLoaded", function() {
    const searchQuery = decodeURIComponent(window.location.search.replace("?q=", ""));
    highlight(searchQuery);
});

function highlight(query) {
    // Use Mark.js to highlight the query
    const context = document.querySelector(".search-post");
    const mark = new Mark(context);
    mark.unmark().mark(query, {
        exclude: ["button", "input"] // Exclude buttons and input elements from the highlight
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
                // console.log(result.message);
                // console.log('Likes count from server:', result.likes_count);

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


// Function to handle the comment like button click
function commentLike(commentId) {
    // Try to get the button element by ID
    const btn = document.getElementById(`comment-like-${commentId}`);

    // Check if the button element exists
    if (btn) {
        // Log the button element and its attributes for debugging
        // console.log('Button element:', btn);
        
        // Get the 'data-comment-liked' attribute
        const isLiked = btn.getAttribute('data-comment-liked') === 'true';

        if (!btn.classList.contains('processing')) {
            btn.classList.add('processing');

            const endpoint = isLiked ? `/addCommentLike/${commentId}` : `/removeCommentlike/${commentId}`;

            fetch(endpoint)
                .then(response => {
                    if (!response.ok) {
                        throw new Error(`HTTP error! Status: ${response.status}`);
                    }
                    return response.json();
                })
                .then(result => {
                    // console.log(result.message);
                    // console.log('Likes count from server:', result.likes_count);

                    btn.setAttribute('data-comment-liked', !isLiked);
                    btn.classList.toggle('liked');

                    // Update likes count in the HTML
                    updateCommentLikesCount(commentId, result.likes_count);
                })
                .catch(error => {
                    console.error('Error:', error);
                })
                .finally(() => {
                    btn.classList.remove('processing');
                });
        }
    }
}

// Function to update the comment likes count in the HTML
function updateCommentLikesCount(commentId, likesCount) {
    const likesCountElement = document.getElementById(`comment-likes-count-${commentId}`);
    if (likesCountElement) {
        const strongElement = likesCountElement.querySelector('strong');
        if (strongElement) {
            strongElement.textContent = likesCount;
        }
    }
}

// Example usage:
// Attach a click event listener to your comment like buttons
document.querySelectorAll('.comment-like-button').forEach(button => {
    button.addEventListener('click', () => {
        const commentId = button.dataset.commentId;
        commentLike(commentId);
    });
});
