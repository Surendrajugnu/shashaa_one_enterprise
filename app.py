from datetime import datetime
from flask import Flask, render_template, request, redirect, url_for, flash, abort
from flask_sqlalchemy import SQLAlchemy
from flask_mail import Mail, Message
from dotenv import load_dotenv
import os

# Load environment variables from .env file
load_dotenv()

app = Flask(__name__)
app.secret_key = "change-this-secret-key"
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///callbacks.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# Email Configuration (uses environment variables for security)
app.config['MAIL_SERVER'] = os.getenv('MAIL_SERVER', 'smtp.gmail.com')
app.config['MAIL_PORT'] = int(os.getenv('MAIL_PORT', 587))
app.config['MAIL_USE_TLS'] = os.getenv('MAIL_USE_TLS', True)
app.config['MAIL_USERNAME'] = os.getenv('MAIL_USERNAME', 'surendra.jugnu@gmail.com')
app.config['MAIL_PASSWORD'] = os.getenv('MAIL_PASSWORD', 'test-password')
app.config['MAIL_DEFAULT_SENDER'] = os.getenv('MAIL_DEFAULT_SENDER', 'surendra.jugnu@gmail.com')

mail = Mail(app)
db = SQLAlchemy(app)

class Callback(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(100), nullable=False)
    phone = db.Column(db.String(15), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    def __repr__(self):
        return f'<Callback {self.name}>'

@app.context_processor
def inject_now():
    return {"now": datetime.utcnow()}

category_cards = [
    {"slug": "health", "title": "Health Insurance", "description": "Cashless hospital stays and family coverage.", "icon": "🏥"},
    {"slug": "life", "title": "Life Insurance", "description": "Term plans, savings and family security.", "icon": "💙"},
    {"slug": "motor", "title": "Motor Insurance", "description": "Car and bike cover with fast claims.", "icon": "🚗"},
    {"slug": "travel", "title": "Travel Insurance", "description": "Domestic and international trip protection.", "icon": "✈️"},
]

home_products = [
    {"title": "Term Life Insurance", "badge": "Upto 15% Discount", "icon": "🛡️", "href": "/category/life"},
    {"title": "Health Insurance", "badge": "Lowest Price Guarantee", "icon": "❤️", "href": "/category/health"},
    {"title": "Investment Plans", "badge": "In-Built Life Cover", "icon": "💰", "href": "/category/life"},
    {"title": "Car Insurance", "badge": "Lowest Price Guarantee", "icon": "🚗", "href": "/category/motor"},
    {"title": "2 Wheeler Insurance", "badge": "Upto 85% Discount", "icon": "🏍️", "href": "/category/motor"},
    {"title": "Family Health Insurance", "badge": "Upto 25% Discount", "icon": "👪", "href": "/category/health"},
    {"title": "Travel Insurance", "badge": "Fast Claims", "icon": "✈️", "href": "/category/travel"},
    {"title": "Term Insurance (Women)", "badge": "Upto 20% Cheaper", "icon": "👩‍🦰", "href": "/category/life"},
    {"title": "Term Plans with Return of Premium", "badge": "Smart Savings", "icon": "💵", "href": "/category/life"},
    {"title": "Guaranteed Return Plans", "badge": "Upto 7.4% Returns", "icon": "📈", "href": "/category/life"},
    {"title": "Child Savings Plans", "badge": "Premium Waiver", "icon": "👶", "href": "/category/life"},
    {"title": "Retirement Plans", "badge": "Steady Income", "icon": "🧓", "href": "/category/life"},
    {"title": "Employee Group Health Insurance", "badge": "Upto 65% Discount", "icon": "🏥", "href": "/category/health"},
    {"title": "Commercial Vehicle", "badge": "Business Cover", "icon": "🚚", "href": "/category/motor"},
]

policy_plans = [
    {"category": "health", "title": "Family Health Shield", "price": 5600, "benefit": "Cashless hospital admission", "details": "Comprehensive family health cover with wellness benefits."},
    {"category": "health", "title": "Senior Citizen Care", "price": 5900, "benefit": "Critical illness cover", "details": "Designed for parents with high medical coverage."},
    {"category": "life", "title": "Term Secure Plan", "price": 7800, "benefit": "High sum assured", "details": "Pure protection term insurance for long-term security."},
    {"category": "life", "title": "Savings Plus Plan", "price": 9200, "benefit": "Maturity benefit", "details": "Life cover with savings and flexible premiums."},
    {"category": "motor", "title": "Car Protect Max", "price": 4200, "benefit": "Own-damage cover", "details": "Comprehensive car insurance with zero depreciation add-on."},
    {"category": "motor", "title": "Easy Bike Shield", "price": 2200, "benefit": "Third-party and own damage", "details": "Affordable bike cover for daily commuters."},
    {"category": "travel", "title": "International Trip Cover", "price": 2600, "benefit": "Emergency medical cover", "details": "Worldwide cover for medical emergencies and baggage loss."},
    {"category": "travel", "title": "Domestic Travel Plan", "price": 1300, "benefit": "Trip cancellation cover", "details": "Short-trip insurance for domestic leisure and business travel."},
]

companies = [
    {"name": "Shasha Secure", "rating": 4.8, "description": "Fast policy comparisons and dependable claim support."},
    {"name": "Enterprise Shield", "rating": 4.6, "description": "Custom insurance solutions for businesses and families."},
    {"name": "Trust Guard", "rating": 4.5, "description": "Trusted cover with digital policy servicing."},
    {"name": "HealthPlus", "rating": 4.7, "description": "Wellness plans with cashless hospital access nationwide."},
]

testimonials = [
    {"name": "Ayesha K.", "quote": "Found the right family health plan in minutes. The premium comparison was very helpful."},
    {"name": "Rohan S.", "quote": "The travel insurance recommendations were easy to understand and cost-effective."},
    {"name": "Priya M.", "quote": "I secured term life cover quickly with a plan that fit my budget."},
]

locations = ["Delhi", "Mumbai", "Bengaluru", "Chennai", "Kolkata"]

age_brackets = {
    "18-25": 1.0,
    "26-35": 1.1,
    "36-45": 1.25,
    "46-55": 1.45,
    "56+": 1.7,
}

categories = {
    "individual": 1.0,
    "family": 1.45,
    "business": 2.0,
}

benefits = [
    {"title": "Compare 500+ plans", "description": "Get instant pricing across leading insurers."},
    {"title": "Easy claims support", "description": "Quick assistance for policy servicing and claims."},
    {"title": "Expert advice", "description": "Insurance guidance with clear plan comparisons."},
]

@app.route("/")
def index():
    featured = policy_plans[:6]
    return render_template(
        "index.html",
        category_cards=category_cards,
        featured=featured,
        companies=companies,
        testimonials=testimonials,
        benefits=benefits,
        home_products=home_products,
        also_buy=["LIC Plans", "Return of Premium", "Life Insurance for Housewives", "Day 1 Coverage", "1 Cr Health Insurance", "Personal Accident", "Commercial Vehicles"],
    )

@app.route("/category/<slug>")
def category_page(slug):
    category_info = next((item for item in category_cards if item["slug"] == slug), None)
    if not category_info:
        abort(404)

    plans = [plan for plan in policy_plans if plan["category"] == slug]
    return render_template("category.html", category=category_info, plans=plans, companies=companies)

@app.route("/quote", methods=["GET", "POST"])
def quote():
    results = None
    if request.method == "POST":
        name = request.form.get("name", "").strip()
        email = request.form.get("email", "").strip()
        age = request.form.get("age")
        category = request.form.get("category")
        sum_assured = request.form.get("sum_assured")
        location = request.form.get("location")

        if not name or not email or not age or not category or not sum_assured or not location:
            flash("Please complete all quote fields before submitting.", "error")
            return redirect(url_for("quote"))

        quote_value = calculate_quote(age, category, int(sum_assured), location)
        selected_plan = next((plan for plan in policy_plans if plan["category"] == category), policy_plans[0])

        results = {
            "name": name,
            "email": email,
            "quote": quote_value,
            "category": category,
            "sum_assured": sum_assured,
            "location": location,
            "plan": selected_plan,
        }

    return render_template("quote.html", locations=locations, categories=categories, results=results, category_cards=category_cards)

@app.route("/companies")
def companies_page():
    return render_template("companies.html", companies=companies)

@app.route("/about")
def about():
    return render_template("about.html", category_cards=category_cards, benefits=benefits)

@app.route("/login")
def login():
    return render_template("login.html")

@app.route("/get-callback")
def get_callback_page():
    return render_template("get_callback.html")

@app.route("/callback", methods=["POST"])
def callback():
    name = request.form.get("callback_name", "").strip()
    email = request.form.get("callback_email", "").strip()
    phone = request.form.get("callback_phone", "").strip()

    if not name or not email or not phone:
        flash("Please fill all callback fields.", "error")
        return redirect(url_for("index"))

    try:
        new_callback = Callback(name=name, email=email, phone=phone)
        db.session.add(new_callback)
        db.session.commit()
        
        # Send email to admin
        admin_email = "Richaverma0312@gmail.com"
        admin_subject = f"New Callback Request from {name}"
        admin_body = f"""
        New Callback Request Received:
        
        Name: {name}
        Email: {email}
        Phone: {phone}
        Submitted: {datetime.utcnow().strftime('%Y-%m-%d %H:%M:%S')}
        
        Please contact the customer at the provided phone number or email.
        
        Best regards,
        Shashaa One Enterprise
        """
        
        try:
            admin_msg = Message(subject=admin_subject, recipients=[admin_email], body=admin_body)
            mail.send(admin_msg)
        except Exception as email_error:
            print(f"Error sending admin email: {email_error}")
        
        # Send confirmation email to customer
        customer_subject = "Callback Request Confirmed - Shashaa One Enterprise"
        customer_body = f"""
        Hi {name},
        
        Thank you for requesting a callback! We've received your request and our experts will call you soon at {phone}.
        
        Your Details:
        Name: {name}
        Email: {email}
        Phone: {phone}
        
        We appreciate your interest in our insurance products. Our team will contact you within 24 hours.
        
        Best regards,
        Shashaa One Enterprise Team
        Richaverma0312@gmail.com
        """
        
        try:
            customer_msg = Message(subject=customer_subject, recipients=[email], body=customer_body)
            mail.send(customer_msg)
        except Exception as email_error:
            print(f"Error sending customer email: {email_error}")
        
        flash("Thank you! We'll call you soon. Check your email for confirmation.", "success")
    except Exception as e:
        db.session.rollback()
        flash("Error saving your callback request. Please try again.", "error")
        print(f"Error: {e}")

    return redirect(url_for("index"))

def calculate_quote(age_range, category, sum_assured, location):
    age_factor = age_brackets.get(age_range, 1.0)
    category_factor = categories.get(category, 1.0)
    location_factor = 1.05 if location in ["Mumbai", "Delhi", "Bengaluru"] else 1.0
    base = sum_assured / 1000
    premium = base * age_factor * category_factor * location_factor * 12
    return round(premium)

if __name__ == "__main__":
    with app.app_context():
        db.create_all()
    app.run(debug=True)
