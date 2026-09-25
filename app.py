import streamlit as st
import sqlite3
import random
from datetime import datetime


# ==========================================================
# PAGE CONFIGURATION
# ==========================================================

st.set_page_config(
    page_title="Railway Reservation System",
    page_icon="🚆",
    layout="wide"
)


# ==========================================================
# DATABASE CONNECTION
# ==========================================================

def get_connection():
    return sqlite3.connect("railway.db")


# ==========================================================
# CREATE DATABASE TABLE
# ==========================================================

def create_table():

    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS bookings (

            booking_id INTEGER PRIMARY KEY AUTOINCREMENT,

            pnr TEXT UNIQUE,

            passenger_name TEXT NOT NULL,

            age INTEGER,

            gender TEXT,

            marital_status TEXT,

            train_name TEXT,

            train_number TEXT,

            source TEXT,

            destination TEXT,

            journey_date TEXT,

            boarding_time TEXT,

            coach TEXT,

            seat_number TEXT,

            meal TEXT,

            fare REAL,

            booking_date TEXT

        )
    """)

    conn.commit()
    conn.close()


create_table()


# ==========================================================
# TRAIN DATA
# ==========================================================

trains = {
    "Rajdhani Express": {
        "number": "12951",
        "source": "Mumbai",
        "destination": "Delhi",
        "3 Tier": 1800,
        "2 Tier": 2800,
        "First Class": 4200,
        "General": 700
    },

    "Duronto Express": {
        "number": "12220",
        "source": "Mumbai",
        "destination": "Nagpur",
        "3 Tier": 1400,
        "2 Tier": 2200,
        "First Class": 3500,
        "General": 500
    },

    "Shatabdi Express": {
        "number": "12009",
        "source": "Mumbai",
        "destination": "Ahmedabad",
        "3 Tier": 1200,
        "2 Tier": 1800,
        "First Class": 2800,
        "General": 400
    }
}


# ==========================================================
# HELPER FUNCTIONS
# ==========================================================

def generate_pnr():

    return str(random.randint(1000000000, 9999999999))


def get_booked_seats(train_number, journey_date, coach):

    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
        SELECT seat_number
        FROM bookings
        WHERE train_number = ?
        AND journey_date = ?
        AND coach = ?
    """, (train_number, str(journey_date), coach))

    seats = cursor.fetchall()

    conn.close()

    return [seat[0] for seat in seats]


