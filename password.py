import streamlit as st
import re
import random
import string

# Function to check password strength
def check_password_strength(password):
    score = 0
    feedback = []

    # Length Check
    if len(password) >= 8:
        score += 1
    else:
        feedback.append("❌ Password should be at least 8 characters long.")

    # Upper & Lowercase Check
    if re.search(r"[A-Z]", password) and re.search(r"[a-z]", password):
        score += 1
    else:
        feedback.append("❌ Include both uppercase and lowercase letters.")

    # Digit Check
    if re.search(r"\d", password):
        score += 1
    else:
        feedback.append("❌ Add at least one number (0-9).")

    # Special Character Check
    if re.search(r"[!@#$%^&*]", password):
        score += 1
    else:
        feedback.append("❌ Include at least one special character (!@#$%^&*).")

    return score, feedback

# Function to generate strong passwords
def generate_strong_password(length=12, count=5):
    passwords = []
    for _ in range(count):
        lower = random.choice(string.ascii_lowercase)
        upper = random.choice(string.ascii_uppercase)
        digit = random.choice(string.digits)
        special = random.choice("!@#$%^&*")

        all_characters = string.ascii_letters + string.digits + "!@#$%^&*"
        password = lower + upper + digit + special + ''.join(random.choices(all_characters, k=length-4))
        password = ''.join(random.sample(password, len(password)))
        passwords.append(password)
    return passwords

# Streamlit UI
st.set_page_config(page_title="Colorful Password Strength Meter", page_icon="🔒", layout="wide")
st.title("  Password Strength Meter")

# Password input with real-time feedback
password = st.text_input("Enter your password:", type="password", placeholder="Type your password here...")

if password:
    score, feedback = check_password_strength(password)
    strength_label = {0: "Weak", 1: "Moderate", 2: "Strong"}
    strength_color = {0: "red", 1: "orange", 2: "green"}
    
    # Display strength indicator
    st.markdown(f"<h3 style='color: {strength_color[score]}; text-align: center;'>Password Strength: {strength_label[score]}</h3>", unsafe_allow_html=True)
    
    # Display feedback
    for message in feedback:
        st.write(message)

# Password history
if 'password_history' not in st.session_state:
    st.session_state.password_history = []

if st.button("Check Password"):
    if password not in st.session_state.password_history:
        st.session_state.password_history.append(password)
        st.success("Password checked and added to history.")
    else:
        st.warning("This password has been checked before!")

# Generate strong passwords
st.subheader("✨ Generate Strong Passwords")
length = st.number_input("Enter desired password length (minimum 8):", min_value=8, value=12)
count = st.number_input("Number of passwords to generate:", min_value=1, value=5)

if st.button("Generate Passwords"):
    strong_passwords = generate_strong_password(length, count)
    st.success("Generated Strong Passwords:")
    for pwd in strong_passwords:
        st.markdown(f"<p style='font-size: 18px; color: blue;'>{pwd}</p>", unsafe_allow_html=True)

# Display password history
st.subheader("📜 Password History")
if st.session_state.password_history:
    for pwd in st.session_state.password_history:
        st.markdown(f"<p style='font-size: 16px; color: purple;'>{pwd}</p>", unsafe_allow_html=True)
else:
    st.write("No passwords checked yet.")