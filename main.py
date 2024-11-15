import streamlit as st

# Function to calculate crude risk odds
def calculate_odds(age, smoking, alcohol, activity, diet, bmi, family_history):
    odds = {
        "Cancer": 5,  # Base risk: 5%
        "Diabetes": 7,  # Base risk: 7%
        "Heart Disease": 10,  # Base risk: 10%
        "Respiratory Disease": 4,  # Base risk: 4%
        "Dementia": 6,  # Base risk: 6%
    }

    # Adjust odds based on risk factors
    if age >= 50:
        odds = {k: v + 10 for k, v in odds.items()}  # Add 10% to all conditions for age

    if smoking:
        odds["Cancer"] += 15
        odds["Respiratory Disease"] += 20
        odds["Heart Disease"] += 10

    if alcohol in ['Regularly', 'Heavily']:
        odds["Cancer"] += 5
        odds["Heart Disease"] += 5

    if activity < 2:
        odds["Heart Disease"] += 5
        odds["Diabetes"] += 5

    if diet in ['High in fats/sugars', 'Low in vegetables/fruits']:
        odds["Cancer"] += 5
        odds["Diabetes"] += 10
        odds["Heart Disease"] += 5

    if bmi >= 30:
        odds["Diabetes"] += 15
        odds["Heart Disease"] += 10

    for member, conditions in family_history.items():
        if "Cancer" in conditions:
            odds["Cancer"] += 5
        if "Diabetes" in conditions:
            odds["Diabetes"] += 5
        if "Heart Disease" in conditions:
            odds["Heart Disease"] += 5
        if "Respiratory Disease" in conditions:
            odds["Respiratory Disease"] += 5
        if "Dementia" in conditions:
            odds["Dementia"] += 5

    return {k: min(100, v) for k, v in odds.items()}  # Cap odds at 100%

# Streamlit application
st.title("Preventable Illness Risk Assessment")

# Collect user inputs
age = st.slider("What is your age?", 0, 100, 25)
gender = st.selectbox("What is your gender?", ["Male", "Female", "Non-Binary", "Other"])
smoking = st.checkbox("Do you currently smoke or have a history of smoking?")
alcohol = st.radio("How often do you consume alcohol?", ["Never", "Socially", "Regularly", "Heavily"])
activity = st.slider("How many hours per week do you engage in physical activity?", 0, 20, 5)
diet = st.radio("How would you describe your diet?", ["Balanced", "High in fats/sugars", "Low in vegetables/fruits"])
height = st.number_input("What is your height in centimeters?", min_value=100, max_value=250, value=170)
weight = st.number_input("What is your weight in kilograms?", min_value=30, max_value=200, value=70)
bmi = weight / ((height / 100) ** 2)

# Family history section
st.header("Family History")
family_members = [
    "Parent 1", "Parent 2",
    "Grandparent 1", "Grandparent 2", 
    "Grandparent 3", "Grandparent 4", 
    "Sibling 1", "Sibling 2"
]
family_history = {}
for member in family_members:
    st.subheader(f"Health Conditions for {member}")
    conditions = st.multiselect(
        f"Select known health conditions for {member}:",
        ["Cancer", "Diabetes", "Heart Disease", "Respiratory Disease", "Dementia", "N/A"]
    )
    family_history[member] = conditions

# Calculate odds
odds = calculate_odds(age, smoking, alcohol, activity, diet, bmi, family_history)

# Display risk assessment
st.header("Risk Assessment Results")
st.write("The following are your estimated odds of developing these illnesses based on your inputs:")
for condition, percentage in odds.items():
    st.write(f"- **{condition}**: {percentage}%")
