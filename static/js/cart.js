function getCookie(name) {
    let cookieValue = null;
    if (document.cookie && document.cookie !== '') {
        const cookies = document.cookie.split(';');
        for (let i = 0; i < cookies.length; i++) {
            const cookie = cookies[i].trim();
            if (cookie.substring(0, name.length + 1) === (name + '=')) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }
    return cookieValue;
}

document.addEventListener('DOMContentLoaded', function () {
    var addToCartButton = document.querySelector('.add-to-cart');
    var csrftoken = getCookie('csrftoken');

    addToCartButton.addEventListener('click', function () {
        var productId = this.dataset.productId;

        var xhr = new XMLHttpRequest();
        xhr.open('POST', '/cart/add/' + productId + '/');
        xhr.setRequestHeader('Content-Type', 'application/json');
        xhr.setRequestHeader('X-CSRFToken', csrftoken);
        xhr.onload = function () {
            if (xhr.status === 200) {
                var data = JSON.parse(xhr.responseText);
                document.querySelector('#cart-counter').textContent = data.cart_total_items;
            }
        };
        xhr.send(JSON.stringify({ quantity: 1 }));
    });
});




