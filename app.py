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
st.title("Voice & Text-Based Recipe Generator 🍳")
st.subheader("Enter or speak your ingredients, and get a recipe!")

# Sidebar for dietary preferences
st.sidebar.header("Dietary Preferences")
dietary_preference = st.sidebar.selectbox(
    "Select Dietary Preference",
    ["None", "Vegetarian", "Vegan", "Gluten-Free", "Low-Carb", "Keto"]
)

# User input: Text or Audio
st.markdown("### 📝 Enter Ingredients (Text) or Upload Audio 🎙️")

# Text input
text_ingredients = st.text_area("Enter ingredients manually (comma-separated):")

# Audio input
audio_file = st.file_uploader("Upload audio (MP3/WAV)", type=["wav", "mp3"])

transcribed_text = ""

# Process audio if uploaded
if audio_file:
    with tempfile.NamedTemporaryFile(delete=False, suffix=".wav") as tmp_file:
        tmp_file.write(audio_file.read())
        tmp_file_path = tmp_file.name

    # Transcribe with Whisper
    with st.spinner("Transcribing your ingredients..."):
        transcribed_text = whisper_model.transcribe(tmp_file_path)["text"]
        st.markdown("### 📝 Transcribed Ingredients")
        st.write(transcribed_text)

# Use text input if provided, otherwise use transcribed text
final_ingredients = text_ingredients if text_ingredients else transcribed_text

# Generate recipe if ingredients are available
if final_ingredients:
    with st.spinner("Generating recipe..."):
        prompt = f"""
        Act as a professional chef. Generate a detailed recipe based on the following ingredients:

        Ingredients: {final_ingredients}

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
