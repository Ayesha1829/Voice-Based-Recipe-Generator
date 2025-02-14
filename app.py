import os
import whisper
import streamlit as st
import google.generativeai as genai
from dotenv import load_dotenv
import tempfile
import json

# Load environment variables
load_dotenv()

# Configure Gemini
genai.configure(api_key=os.getenv("GEMINI_API_KEY"))
model = genai.GenerativeModel('gemini-pro')

# Load Whisper
whisper_model = whisper.load_model("small")

# Load or initialize saved recipes
def load_saved_recipes():
    if os.path.exists("saved_recipes.json"):
        with open("saved_recipes.json", "r") as file:
            return json.load(file)
    return []

def save_recipe(recipe):
    saved_recipes = load_saved_recipes()
    saved_recipes.append(recipe)
    with open("saved_recipes.json", "w") as file:
        json.dump(saved_recipes, file)

# Streamlit UI
st.title("Voice-Based Recipe Generator 🍳")
st.subheader("Speak or upload your ingredients, and get a recipe!")

# Sidebar for dietary preferences
st.sidebar.header("Dietary Preferences")
dietary_preference = st.sidebar.selectbox(
    "Select Dietary Preference",
    ["None", "Vegetarian", "Vegan", "Gluten-Free", "Low-Carb", "Keto"]
)

# User input: Upload audio or speak
st.markdown("### 🎙️ Speak or Upload Ingredients")
audio_file = st.file_uploader("Upload audio (MP3/WAV) or speak your ingredients", type=["wav", "mp3"])

# Process audio
if audio_file:
    # Save uploaded audio to a temporary file
    with tempfile.NamedTemporaryFile(delete=False, suffix=".wav") as tmp_file:
        tmp_file.write(audio_file.read())
        tmp_file_path = tmp_file.name

    # Transcribe with Whisper
    with st.spinner("Transcribing your ingredients..."):
        transcription = whisper_model.transcribe(tmp_file_path)["text"]
        
        # Display transcription
        st.write("---")
        st.markdown("### 📝 Transcribed Ingredients")
        st.write(transcription)

        # Generate recipe with Gemini
        with st.spinner("Generating recipe..."):
            prompt = f"""
            Act as a professional chef. Generate a detailed recipe based on the following ingredients:

            Ingredients: {transcription}

            Dietary Preference: {dietary_preference if dietary_preference != "None" else "None"}

            Provide the recipe in the following format:
            1. Recipe Name
            2. Ingredients (with quantities)
            3. Step-by-Step Instructions
            4. Serving Suggestions
            5. Tips or Variations
            """
            
            response = model.generate_content(prompt)
            recipe = response.text
            
            # Display recipe
            st.write("---")
            st.markdown("### 🍴 Generated Recipe")
            st.markdown(recipe)

            # Save recipe option
            if st.button("💾 Save Recipe"):
                save_recipe(recipe)
                st.success("Recipe saved successfully!")

# View saved recipes
st.write("---")
st.markdown("### 📚 Saved Recipes")
saved_recipes = load_saved_recipes()
if saved_recipes:
    for i, recipe in enumerate(saved_recipes, 1):
        st.markdown(f"#### Recipe {i}")
        st.markdown(recipe)
        st.write("---")
else:
    st.write("No recipes saved yet.")
