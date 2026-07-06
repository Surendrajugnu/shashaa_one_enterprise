from datetime import datetime
from flask import Flask, render_template, request, redirect, url_for, flash, abort

app = Flask(__name__)
app.secret_key = "change-this-secret-key"

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

def calculate_quote(age_range, category, sum_assured, location):
    age_factor = age_brackets.get(age_range, 1.0)
    category_factor = categories.get(category, 1.0)
    location_factor = 1.05 if location in ["Mumbai", "Delhi", "Bengaluru"] else 1.0
    base = sum_assured / 1000
    premium = base * age_factor * category_factor * location_factor * 12
    return round(premium)

if __name__ == "__main__":
    app.run(debug=True)
