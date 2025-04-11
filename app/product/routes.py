import os
from datetime import datetime
from flask import Blueprint, send_file, abort
from flask import render_template, url_for, flash, redirect, request, session
from flask_login import (
    login_required,
    login_user,
    current_user,
    logout_user,
)
from app import db, create_app  # Import create_app
from app.product.forms import ProductForm,Update_ProductForm
from app.models import User, Product, Order, OrderItem  # Import all your models
from app.helpers import save_picture,delete_picture
from io import BytesIO
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import letter
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.platypus import Paragraph, SimpleDocTemplate, Spacer
from reportlab.lib.units import inch
from flask_paginate import Pagination, get_page_parameter

product = Blueprint("product", __name__)




@product.route('/add_product', methods=['GET', 'POST'])
@login_required
def add_product():
    form = ProductForm()
    if form.validate_on_submit():
        picture_file = save_picture(form.image.data, "static/media/product_images")
        product = Product(name=form.name.data, description=form.description.data, price=form.price.data, quantity=form.quantity.data, category=form.category.data, image=picture_file,author = current_user.username)
        db.session.add(product)
        db.session.commit()
        flash('Product added successfully!', 'success')
        return redirect(url_for('main.home'))
    return render_template('product/add_product.html', form=form, title='Add New Product')

@product.route('/product/<int:product_id>')
def product_detail(product_id):
    product = Product.query.get_or_404(product_id)
    return render_template('product/product_detail.html', product=product)

@product.route('/cart')
def view_cart():
    cart_items = []
    cart_total = 0
    shipping_cost = 5.00  # Example fixed shipping cost
    if 'cart' in session:
        for product_id, quantity in session['cart'].items():
            product = Product.query.get(int(product_id))
            if product:
                total_price = product.price * quantity
                cart_items.append({'product': product, 'quantity': quantity, 'total_price': total_price, 'id': product.id})
                cart_total += total_price
    return render_template('product/cart.html', cart_items=cart_items, cart_total=cart_total,shipping_cost=shipping_cost)

@product.route('/add_to_cart/<int:product_id>', methods=['POST'])
def add_to_cart(product_id):
    quantity = int(request.form.get('quantity', 1))
    if quantity <= 0:
        flash('Quantity must be at least 1.', 'warning')
        return redirect(url_for('product.product_detail', product_id=product_id))

    product = Product.query.get_or_404(product_id)
    if quantity > product.quantity:
        flash(f'Not enough stock. Only {product.quantity} available.', 'warning')
        return redirect(url_for('product.product_detail', product_id=product_id))

    if 'cart' not in session:
        session['cart'] = {}

    product_id_str = str(product_id)
    if product_id_str in session['cart']:
        session['cart'][product_id_str] += quantity
    else:
        session['cart'][product_id_str] = quantity

    session.modified = True
    flash(f'{quantity} {product.name}(s) added to cart!', 'success')
    return redirect(url_for('product.view_cart'))

@product.route('/update_cart_item/<int:item_id>', methods=['POST'])
def update_cart_item(item_id):
    quantity = int(request.form.get('quantity'))
    if quantity <= 0:
        return redirect(url_for('product.remove_from_cart', item_id=item_id))

    product_id_str = str(item_id)
    product = Product.query.get_or_404(item_id) # Use item_id as product_id here

    if quantity > product.quantity:
        flash(f'Not enough stock for {product.name}. Only {product.quantity} available.', 'warning')
        return redirect(url_for('product.view_cart'))

    if 'cart' in session and product_id_str in session['cart']:
        session['cart'][product_id_str] = quantity
        session.modified = True
        flash(f'{product.name} quantity updated.', 'info')
    return redirect(url_for('product.view_cart'))

@product.route('/remove_from_cart/<int:item_id>', methods=['POST'])
def remove_from_cart(item_id):
    product_id_str = str(item_id)
    if 'cart' in session and product_id_str in session['cart']:
        del session['cart'][product_id_str]
        session.modified = True
        flash('Item removed from cart.', 'info')
    return redirect(url_for('product.view_cart'))

