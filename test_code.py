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
            "logged_in": [False, False],
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
            # Conversion en string pour éviter les erreurs de type
            if str(user_row.iloc[0]['password']) == str(password):
                return True, user_row.iloc[0]
        return False, None
    except Exception as e:
        st.error(f"Erreur de lecture du fichier CSV : {e}")
        return False, None

# --- 4. GESTION DE LA SESSION ---
if 'connected' not in st.session_state:
    st.session_state['connected'] = False
    st.session_state['user_data'] = None

# --- 5. LOGIQUE D'AFFICHAGE PRINCIPALE ---

# CAS A : L'UTILISATEUR N'EST PAS CONNECTÉ
if not st.session_state['connected']:
    st.title("🔐 Identification")
    st.write("Veuillez entrer vos identifiants pour accéder à l'album.")
    
    # Un seul formulaire avec une clé unique pour éviter l'erreur Duplicate Form
    with st.form(key="formulaire_authentification"):
        user_input = st.text_input("Nom d'utilisateur")
        password_input = st.text_input("Mot de passe", type="password")
        submit = st.form_submit_button("Se connecter")
        
        if submit:
            success, data = check_login(user_input, password_input)
            if success:
                st.session_state['connected'] = True
                st.session_state['user_data'] = data
                st.success("Connexion réussie !")
                st.rerun()
            else:
                st.error("Nom d'utilisateur ou mot de passe incorrect.")

# CAS B : L'UTILISATEUR EST CONNECTÉ
else:
    # --- BARRE LATÉRALE ---
    # On accède au nom SEULEMENT ici pour éviter l'erreur NoneType
    st.sidebar.title(f"👤 {st.session_state['user_data']['name']}")
    st.sidebar.write(f"Rôle : {st.session_state['user_data']['role']}")
    
    choix = st.sidebar.radio("Menu", ["Accueil", "Album Photos"])
    
    st.sidebar.markdown("---")
    
    # Bouton de déconnexion dans le menu
    if st.sidebar.button("Déconnexion"):
        st.session_state['connected'] = False
        st.session_state['user_data'] = None
        st.rerun()

    # --- CONTENU DES PAGES ---
    if choix == "Accueil":
        st.title("🏠 Accueil")
        st.header(f"Bienvenue sur ma page {st.session_state['user_data']['name']} !")
        st.info("Sélectionnez 'Album Photos' dans le menu pour voir les chats.")

    elif choix == "Album Photos":
        st.title("🐱 Bienvenue dans l'album des mes Chats")
        
        # Structure en 3 colonnes pour l'affichage côte à côte
        col1, col2, col3 = st.columns(3)
        
        # Utilisation de try/except au cas où un fichier image manque
        try:
            with col1:
                st.image("chat1.JFIF", caption="Chat n°1", use_container_width=True)
            with col2:
                st.image("chat2.JFIF", caption="Chat n°2", use_container_width=True)
            with col3:
                st.image("chat3.JFIF", caption="Chat n°3", use_container_width=True)
        except Exception as e:
            st.warning("Note : Assurez-vous que chat1.JFIF, chat2.JFIF et chat3.JFIF sont bien dans le dossier.")
            st.error(f"Détail technique : {e}")