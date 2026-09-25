# 🚆 Railway Reservation System

A simple **Railway Reservation System** developed using **Python, Streamlit, and SQLite3**.

The application allows users to enter passenger and journey details, select a train, coach, and seat, automatically calculate the fare, and store the booking information in a SQLite database. Users can also retrieve their booking details using their PNR number.

---

## 📌 Project Overview

The Railway Reservation System demonstrates how a Python application can be connected with a database and exposed through a user-friendly Streamlit web interface.

### Main Workflow

```text
User
  ↓
Streamlit Web Application
  ↓
Passenger & Journey Details
  ↓
Train / Coach / Seat Selection
  ↓
Fare Calculation
  ↓
SQLite3 Database
  ↓
Booking Confirmation
  ↓
PNR Generation
  ↓
Booking Retrieval
```

---

## ✨ Features

* 👤 Passenger registration
* 🚆 Train selection
* 🛤️ Source and destination information
* 📅 Journey date selection
* ⏰ Boarding time selection
* 💺 Coach selection
* 🎫 Seat selection
* 🔢 Automatic PNR generation
* 💰 Automatic fare calculation
* 🗄️ SQLite3 database storage
* 🔎 Booking retrieval using PNR
* 📋 View all booking records
* 🚫 Prevents already-booked seats from being selected
* 📊 Display booking records using Streamlit

---

## 🛠️ Technologies Used

| Technology | Purpose                               |
| ---------- | ------------------------------------- |
| Python     | Application programming               |
| Streamlit  | Web application frontend              |
| SQLite3    | Database                              |
| Pandas     | Display and retrieve database records |
| Random     | PNR generation                        |
| Datetime   | Booking date and time                 |

---

## 📂 Project Structure

```text
RailwayReservation/
│
├── app.py
├── railway.db
└── README.md
```

> `railway.db` is automatically created when the application is executed for the first time.

---

## ⚙️ Installation

### 1. Clone the Repository

```bash
git clone <repository-url>
```

Navigate to the project directory:

```bash
cd RailwayReservation
```

---

### 2. Create a Virtual Environment

```bash
python -m venv venv
```

Activate the virtual environment.

#### Windows

```bash
venv\Scripts\activate
```

#### macOS / Linux

```bash
source venv/bin/activate
```

---

### 3. Install Required Libraries

```bash
pip install streamlit pandas
```

SQLite3 is included with standard Python installations, so normally no separate installation is required.

---

## ▶️ Run the Application

Execute:

```bash
streamlit run app.py
```

The Streamlit application will open in your default web browser.

---

# 🖥️ Application Modules

## 1. 🎫 Book Ticket

The user enters:

* Passenger Name
* Age
* Gender
* Marital Status
* Meal Preference
* Train
* Coach
* Journey Date
* Boarding Time
* Seat Number

The application automatically determines the fare based on the selected train and coach.

Example:

```text
Train       : Rajdhani Express
Train No.   : 12951
Coach       : 3 Tier
Seat        : 10
Fare        : ₹1800
```

After successful booking, the application generates a unique PNR number.

---

## 2. 💺 Seat Availability

The application checks SQLite before displaying available seats.

For example:

```text
Total Seats

1  2  3  4  5  6  7  8  9  10
11 12 13 14 15 16 17 18 19 20
```

If seats `3`, `7`, and `15` are already booked:

```text
Booked Seats

3
7
15
```

The application removes these seats from the available selection.

Therefore, another passenger cannot select an already-booked seat for the same:

```text
Train + Journey Date + Coach
```

---

# 🗄️ Database

The application uses SQLite3.

Database:

```text
railway.db
```

Table:

```text
bookings
```

### Database Schema

| Column         | Data Type | Description       |
| -------------- | --------- | ----------------- |
| booking_id     | INTEGER   | Primary key       |
| pnr            | TEXT      | Unique PNR        |
| passenger_name | TEXT      | Passenger name    |
| age            | INTEGER   | Passenger age     |
| gender         | TEXT      | Passenger gender  |
| marital_status | TEXT      | Marital status    |
| train_name     | TEXT      | Train name        |
| train_number   | TEXT      | Train number      |
| source         | TEXT      | Boarding station  |
| destination    | TEXT      | Destination       |
| journey_date   | TEXT      | Journey date      |
| boarding_time  | TEXT      | Boarding time     |
| coach          | TEXT      | Selected coach    |
| seat_number    | TEXT      | Selected seat     |
| meal           | TEXT      | Meal preference   |
| fare           | REAL      | Ticket fare       |
| booking_date   | TEXT      | Booking timestamp |

---

# 🔎 Booking Retrieval

Users can retrieve their booking by entering their PNR number.

Example:

```text
Enter PNR Number:

8392746123

        ↓

Search Booking

        ↓

Passenger Details
Train Details
Journey Details
Coach
Seat
Fare
```

The application executes a database query similar to:

```sql
SELECT *
FROM bookings
WHERE pnr = ?;
```

---

# 📋 View All Bookings

The **All Bookings** section retrieves all booking records from SQLite3 and displays them in a Streamlit dataframe.

Example:

```text
PNR        Passenger       Train              Coach     Seat    Fare
--------------------------------------------------------------------
8392746123 Rahul Sharma    Rajdhani Express   3 Tier     5     1800
7293816452 Priya Shah      Duronto Express    2 Tier     8     2200
9182736451 Amit Patil      Shatabdi Express   General   12      400
```

---

# 🚆 Sample Train Data

The current application contains sample train information.

### Rajdhani Express

```text
Train Number : 12951
Source       : Mumbai
Destination  : Delhi
```

| Coach       |  Fare |
| ----------- | ----: |
| 3 Tier      | ₹1800 |
| 2 Tier      | ₹2800 |
| First Class | ₹4200 |
| General     |  ₹700 |

### Duronto Express

```text
Train Number : 12220
Source       : Mumbai
Destination  : Nagpur
```

| Coach       |  Fare |
| ----------- | ----: |
| 3 Tier      | ₹1400 |
| 2 Tier      | ₹2200 |
| First Class | ₹3500 |
| General     |  ₹500 |

### Shatabdi Express

```text
Train Number : 12009
Source       : Mumbai
Destination  : Ahmedabad
```

| Coach       |  Fare |
| ----------- | ----: |
| 3 Tier      | ₹1200 |
| 2 Tier      | ₹1800 |
| First Class | ₹2800 |
| General     |  ₹400 |

> The train and fare information in this project is sample data intended for learning and demonstration.

---

# 🔐 Booking Validation

The application performs basic validation before saving a booking.

### Passenger Name

```python
if passenger_name.strip() == "":
    st.error("Please enter passenger name.")
```

### Seat Availability

The application checks whether seats are available before confirming the booking.

### Duplicate Booking

The database uses a unique constraint on the PNR:

```sql
pnr TEXT UNIQUE
```

---

# 🧠 Concepts Demonstrated

This project is useful for learning the integration of:

### Python

* Variables
* Conditional statements
* Functions
* Dictionaries
* Lists
* Exception handling
* Modules

### Streamlit

* `st.title()`
* `st.text_input()`
* `st.number_input()`
* `st.selectbox()`
* `st.radio()`
* `st.multiselect()`
* `st.date_input()`
* `st.time_input()`
* `st.form()`
* `st.columns()`
* `st.button()`
* `st.dataframe()`
* `st.success()`
* `st.error()`

### SQLite3

* Database connection
* Creating tables
* INSERT
* SELECT
* WHERE
* Parameterized queries
* UNIQUE constraints
* Fetching records

### Pandas

* Reading SQL query results
* Creating DataFrames
* Displaying tabular data

---

# 🔄 CRUD Extension

The current project primarily demonstrates:

```text
CREATE
  ↓
INSERT BOOKING
  ↓
READ
  ↓
RETRIEVE BOOKING
```

It can be extended into a complete CRUD application:

```text
C → Create Booking
R → Read Booking
U → Update Booking
D → Delete / Cancel Booking
```

---

# 🚀 Future Enhancements

The project can be extended with:

* 🎫 Ticket cancellation
* 🔄 Ticket modification
* 👨‍👩‍👧 Multiple passengers per booking
* 💳 Payment module
* 📧 Email confirmation
* 📱 SMS notification
* 🔐 User login and authentication
* 👨‍💼 Admin dashboard
* 🚆 Train search
* 🛤️ Station management
* 💺 Visual seat map
* 📊 Booking analytics
* 📥 Download ticket as PDF
* 🧾 Generate printable ticket
* 🗃️ Separate Passenger, Train, Coach and Booking tables
* 🔗 Foreign key relationships
* 🏗️ Object-Oriented Programming architecture

---

# 📊 Recommended Database Architecture

For a more advanced version, instead of keeping everything in one `bookings` table, the database can be normalized:

```text
Passenger
   │
   │
   ▼
Booking ─────────── Train
   │
   ▼
Seat
   │
   ▼
Payment
```

Possible tables:

```text
passengers
trains
coaches
seats
bookings
payments
```

This structure would make the project closer to a real-world database application.

---

# 🎯 Learning Objective

The primary objective of this project is to demonstrate how to build a database-driven web application using Python.

By completing this project, learners will understand:

```text
Python
  ↓
Streamlit
  ↓
User Input
  ↓
Business Logic
  ↓
SQLite3
  ↓
SQL Queries
  ↓
Database Records
  ↓
Data Retrieval
  ↓
Streamlit Display
```

---

# 👨‍💻 Author

**Chandan**

Python | Data Science | Streamlit | SQL | Machine Learning

---

# 📜 License

This project is created for **educational and demonstration purposes**.

[alt text](diagram.png)