        
            // This script will update the cart count in the navbar dynamically
            function updateCartCount() {
                fetch('/cart/count') // Create a new route in your Flask app to get the cart count
                    .then(response => response.json())
                    .then(data => {
                        const cartBadge = document.querySelector('.nav-masthead a[href="{{ url_for('product.view_cart') }}"] .badge');
                        if (cartBadge) {
                            cartBadge.textContent = data.count;
                            if (data.count > 0) {
                                cartBadge.classList.add('bg-success');
                                cartBadge.classList.remove('bg-secondary');
                            } else {
                                cartBadge.classList.remove('bg-success');
                                cartBadge.classList.add('bg-secondary');
                            }
                        }
                    })
                    .catch(error => {
                        console.error('Error fetching cart count:', error);
                    });
            }

            // Call updateCartCount when the page loads
            document.addEventListener('DOMContentLoaded', updateCartCount);

            // You might need to call updateCartCount after a successful "Add to Cart" action
            // For example, if your "Add to Cart" form submits via JavaScript:
            document.querySelectorAll('form[action^="/add_to_cart/"]').forEach(form => {
                form.addEventListener('submit', function(event) {
                    event.preventDefault(); // Prevent default form submission
                    fetch(this.action, {
                        method: 'POST',
                        body: new FormData(this)
                    })
                    .then(response => response.json()) // Assuming your add_to_cart route returns JSON
                    .then(data => {
                        if (data.success) {
                            updateCartCount(); // Update the cart count in the navbar
                            // Optionally show a success message to the user
                        } else if (data.error) {
                            // Optionally show an error message
                        }
                    })
                    .catch(error => {
                        console.error('Error adding to cart:', error);
                    });
                });
            });
        