@product.route('/checkout')
def checkout():
    if 'cart' not in session or not session['cart']:
        flash('Your cart is empty. Start shopping!', 'warning')
        return redirect(url_for('main.home'))

    cart_items = []
    cart_total = 0
    shipping_cost = 5.00  # Example fixed shipping cost
    for product_id, quantity in session['cart'].items():
        product = Product.query.get(int(product_id))
        if product:
            total_price = product.price * quantity
            cart_items.append({'product': product, 'quantity': quantity, 'total_price': total_price, 'id': product.id})
            cart_total += total_price

    final_total = cart_total + shipping_cost

    return render_template('product/checkout.html', cart_items=cart_items, cart_total=cart_total, shipping_cost=shipping_cost, final_total=final_total, title='Checkout')


@product.route('/clear_cart')
def clear_cart():
    session.pop('cart', None)
    flash('Your cart has been cleared.', 'info')
    return redirect(url_for('product.view_cart'))


# --- Update Product Details ---
@product.route('/admin/product/update/<int:product_id>', methods=['GET', 'POST'])
@login_required
def update_product(product_id):
    product = Product.query.get_or_404(product_id)
    form = Update_ProductForm()
    if form.validate_on_submit():
        product.name = form.name.data
        product.description = form.description.data
        product.price = form.price.data
        product.quantity = form.quantity.data
        product.category = form.category.data
        if form.image.data:
            # Delete the old image if a new one is uploaded
            if product.image:
                old_image_path = os.path.join(create_app().root_path, "static/media/product_images", product.image)
                delete_picture(old_image_path)
            picture_file = save_picture(form.image.data, "static/media/product_images")
            product.image = picture_file
        db.session.commit()
        flash('Product details updated successfully!', 'success')
        return redirect(url_for('product.product_detail', product_id=product.id))
    elif request.method == "GET":
        form.name.data = product.name
        form.description.data = product.description
        form.price.data = product.price
        form.quantity.data = product.quantity
        form.category.data = product.category
        
    return render_template('product/update_product.html', form=form, product=product, title='Update Product')

# --- Delete Product ---
@product.route('/admin/product/delete/<int:product_id>', methods=['POST'])
@login_required
def delete_product(product_id):
    product = Product.query.get_or_404(product_id)
    # Delete the product image file
    if product.image:
        image_path = os.path.join(create_app().root_path, "static/media/product_images", product.image)
        delete_picture(image_path)
    db.session.delete(product)
    db.session.commit()
    flash('Product deleted successfully!', 'success')
    return redirect(url_for('main.home')) # Or a product listing page

# Place order routes
@product.route('/place_order', methods=['POST'])
@login_required
def place_order():
    if 'cart' not in session or not session['cart']:
        flash('Your cart is empty.', 'warning')
        return redirect(url_for('main.home'))

    cart = session['cart']
    cart_total = 0
    order_items = []

    order = Order(user_id=current_user.id, order_date=datetime.utcnow())
    db.session.add(order)
    db.session.flush()  # Get the order ID immediately

    for product_id_str, quantity in cart.items():
        product = Product.query.get(int(product_id_str))
        if product:
            if product.quantity < quantity:
                flash(f'Not enough stock for {product.name}. Only {product.quantity} available.', 'danger')
                db.session.rollback()
                return redirect(url_for('product.view_cart'))

            total_price = product.price * quantity
            cart_total += total_price
            order_item = OrderItem(
                order_id=order.id,
                product_id=product.id,
                quantity=quantity,
                price=product.price
            )
            order_items.append(order_item)
            db.session.add(order_item)

            # Update product quantity
            product.quantity -= quantity

    order.total_amount = cart_total + 5.00  # Add your shipping cost here
    db.session.commit()

    session.pop('cart', None)  # Clear the cart

    flash(f'Your order has been placed successfully! Order ID: {order.id}', 'success')
    return redirect(url_for('product.order_confirmation', order_id=order.id))

