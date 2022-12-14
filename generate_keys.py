import pickle
from pathlib import Path

import streamlit_authenticator as stauth

names = ["admin"]
usernames = ["admin"]
passwords = ["admin"]

hashed_passwords = stauth.Hasher(passwords).generate()

file_path = Path(__file__).parent / "hashed_password.pkl"
with file_path.open("wb") as file:
    pickle.dump(hashed_passwords, file)