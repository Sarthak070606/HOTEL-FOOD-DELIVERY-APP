import streamlit as st
import pandas as pd

if "hotel" not in st.session_state:
    class User:
        def __init__(self, unique_id, name, email, contact, city, password):
            self.id = unique_id
            self.name = name
            self.email = email
            self.contact = contact
            self.city = city
            self.password = password
            self.bill = 0

    class Hotel:
        count = 1
        userlist = []

        veg_menu = {
            1: ("Palak Paneer", 350),
            2: ("Aloo Gobi", 220),
            3: ("Paneer Masala", 260),
            4: ("Kaju Kari", 210),
            5: ("Fried Dal", 200),
            6: ("Sadi Roti", 15),
            7: ("Tika Roti", 25),
            8: ("Nan Roti", 50),
            9: ("Fried Rice", 120),
            10: ("Masala Maggi", 120)
        }

        nonveg_menu = {
            1: ("Mutton", 350),
            2: ("Fish", 1000),
            3: ("Masala Chicken", 210),
            4: ("Chicken Koliwala", 200)
        }

        def register_user(self, name, email, contact, city, password):
            user = User(Hotel.count, name, email, contact, city, password)
            self.userlist.append(user)
            Hotel.count += 1
            return user

        def login_user(self, email, password):
            for user in self.userlist:
                if user.email == email and user.password == password:
                    return user
            return None

    st.session_state.hotel = Hotel()

hotel = st.session_state.hotel

# --- Streamlit UI ---
st.set_page_config(page_title="Hotel Deepali", page_icon="🏨", layout="centered")
st.title("🏨 Hotel Deepali")
st.caption("Order delicious Veg & Non-Veg food online!")

# --- Sidebar Navigation ---
menu = ["Home", "Register", "Login", "Logout"]
choice = st.sidebar.selectbox("Navigation", menu)

# --- Home Page ---
if choice == "Home":
    st.image("Hotel1", caption="Welcome to Hotel Deepali", use_container_width=True)
    st.subheader("🍽️ Enjoy Delicious Veg & Non-Veg Food")
    st.write("Please register or login to place your order.")

# --- Register Page ---
elif choice == "Register":
    st.subheader("📝 Register New User")
    with st.form("register_form"):
        name = st.text_input("Name")
        email = st.text_input("Email")
        contact = st.text_input("Contact")
        city = st.text_input("City")
        password = st.text_input("Password", type="password")
        submit = st.form_submit_button("Register")
        if submit:
            user = hotel.register_user(name, email, contact, city, password)
            st.success(f"User {user.name} registered successfully!")

# --- Login Page ---
elif choice == "Login":
    st.subheader("🔑 Login")
    with st.form("login_form"):
        email = st.text_input("Email")
        password = st.text_input("Password", type="password")
        login_btn = st.form_submit_button("Login")

    if login_btn:
        user = hotel.login_user(email, password)
        if user:
            st.session_state.user = user
            st.success(f"Welcome back, {user.name}!")
        else:
            st.error("Invalid email or password.")

elif choice == "Logout":
    st.session_state.user = None
    st.success("You have been logged out.")

if "user" in st.session_state and st.session_state.user is not None:
    user = st.session_state.user
    st.subheader(f"🍴 Welcome {user.name}, place your order:")

    with st.form("order_form"):
        veg_selections = {}
        nonveg_selections = {}

        st.markdown("### 🌱 Veg Menu")
        for id, (dish, price) in hotel.veg_menu.items():
            qty = st.number_input(f"{dish} - ₹{price}", min_value=0, step=1, key=f"veg{id}")
            veg_selections[id] = qty

        st.markdown("### 🍗 Non-Veg Menu")
        for id, (dish, price) in hotel.nonveg_menu.items():
            qty = st.number_input(f"{dish} - ₹{price}", min_value=0, step=1, key=f"nonveg{id}")
            nonveg_selections[id] = qty

        place_order = st.form_submit_button("Place Order")

    if place_order:
        user.bill = 0  # Reset previous bill
        ordered_items = []

        for id, qty in veg_selections.items():
            if qty > 0:
                dish, price = hotel.veg_menu[id]
                total = price * qty
                user.bill += total
                ordered_items.append((dish, qty, total))

        for id, qty in nonveg_selections.items():
            if qty > 0:
                dish, price = hotel.nonveg_menu[id]
                total = price * qty
                user.bill += total
                ordered_items.append((dish, qty, total))

        if user.bill > 0:
            st.success(f"✅ Order placed successfully! Total bill: ₹{user.bill}")
            st.info("🍽️ Your order has been delivered!")
            st.balloons()

            # Show order summary
            st.markdown("### 🧾 Order Summary")
            order_df = pd.DataFrame(ordered_items, columns=["Item", "Quantity", "Price (₹)"])
            st.table(order_df)

            bill_text = f"--- Hotel Deepali Bill ---\n"
            bill_text += f"Name: {user.name}\nEmail: {user.email}\nContact: {user.contact}\nCity: {user.city}\n\n"
            bill_text += "Item\tQuantity\tPrice\n"
            for item, qty, total in ordered_items:
                bill_text += f"{item}\t{qty}\t₹{total}\n"
            bill_text += f"\nTotal Bill: ₹{user.bill}"

            # Download button
            st.download_button(
                label="💾 Download Bill",
                data=bill_text,
                file_name="HotelDeepali_Bill.txt",
                mime="text/plain"
            )
        else:
            st.warning("⚠️ You haven't selected any items.")
