import streamlit as st
from google.generativeai import GenerativeModel, configure
from langchain.memory import ConversationBufferMemory

# Set page config
st.set_page_config(page_title="HealthCare Assistant", page_icon="🏥", layout="wide")

# Custom CSS
st.markdown("""
<style>
    .main {
        background-color: black;
    }
    .stApp {
        max-width: 900px;
        margin: 0 auto;
    }
    .stTextInput > div > div > input {
        background-color: white;
    }
    .stButton > button {
        background-color: #4CAF50;
        color: white;
        font-weight: bold;
    }
    .result-card {
        background-color: grey;
        padding: 20px;
        border-radius: 10px;
        box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
        margin-bottom: 20px;
    }
    .disclaimer {
        font-size: 0.8em;
        color: #666;
        font-style: italic;
    }
</style>
""", unsafe_allow_html=True)

# Gemini API setup (make sure to replace with your actual API key)
GEMINI_API_KEY = "AIzaSyDZZEG2EsmqkcCWjmpaZhBRvu5QfinhP64"
configure(api_key=GEMINI_API_KEY)
model = GenerativeModel('gemini-pro')

# Memory setup
symptoms_memory = ConversationBufferMemory(input_key='symptoms', memory_key='chat_history')
medications_memory = ConversationBufferMemory(input_key='condition', memory_key='medication_history')
nutrition_memory = ConversationBufferMemory(input_key='condition', memory_key='nutrition_history')

# Helper functions
def get_gemini_response(prompt):
    response = model.generate_content(prompt)
    return response.text

def analyze_symptoms(symptoms):
    prompt = f"List 2 possible conditions for these symptoms: {symptoms}. Summarize."
    return get_gemini_response(prompt)

def suggest_medications(condition):
    prompt = f"Provide 2 first aid medications for {condition}. Summarize."
    return get_gemini_response(prompt)

def recommend_nutrition(condition):
    prompt = f"Recommend 2 nutritional foods for {condition}. Summarize."
    return get_gemini_response(prompt)

# App header
st.title("🏥 HealthCare Assistant")
st.markdown("Get quick insights about your symptoms and health concerns.")

# User input
with st.form("symptom_form"):
    input_text = st.text_area("Describe your symptoms or health concern:", height=100)
    submit_button = st.form_submit_button("Analyze")

if submit_button and input_text:
    with st.spinner("Analyzing your symptoms..."):
        condition = analyze_symptoms(input_text)
        medications = suggest_medications(condition)
        nutrition = recommend_nutrition(condition)

    # Display results
    st.success("Analysis complete!")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("### 🔍 Possible Conditions")
        st.markdown(f'<div class="result-card">{condition}</div>', unsafe_allow_html=True)
        
        st.markdown("### 💊 First Aid Medications")
        st.markdown(f'<div class="result-card">{medications}</div>', unsafe_allow_html=True)
    
    with col2:
        st.markdown("### 🥗 Nutritional Recommendations")
        st.markdown(f'<div class="result-card">{nutrition}</div>', unsafe_allow_html=True)
    
    # Save to memory
    symptoms_memory.save_context({"symptoms": input_text}, {"output": condition})
    medications_memory.save_context({"condition": condition}, {"output": medications})
    nutrition_memory.save_context({"condition": condition}, {"output": nutrition})

# Conversation history
if st.checkbox("Show Conversation History"):
    st.subheader("Symptoms History")
    st.info(symptoms_memory.buffer)
    
    st.subheader("Medications History")
    st.info(medications_memory.buffer)
    
    st.subheader("Nutrition History")
    st.info(nutrition_memory.buffer)

# Disclaimer
st.markdown("""
<div class="disclaimer">
    <strong>Disclaimer:</strong> This HealthCare Assistant is for informational purposes only. 
    It does not provide medical advice, diagnosis, or treatment. Always seek the advice of your 
    physician or other qualified health provider with any questions you may have regarding a 
    medical condition.
</div>
""", unsafe_allow_html=True)