def save_booking(data):

    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
        INSERT INTO bookings
        (
            pnr,
            passenger_name,
            age,
            gender,
            marital_status,
            train_name,
            train_number,
            source,
            destination,
            journey_date,
            boarding_time,
            coach,
            seat_number,
            meal,
            fare,
            booking_date
        )
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
    """, data)

    conn.commit()
    conn.close()


def get_all_bookings():

    conn = get_connection()

    query = """
        SELECT
            pnr,
            passenger_name,
            train_name,
            train_number,
            source,
            destination,
            journey_date,
            coach,
            seat_number,
            fare
        FROM bookings
        ORDER BY booking_id DESC
    """

    import pandas as pd

    df = pd.read_sql_query(query, conn)

    conn.close()

    return df


def search_booking(pnr):

    conn = get_connection()

    query = """
        SELECT *
        FROM bookings
        WHERE pnr = ?
    """

    import pandas as pd

    df = pd.read_sql_query(
        query,
        conn,
        params=(pnr,)
    )

    conn.close()

    return df


# ==========================================================
# APPLICATION HEADER
# ==========================================================

st.title("🚆 Railway Reservation System")

st.caption(
    "Book your train ticket and retrieve your reservation "
    "details using SQLite3."
)

st.markdown("---")


# ==========================================================
# SIDEBAR
# ==========================================================

page = st.sidebar.radio(
    "Navigation",
    [
        "🎫 Book Ticket",
        "🔎 Retrieve Booking",
        "📋 All Bookings"
    ]
)


# ==========================================================
# BOOK TICKET
# ==========================================================

if page == "🎫 Book Ticket":

    st.header("Passenger & Journey Details")

    with st.form("booking_form"):

        # --------------------------------------------------
        # PASSENGER DETAILS
        # --------------------------------------------------

        st.subheader("👤 Passenger Details")

        col1, col2 = st.columns(2)

        with col1:

            passenger_name = st.text_input(
                "Passenger Name"
            )

            age = st.number_input(
                "Age",
                min_value=5,
                max_value=105,
                value=18
            )

            gender = st.selectbox(
                "Gender",
                [
                    "Male",
                    "Female",
                    "Others"
                ]
            )

        with col2:

            marital_status = st.radio(
                "Marital Status",
                [
                    "Single",
                    "Married",
                    "Separated"
                ],
                horizontal=True
            )

            meal = st.multiselect(
                "Meal Preference",
                [
                    "Vada Pav",
                    "Misal Pav",
                    "Pav Bhaji",
                    "Pulav"
                ],
                max_selections=2
            )

        st.markdown("---")

        # --------------------------------------------------
        # TRAIN DETAILS
        # --------------------------------------------------

        st.subheader("🚆 Train Details")

        train_name = st.selectbox(
            "Select Train",
            list(trains.keys())
        )

        train = trains[train_name]

        col3, col4 = st.columns(2)

        with col3:

            st.text_input(
                "Train Number",
                value=train["number"],
                disabled=True
            )

            st.text_input(
                "Source",
                value=train["source"],
                disabled=True
            )

        with col4:

            st.text_input(
                "Destination",
                value=train["destination"],
                disabled=True
            )

            coach = st.selectbox(
                "Select Coach",
                [
                    "3 Tier",
                    "2 Tier",
                    "First Class",
                    "General"
                ]
            )

        st.markdown("---")

        # --------------------------------------------------
        # JOURNEY DETAILS
        # --------------------------------------------------

        st.subheader("🛤️ Journey Details")

        col5, col6 = st.columns(2)

        with col5:

            journey_date = st.date_input(
                "Journey Date"
            )

            boarding_time = st.time_input(
                "Boarding Time"
            )

        with col6:

            # ----------------------------------------------
            # SEAT INFORMATION
            # ----------------------------------------------

            booked_seats = get_booked_seats(
                train["number"],
                journey_date,
                coach
            )

            available_seats = [
                str(i)
                for i in range(1, 21)
                if str(i) not in booked_seats
            ]

            seat_number = st.selectbox(
                "Select Seat",
                available_seats
            )

        st.markdown("---")

        # --------------------------------------------------
        # FARE
        # --------------------------------------------------

        fare = train[coach]

        st.subheader("💰 Fare Details")

        fare_col1, fare_col2 = st.columns(2)

        with fare_col1:

            st.metric(
                "Base Fare",
                f"₹ {fare}"
            )

        with fare_col2:

            st.metric(
                "Selected Seat",
                seat_number
            )

        st.markdown("---")

        # --------------------------------------------------
        # SUBMIT
        # --------------------------------------------------

        submitted = st.form_submit_button(
            "🎫 Confirm Booking",
            use_container_width=True
        )


    # ======================================================
    # PROCESS BOOKING
    # ======================================================

    if submitted:

        if passenger_name.strip() == "":

            st.error(
                "Please enter passenger name."
            )

        elif len(available_seats) == 0:

            st.error(
                "No seats are available for this coach."
            )

        else:

            pnr = generate_pnr()

            booking_date = datetime.now().strftime(
                "%Y-%m-%d %H:%M:%S"
            )

            meal_value = ", ".join(meal)

            data = (
                pnr,
                passenger_name,
                age,
                gender,
                marital_status,
                train_name,
                train["number"],
                train["source"],
                train["destination"],
                str(journey_date),
                str(boarding_time),
                coach,
                seat_number,
                meal_value,
                fare,
                booking_date
            )

            try:

                save_booking(data)

                st.success(
                    "✅ Ticket booked successfully!"
                )

                st.balloons()

                # ------------------------------------------
                # TICKET
                # ------------------------------------------

                st.subheader("🎫 Booking Confirmation")

                ticket_col1, ticket_col2 = st.columns(2)

                with ticket_col1:

                    st.write(
                        f"**PNR Number:** {pnr}"
                    )

                    st.write(
                        f"**Passenger:** {passenger_name}"
                    )

                    st.write(
                        f"**Age:** {age}"
                    )

                    st.write(
                        f"**Gender:** {gender}"
                    )

                    st.write(
                        f"**Train:** {train_name}"
                    )

                    st.write(
                        f"**Train Number:** {train['number']}"
                    )

                with ticket_col2:

                    st.write(
                        f"**From:** {train['source']}"
                    )

                    st.write(
                        f"**To:** {train['destination']}"
                    )

                    st.write(
                        f"**Journey Date:** {journey_date}"
                    )

                    st.write(
                        f"**Coach:** {coach}"
                    )

                    st.write(
                        f"**Seat:** {seat_number}"
                    )

                    st.write(
                        f"**Fare:** ₹ {fare}"
                    )

            except sqlite3.IntegrityError:

                st.error(
                    "Booking failed. Please try another seat."
                )


# ==========================================================
# RETRIEVE BOOKING
# ==========================================================

elif page == "🔎 Retrieve Booking":

    st.header("🔎 Retrieve Booking")

    pnr = st.text_input(
        "Enter PNR Number"
    )

    if st.button(
        "Search Booking",
        use_container_width=True
    ):

        if pnr.strip() == "":

            st.warning(
                "Please enter PNR number."
            )

        else:

            booking = search_booking(pnr)

            if booking.empty:

                st.error(
                    "No booking found for this PNR."
                )

            else:

                st.success(
                    "Booking found successfully!"
                )

                st.dataframe(
                    booking,
                    use_container_width=True,
                    hide_index=True
                )


# ==========================================================
# ALL BOOKINGS
# ==========================================================

elif page == "📋 All Bookings":

    st.header("📋 Booking Records")

    bookings = get_all_bookings()

    if bookings.empty:

        st.info(
            "No bookings available."
        )

    else:

        st.dataframe(
            bookings,
            use_container_width=True,
            hide_index=True
        )