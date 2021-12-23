window.addEventListener('DOMContentLoaded', () => {
    let profileImages = Array.from(document.getElementsByClassName('profile-image'))
    let currentImageIndex = 0

    let interwalId = setInterval(function () {

        profileImages.forEach(function (item, index) {
            if (index !== currentImageIndex) {
                item.style.display = "none";
            } else {
                item.style.display = "block";
            }
        })
        currentImageIndex++

        if (currentImageIndex === profileImages.length) {
            currentImageIndex = 0
        }

    }, 1000);
})