@product.route('/order/confirmation/<int:order_id>')
@login_required
def order_confirmation(order_id):
    order = Order.query.get_or_404(order_id)
    if order.user_id != current_user.id:
        abort(403)  # Unauthorized access
    order_items = OrderItem.query.filter_by(order_id=order.id).all()
    return render_template('product/order/order_confirmation.html', order=order, order_items=order_items)

# Download order as pdf
@product.route('/order/download_pdf/<int:order_id>')
@login_required
def download_order_pdf(order_id):
    order = Order.query.get_or_404(order_id)
    if order.user_id != current_user.id:
        abort(403)

    order_items = OrderItem.query.filter_by(order_id=order.id).all()

    buffer = BytesIO()
    doc = SimpleDocTemplate(buffer, pagesize=letter)
    styles = getSampleStyleSheet()
    story = []

    story.append(Paragraph("Order Confirmation", styles['Heading1']))
    story.append(Spacer(1, 0.2 * inch))
    story.append(Paragraph(f"Order ID: {order.id}", styles['Normal']))
    story.append(Paragraph(f"Order Date: {order.order_date.strftime('%Y-%m-%d %H:%M:%S UTC')}", styles['Normal']))
    story.append(Spacer(1, 0.2 * inch))
    story.append(Paragraph("Order Details:", styles['Heading2']))
    story.append(Spacer(1, 0.1 * inch))

    data = [['Product', 'Quantity', 'Price', 'Total']]
    for item in order_items:
        data.append([
            item.product.name,
            str(item.quantity),
            f"${item.price:.2f}",
            f"${item.quantity * item.price:.2f}"
        ])

    from reportlab.platypus import Table, TableStyle
    from reportlab.lib import colors

    table = Table(data)
    table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), colors.grey),
        ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
        ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
        ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
        ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
        ('BACKGROUND', (0, 1), (-1, -1), colors.beige),
        ('GRID', (0, 0), (-1, -1), 1, colors.black)
    ]))
    story.append(table)
    story.append(Spacer(1, 0.2 * inch))
    story.append(Paragraph(f"Total Amount: ${order.total_amount:.2f}", styles['Heading3']))

    doc.build(story)
    buffer.seek(0)

    return send_file(
        buffer,
        mimetype='application/pdf',
        as_attachment=True,
        download_name=f'order_confirmation_{order.id}.pdf'
    )


# Order History routes

@product.route('/order/history')
@login_required
def order_history():
    page = request.args.get('page', 1, type=int)
    per_page = 5  # You can adjust the number of orders per page
    orders = Order.query.filter_by(user_id=current_user.id).order_by(Order.order_date.desc()).paginate(page=page, per_page=per_page)
    return render_template('product/order/order_history.html', orders=orders)

# Order History Details 
@product.route('/order/<int:order_id>/details')
@login_required
def order_details(order_id):
    order = Order.query.get_or_404(order_id)
    if order.user_id != current_user.id:
        abort(403)

    page = request.args.get('page', 1, type=int)
    per_page = 5  # You can adjust the number of items per page
    order_items = OrderItem.query.filter_by(order_id=order.id).paginate(page=page, per_page=per_page)
    return render_template('product/order/order_details.html', order=order, order_items=order_items)




# Author route
@product.route('/author/<string:author_name>', defaults={'page': 1})
@product.route('/author/<string:author_name>/page/<int:page>')
def products_by_author(author_name, page):
    per_page = 9  # You can adjust the number of products per page
    products = Product.query.filter_by(author=author_name).paginate(page=page, per_page=per_page)
    pagination = Pagination(page=page, total=products.total, per_page=per_page,
                            record_name='products')
    return render_template('product/products_by_author.html', products=products, pagination=pagination, author_name=author_name)
