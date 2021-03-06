import streamlit as st
import pandas as pd
import numpy as np
import pickle
from sklearn.ensemble import RandomForestClassifier

st.write("""
# Heart Failure Prediction App
This app predicts the heart failure!
Data obtained from the [Heart Failure Prediction Dataset](https://www.kaggle.com/datasets/fedesoriano/heart-failure-prediction) by FEDESORIANO.
""")

st.sidebar.header('User Input Features')

st.sidebar.markdown("""
[Example CSV input file](https://raw.githubusercontent.com/panasak/Heart_Failure_Prediction_Project-Classification-/main/data_example.csv)
""")

# Collects user input features into dataframe
uploaded_file = st.sidebar.file_uploader("Upload your input CSV file", type=["csv"])
if uploaded_file is not None:
    input_df = pd.read_csv(uploaded_file)
else:
    def user_input_features():
        chest_pain_types = st.sidebar.selectbox('Chest Pain Type',('ATA','NAP','ASY','TA'), index =1)
        sex = st.sidebar.selectbox('Sex',('M','F'), index=1)
        resting_ecg = st.sidebar.selectbox('Resting electrocardiogram',('Normal','ST','LVH'))
        exercise_agina = st.sidebar.selectbox('Exercise-induced angina',('Y','N'), index=1)
        st_slope = st.sidebar.selectbox('ST slope',('Up','Flat','Down'), index =1)
        age = st.sidebar.slider('Age (year)', 1,100, 49)
        resting_bp = st.sidebar.slider('Resting blood pressure (mm/Hg)', 0,200,160)
        cholesterol= st.sidebar.slider('Cholesterol (mm/dl)', 0,600,180)
        fasting_bs = st.sidebar.slider('Fasting blood sugar (g)', 0,1,0)
        max_hr = st.sidebar.slider('Maximum heart rate', 60,202,156)
        old_peak = st.sidebar.slider('Oldpeak', -3,7,1)
        data = {'Age': age,
                'Sex': sex,
                'ChestPainType': chest_pain_types,
                'RestingBP': resting_bp,
                'Cholesterol': cholesterol,
                'FastingBS': fasting_bs,
                'RestingECG': resting_ecg,
                'MaxHR': max_hr,
                'ExerciseAngina': exercise_agina,
                'Oldpeak': old_peak,
                'ST_Slope': st_slope}
        features = pd.DataFrame(data, index = [0])
        return features
    input_df = user_input_features()

# Combines user input features with entire penguins dataset
# This will be useful for the encoding phase
hearts_raw = pd.read_csv('heart_clean.csv')
hearts = hearts_raw.drop(columns=['HeartDisease'])
df = pd.concat([input_df,hearts],axis=0)

# Encoding of ordinal features
# https://www.kaggle.com/pratik1120/penguin-dataset-eda-classification-and-clustering
encode = ['Sex','ChestPainType','RestingECG','ExerciseAngina','ST_Slope']
for col in encode:
    dummy = pd.get_dummies(df[col], prefix=col)
    df = pd.concat([df,dummy], axis=1)
    del df[col]
df = df[:1] # Selects only the first row (the user input data)

# Displays the user input features
st.subheader('User Input features')

if uploaded_file is not None:
    st.write(df)
else:
    st.write('Awaiting CSV file to be uploaded. Currently using example input parameters (shown below).')
    st.write(df)

# Reads in saved classification model
load_clf = pickle.load(open('heat_failure_rfcmodel.pkl', 'rb'))

# Apply model to make predictions
prediction = load_clf.predict(df)
prediction_proba = load_clf.predict_proba(df)


st.subheader('Prediction')
heart_disease = np.array(['Normal','Heart disease'])
st.write(heart_disease[prediction])

st.subheader('Prediction Probability')
st.write(prediction_proba)
