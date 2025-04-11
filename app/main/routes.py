from flask import Blueprint, request
from flask import render_template
from app.models import Product


main = Blueprint("main", __name__)


@main.route("/")
@main.route('/home')
def home():
    page = request.args.get('page', 1, type=int)
    per_page = 9  # You can adjust the number of products per page
    products = Product.query.paginate(page=page, per_page=per_page)
    return render_template('main/home.html', products=products)


@main.route("/about")
def about():
    return render_template("main/about.html", title="About")

# Quick Links Routes
@main.route("/about_us")
def about_us():
    return render_template("quick_links/about_us.html", title="About Us")

@main.route("/download")
def download():
    return render_template("quick_links/download.html", title="Download")

@main.route("/privacy_policy")
def privacy_policy():
    return render_template("quick_links/privacy_policy.html", title="Privacy Policy")

@main.route("/terms_condition")
def terms_condition():
    return render_template("quick_links/terms_condition.html", title="Terms & Conditions")
