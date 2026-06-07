# AlphaCart - Premium Full-Stack E-Commerce Platform

A complete full-stack E-Commerce web application built with **Django (Python)**, **SQLite**, and **Bootstrap 5** for a CodeAlpha Full Stack Development internship project. 

AlphaCart is customized for developer workspace essentials (keyboards, monitors, mice, audio equipment, ergonomic office chairs). The project features a premium, responsive glassmorphism UI layout, secure authentication, wishlist management, cart operations, checkout processing, and review/rating systems.

---

## 🚀 Key Features

1. **Secure User Authentication**:
   - Django auth sessions for registration, login, logout.
   - Profile management with automatic creation upon sign-up (signals).
   - Saved shipping profile to auto-fill checkout fields.
   
2. **Dynamic Product Catalog**:
   - Multi-option search (q query parameter).
   - Sidebar filters by category and sorting (price low-to-high, high-to-low, newest).
   - Dynamic CSS fallback placeholders for products without uploaded images.
   - Stock indicators with alerts for low inventory.

3. **Shopping Cart & Session Merging**:
   - Add, remove, and update quantities.
   - Seamlessly merges a guest cart with the user's account cart upon login.
   - Validates available stock quantity before items are added or updated.

4. **Secure Checkout & Order Processing**:
   - Multi-column order summary and shipping address inputs.
   - Deducts items from active product inventory levels.
   - Order confirmation tracking and complete order history lists.
   
5. **Interactive Dashboard**:
   - Single-form profile editor updating user details and shipping details.
   - Quick access to recent orders, saved wishlists, and shopping status.

6. **Feedback & Review System**:
   - 1-to-5 star ratings with detailed comments.
   - Restricts reviews to registered users, enforcing one review per product.
   
7. **Admin Panel**:
   - Manage categories, products, orders, reviews, and wishlists.
   - Inline tabular order item views for administrative review.

---

## 🛠️ Tech Stack
* **Backend**: Django 6.0.6 (Python)
* **Database**: SQLite3
* **Frontend**: HTML5, CSS3 (Custom Stylesheet), JavaScript (ES6)
* **UI Framework**: Bootstrap 5.3.2
* **Icons & Fonts**: FontAwesome 6, Google Fonts (Inter, Outfit)

---

## 📦 Project Directory Layout

```text
ECommerce/
│
├── accounts/          # User profiles, auth forms, dashboard view
├── products/          # Catalog lists, search, details, wishlist, reviews, seed commands
├── cart/              # Cart management utilities & context processors
├── orders/            # Checkout views, order item saves, stock management
├── ecommerce/         # Project core configs (settings.py, urls.py, wsgi.py)
├── static/            # Project-level static files (custom style.css)
├── templates/         # Project-level templates (base.html, shop.html, checkout.html)
│
├── manage.py          # Django administrative CLI
├── db.sqlite3         # SQLite database file
├── requirements.txt   # Python package dependencies list
└── README.md          # Setup instructions & developer notes
```

---

## ⚙️ Installation & Setup

Follow these steps to run the application locally on Windows:

### 1. Set Up Virtual Environment
Initialize a Python virtual environment and activate it:
```bash
# Create virtual environment
python -m venv .venv

# Activate virtual environment
.venv\Scripts\Activate.ps1   # PowerShell
# or
.venv\Scripts\activate.bat   # Command Prompt
```

### 2. Install Dependencies
Install packages in the virtual environment:
```bash
pip install -r requirements.txt
```

### 3. Apply Database Migrations
Initialize database tables in SQLite:
```bash
python manage.py makemigrations
python manage.py migrate
```

### 4. Seed Database & Create Admin User
Run the custom seed command to populate dummy data:
```bash
python manage.py seed_db
```
*This command automatically seeds 5 product categories, 11 developer products, and creates an administrative superuser.*

**Admin Credentials:**
* **Username**: `admin`
* **Password**: `adminpassword`

### 5. Start Development Server
Run the local dev server:
```bash
python manage.py runserver
```
Visit http://127.0.0.1:8000/ in your browser to explore the website. To view the administrative dashboard, visit http://127.0.0.1:8000/admin/ and log in with the admin credentials above.

---

## 🧪 Running Automated Tests
To run the automated test suite testing model validations, views status resolution, and rating calculators:
```bash
python manage.py test
```
