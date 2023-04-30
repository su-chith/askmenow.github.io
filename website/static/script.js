function deleteQuestion() {
    document.addEventListener('DOMContentLoaded', () => {
        const deleteButtons = document.querySelectorAll('.delete-question');
        deleteButtons.forEach(button => {
            console.log('button worked ..................');
            button.addEventListener('click', event => {
                event.preventDefault();
                const questionId = button.dataset.questionid;
                const username = button.dataset.username;
                if (confirm("Are you sure you want to delete this question?")) {
                    fetch(`/profile/${username}/questions/${questionId}`, {
                        method: 'DELETE',
                    })
                        .then(response => {
                            if (response.ok) {
                                window.location.reload();
                            }
                        })
                        .catch(error => console.error(error));
                }
            });
        });
    });

}


document.addEventListener('DOMContentLoaded', function () {
    const upvoteButtons = document.querySelectorAll('.upvote-btn');
    const downvoteButtons = document.querySelectorAll('.downvote-btn');

    upvoteButtons.forEach(function (button) {
        button.addEventListener('click', function (event) {
            event.preventDefault();
            const button = this;
            const post_id = this.getAttribute('data-post');
            const this_post_id = this.getAttribute('data-post-id');
            const url = '/upvote/' + post_id;

            fetch(url, {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                    'X-Requested-With': 'XMLHttpRequest'
                }
            }).then(function (response) {
                if (response.ok) {
                    const upvoteCountElement = document.querySelector(`.upvote-count-${this_post_id}`);
                    const currentUpvoteCount = parseInt(upvoteCountElement.textContent);
                    const newUpvoteCount = button.classList.contains('upvoted') ? currentUpvoteCount - 1 : currentUpvoteCount + 1;
                    upvoteCountElement.textContent = newUpvoteCount;

                    if (button.classList.contains('upvoted')) {
                        button.classList.remove('upvoted');
                    } else {
                        button.classList.add('upvoted');
                        const downvoteButton = button.nextElementSibling;
                        if (downvoteButton.classList.contains('downvoted')) {
                            downvoteButton.classList.remove('downvoted');
                            const downvoteCountElement = document.querySelector(`.downvote-count-${this_post_id}`);
                            const currentDownvoteCount = parseInt(downvoteCountElement.textContent);
                            const newDownvoteCount = currentDownvoteCount - 1;
                            downvoteCountElement.textContent = newDownvoteCount;
                        }
                    }
                } else {
                    console.log('Failed to update upvote status');
                }
            }).catch(function (error) {
                console.log(error);
            });
        });
    });

    downvoteButtons.forEach(function (button) {
        button.addEventListener('click', function (event) {
            event.preventDefault();
            const button = this;
            const post_id = this.getAttribute('data-post');
            const this_post_id = this.getAttribute('data-post-id');
            const url = '/downvote/' + post_id;

            fetch(url, {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                    'X-Requested-With': 'XMLHttpRequest'
                }
            }).then(function (response) {
                if (response.ok) {
                    const downvoteCountElement = document.querySelector(`.downvote-count-${this_post_id}`);
                    const currentDownvoteCount = parseInt(downvoteCountElement.textContent);
                    const newDownvoteCount = button.classList.contains('downvoted') ? currentDownvoteCount + 1 : currentDownvoteCount - 1;
                    downvoteCountElement.textContent = newDownvoteCount;

                    if (button.classList.contains('downvoted')) {
                        button.classList.remove('downvoted');
                    } else {
                        button.classList.add('downvoted');
                        const upvoteButton = button.previousElementSibling;
                        if (upvoteButton.classList.contains('upvote')) {
                            upvoteButton.classList.remove('upvoted');
                            const upvoteCountElement = document.querySelector(`.upvote-count-${this_post_id}`);
                            const currentUpvoteCount = parseInt(upvoteCountElement.textContent);
                            const newUpvoteCount = currentUpvoteCount - 1;
                            upvoteCountElement.textContent = newUpvoteCount;
                        }
                    }
                }
            })
        })
    })
});
