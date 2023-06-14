# [Online Shop for Artists 🎨](http://vermilioh.pythonanywhere.com/)
[check](http://vermilioh.pythonanywhere.com/)

![Project Image](https://github.com/vermilioh/myonlinestore/blob/main/github_images/main.JPG)

## Project Description
This project is an online portfolio and shop for an artist, built with Django and the Django REST Framework. It showcases the artist's works and provides an e-commerce platform for selling these pieces.

⚠️ The website is still under development and currently only supports the desktop version.

## Technologies Used 🛠️
* **Django:** The primary framework used for backend.
* **Django REST Framework:** Utilized for building a RESTful API.
* **HTML/CSS/JavaScript:** Front-end development.
* **SQLite:** Database management.
* **Git & GitHub:** Version control.

## Project Structure 📂
The project consists of a main application and several auxiliary apps:

* **Main application:** Manages overall configuration and routing of the project.
* **Shop:** Handles the display and purchase of products.
* **Cart:** Manages shopping cart functionality.
* **Accounts:** Handles user registration, authentication, and profile management.
* **Core:** Contains core functionalities utilized by other apps.

## Screenshots and Code Examples 🖼️👩‍💻
In this project, I used several technologies, including Django, Django Template Language (DTL), HTML, CSS, JavaScript, and AJAX. Below are a few examples of how I used these technologies in the project.

### Django & Django Template Language (DTL)
The Django web framework was used extensively throughout this project, and Django Template Language was used to generate dynamic HTML for the various pages. Here's a snippet from the `cart_detail.html` template, showing how DTL is used to generate a dynamic table of products in the cart:

```django
{% for item in cart %}
  <tr class="cart">
    <td class="product">
      <img src="{{ item.product.image.url }}" alt="{{ item.product.name }}">
      <div class="name">{{ item.product.name }}</div>
    </td>
    <td class="price">${{ item.product.price|floatformat:2 }}</td>
    ...
  </tr>
{% empty %}
  <tr>
    <td colspan="5">Your cart is empty.</td>
  </tr>
{% endfor %}
```

### JavaScript & AJAX
JavaScript, specifically jQuery, was used to add interactivity to the page, and AJAX was used to update the cart contents without reloading the page. Here's a snippet showing the AJAX calls made when the quantity of a product in the cart is updated:

```javascript
$(document).ready(function() {
  $('.quantity-input').on('change', function() {
    var newQuantity = $(this).val();
    var productId = $(this).data('product-id');

    $.ajax({
        url: '/cart/update/' + productId + '/',
        type: 'POST',
        data: {
            'csrfmiddlewaretoken': '{{ csrf_token }}',
            'quantity': newQuantity
        },
        success: function(response) {
            console.log('AJAX success:', response);
            location.reload();
        },
        error: function(response) {
            console.log('AJAX error:', response);
            alert('There was an error. Please try again.');
        }
    });
  });
});

```

