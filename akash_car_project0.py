# -*- coding: utf-8 -*-
"""Akash car project0.ipynb

Automatically generated by Colab.

Original file is located at
    https://colab.research.google.com/drive/1bhOH7V3ZA48YShplucJ9tBVYbmGSzCbP
"""

import streamlit as st
import pandas as pd
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score
import base64

def set_background(image_file):
    try:
        with open(image_file, "rb") as image:
            encoded = base64.b64encode(image.read()).decode()
        st.markdown(
            f"""
            <style>
            .stApp {{
                background-image: url("data:image/jpg;base64,{encoded}");
                background-size: cover;
                background-attachment: fixed;
            }}
            .stApp::before {{
                content: "";
                position: fixed;
                top: 0;
                left: 0;
                height: 100%;
                width: 100%;
                background-color: rgba(255,255,255,0.4);  /* white overlay */
                z-index: -1;
            }}
            </style>
            """,
            unsafe_allow_html=True
        )
    except FileNotFoundError:
        st.warning("⚠️ Background image not found. Running with default background.")

set_background("car_bg.jpg")  # You can rename this to your own image file
# App Title
st.title("🚗 Car Evaluation Classifier using Random Forest & Streamlit")
st.write("Predict the car condition using Machine Learning based on various features.")
st.markdown("👩‍💻 Created by: Akash")

# File uploader
uploaded_file = st.file_uploader("📁 Upload your car.csv file", type=['csv'])

@st.cache_data
def load_data():
    url = "https://archive.ics.uci.edu/ml/machine-learning-databases/car/car.data"
    columns = ['buying', 'maint', 'doors', 'persons', 'lug_boot', 'safety', 'class']
    return pd.read_csv(url, names=columns)

df = load_data()




# Encoding categorical columns if needed
df_encoded = df.apply(lambda col: pd.factorize(col)[0])

# Splitting data
X = df_encoded.iloc[:, :-1]
y = df_encoded.iloc[:, -1]

X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# Model
model = RandomForestClassifier()
model.fit(X_train, y_train)

# Accuracy
accuracy = model.score(X_test, y_test)
st.success(f"🎯 Model Accuracy: {accuracy*100:.2f}%")

# Prediction UI
st.subheader("🧪 Predict Car Condition")

input_data = []
for column in df.columns[:-1]:
    value = st.selectbox(f"{column}", df[column].unique())
    input_data.append(value)

      # Convert input to encoded form
input_encoded = [pd.Series(df[column].unique()).tolist().index(val) for column, val in zip(df.columns[:-1], input_data)]
prediction = model.predict([input_encoded])[0]

      # Decode prediction
decoded_label = pd.Series(df[df.columns[-1]].unique())[prediction]
st.success(f"✅ Predicted Condition: {decoded_label}")

st.markdown("❤ **Made by Akash **")
