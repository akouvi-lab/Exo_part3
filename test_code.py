import streamlit as st
import pandas as pd
import os

# --- 1. CONFIGURATION DE LA PAGE ---
st.set_page_config(page_title="App Chat Sécurisée", layout="wide")

# --- 2. CRÉATION DU CSV (SI INEXISTANT) ---
def initialiser_csv():
    if not os.path.exists("users.csv"):
        data = {
            "name": ["admin", "akouvi"],
            "password": ["admin123", "chat2024"],
            "email": ["admin@test.com", "akouvi@test.com"],
            "failed_login_attemps": [0, 0],
            "role": ["admin", "user"]
        }
        pd.DataFrame(data).to_csv("users.csv", index=False)

initialiser_csv()

# --- 3. FONCTIONS DE CONNEXION ---
def check_login(username, password):
    try:
        df = pd.read_csv("users.csv")
        user_row = df[df['name'] == username]
        if not user_row.empty:
            if str(user_row.iloc[0]['password']) == str(password):
                return True, user_row.iloc[0]
        return False, None
    except Exception as e:
        return False, None

# --- 4. GESTION DE LA SESSION ---
if 'connected' not in st.session_state:
    st.session_state['connected'] = False
    st.session_state['user_data'] = None

# --- 5. LOGIQUE D'AFFICHAGE ---

if not st.session_state['connected']:
    # --- PAGE DE CONNEXION ---
    st.title("🔐 Connexion")
    st.text("identifiant : akouvi , Mot de passe = chat2014")
    # Utilisation d'une clé unique pour éviter l'erreur Duplicate Form
    with st.form(key="login_unique_form"):
        user_input = st.text_input("Nom d'utilisateur")
        password_input = st.text_input("Mot de passe", type="password")
        submit = st.form_submit_button("Se connecter")
        
        if submit:
            success, data = check_login(user_input, password_input)
            if success:
                st.session_state['connected'] = True
                st.session_state['user_data'] = data
                st.rerun()
            else:
                st.error("Identifiants incorrects")

else:
    # --- INTERFACE CONNECTÉE ---
    st.sidebar.title(f"👤 {st.session_state['user_data']['name']}")
    choix = st.sidebar.radio("Menu", ["Accueil", "Album Photos"])
    
    st.sidebar.markdown("---")
    if st.sidebar.button("Déconnexion"):
        st.session_state['connected'] = False
        st.session_state['user_data'] = None
        st.rerun()

    if choix == "Accueil":
        st.title("🏠 Accueil")
        st.write(f"Bienvenue {st.session_state['user_data']['name']} !")

    elif choix == "Album Photos":
        st.title("🐱 Bienvenue sur l'album de mes chats")
        
        # Définition des URLs GitHub Raw
        chat1_url = "https://raw.githubusercontent.com/akouvi-lab/Exo_part3/refs/heads/main/chat1.jfif"
        chat2_url = "https://raw.githubusercontent.com/akouvi-lab/Exo_part3/refs/heads/main/chat2.jfif"
        chat3_url = "https://raw.githubusercontent.com/akouvi-lab/Exo_part3/refs/heads/main/chat3.jfif"
        
        # Affichage en 3 colonnes
        col1, col2, col3 = st.columns(3)
        
        with col1:
            st.image(chat1_url, caption="Chat 1", use_container_width=True)
        with col2:
            st.image(chat2_url, caption="Chat 2", use_container_width=True)
        with col3:
            st.image(chat3_url, caption="Chat 3", use_container_width=True)


