import streamlit as st
import secrets
import string
import os
import re

# --- FUNCTIONS --- #

def generate_password(length=14):
    """Generate a secure random password including special characters."""
    characters = string.ascii_letters + string.digits + "!@#$%^&*"
    return ''.join(secrets.choice(characters) for _ in range(length))

def load_word_list(file_path='words.txt'):
    """
    Load words from a local file that contains numbers and words.
    This function extracts only the alphabetical part of tokens.
    
    Example token: "pentagram-61111" -> uses "pentagram".
    """
    words = []
    try:
        with open(file_path, 'r') as f:
            for line in f:
                tokens = line.strip().split()
                for token in tokens:
                    if '-' in token:
                        parts = token.split('-')
                        if parts[0].isalpha():
                            words.append(parts[0])
                    else:
                        if token.isalpha():
                            words.append(token)
        return words
    except FileNotFoundError:
        st.error(f"⚠️ Word list file not found at {os.path.abspath(file_path)}")
        return []

def generate_passphrase(num_words=3):
    """
    Generate a short passphrase from a cleaned word list and append a random two-digit number 
    and a random symbol for extra complexity.
    """
    words = load_word_list()
    if not words:
        return "Error: Could not load word list"
    passphrase = '-'.join(secrets.choice(words) for _ in range(num_words))
    random_number = ''.join(secrets.choice(string.digits) for _ in range(2))
    random_symbol = secrets.choice("!@#$%^&*")
    return passphrase + random_number + random_symbol

def check_password_strength(password):
    """Evaluate password strength based on length, letter case, digits, and special characters."""
    score = 0
    feedback = []
    
    # Length Check
    if len(password) >= 8:
        score += 1
    else:
        feedback.append("Password should be at least 8 characters long.")
    
    # Uppercase & Lowercase Check
    if re.search(r"[A-Z]", password) and re.search(r"[a-z]", password):
        score += 1
    else:
        feedback.append("Include both uppercase and lowercase letters.")
    
    # Digit Check
    if re.search(r"\d", password):
        score += 1
    else:
        feedback.append("Add at least one number (0-9).")
    
    # Special Character Check
    if re.search(r"[!@#$%^&*]", password):
        score += 1
    else:
        feedback.append("Include at least one special character (!@#$%^&*).")
    
    if score == 4:
        strength = "✅ Strong Password!"
    elif score == 3:
        strength = "⚠️ Moderate Password - Consider adding more security features."
    else:
        strength = "❌ Weak Password - " + " ".join(feedback)
    
    return score, strength, feedback

# --- MAIN APP --- #

def main():
    st.set_page_config(page_title="Password Tools", page_icon="🔑", layout="centered")
    st.title("🔑 Password & Passphrase Generator with Strength Meter by ZeeJay🙅‍♂️")
    
    # Sidebar Info and About Section
    st.sidebar.markdown("## About This App")
    st.sidebar.info(
        "A simple and powerful 🔐 password & passphrase generator built with Streamlit 👑. "
        "Generate secure passwords 🔢, memorable short passphrases ✍️, and evaluate password strength 📊. "
        "Enhance your digital security 🔒 with ease! 🔥"
    )
    
    with st.sidebar.expander("📲 Connect with me:"):
        st.markdown("""
- 🔗 [LinkedIn](https://www.linkedin.com/in/zohaib-javd)
- 👨‍💻 [GitHub](https://www.github.com/zohaib-javd)
- 📧 Email: zohaibjaved@gmail.com
        """)
    
    with st.sidebar.expander("🧑‍🏫 Special thanks to all my teachers:"):
        st.markdown("""
- Sir Zia Khan  
- Sir Daniyal Nagori  
- Sir Muhammad Qasim  
- Sir Ameen Alam  
- Sir Aneeq Khatri  
- Sir Okasha Aijaz  
- Sir Muhammad Osama  
- Sir Mubashir Ali  
- Sir Amjad Ali  
- Sir Naeem Hussain  
- Sir Fahad Ghouri  
- Sir Saleem Raza  
- Sir Shaikh Abdul Sami  
- Sir Abdullah arain
        """)
    
    # SESSION STATE SETUP
    if "generated_result" not in st.session_state:
        st.session_state["generated_result"] = ""
    if "generator_type" not in st.session_state:
        st.session_state["generator_type"] = ""
    
    # PASSWORD & PASSPHRASE GENERATOR SECTION
    st.header("🔑 Password & Passphrase Generator")
    col1, col2 = st.columns(2)
    
    with col1:
        st.subheader("Password Settings")
        pw_length = st.slider(
            "Select password length:",
            min_value=8,
            max_value=30,
            value=12,
            help="Recommended minimum is 12 characters"
        )
        if st.button("Generate Password", key="gen_pw"):
            st.session_state.generated_result = generate_password(pw_length)
            st.session_state.generator_type = "password"
        if st.session_state.generator_type == "password" and st.session_state.generated_result:
            st.code(st.session_state.generated_result, language="text")
    
    with col2:
        st.subheader("Passphrase Settings")
        num_words = st.slider(
            "Select number of words:",
            min_value=1,
            max_value=8,
            value=3,
            help="A short passphrase is recommended"
        )
        if st.button("Generate Passphrase", key="gen_passphrase"):
            st.session_state.generated_result = generate_passphrase(num_words)
            st.session_state.generator_type = "passphrase"
        if st.session_state.generator_type == "passphrase" and st.session_state.generated_result:
            st.code(st.session_state.generated_result, language="text")
    
    st.divider()
    st.markdown("""
    ### 🛡️ Security Recommendations:
    - **Passwords:** Use at least 12 characters with a mix of letters, numbers, and special characters.
    - **Passphrases:** Use a short passphrase (2-4 words) for memorability, enhanced with numbers and symbols.
    """)
    
    # PASSWORD STRENGTH METER SECTION
    st.header("🔐 Password Strength Meter")
    user_password = st.text_input("Enter a password to evaluate:", type="password")
    
    if st.button("Check Password Strength", key="check_strength"):
        if user_password:
            score, strength_message, suggestions = check_password_strength(user_password)
            st.write(f"**Strength Score:** {score}/4")
            st.write(strength_message)
            if suggestions:
                st.write("**Suggestions:**")
                for suggestion in suggestions:
                    st.write(f"- {suggestion}")
        else:
            st.warning("Please enter a password to evaluate.")
    
    if user_password:
        score, _, _ = check_password_strength(user_password)
        if score < 4:
            if st.button("Suggest a Strong Password", key="suggest_strong_pw"):
                suggested_pw = generate_password(14)
                st.code(suggested_pw, language="text")

if __name__ == "__main__":
    main()
