# Voice-Based Recipe Generator 🍳

A hands-free cooking assistant that generates recipes based on spoken or uploaded ingredients. Built with **Whisper** (speech-to-text), **Gemini** (recipe generation), and **Streamlit** (UI). Includes dietary preference filters and the ability to save favorite recipes.

---

## Features ✨

- **Speech-to-Text**: Upload an audio file or speak your ingredients, and the app will transcribe them using OpenAI's Whisper.
- **Recipe Generation**: Get a detailed recipe based on your ingredients, powered by Google's Gemini.
- **Dietary Preferences**: Filter recipes by dietary preferences (e.g., vegetarian, gluten-free, keto).
- **Save Recipes**: Save your favorite recipes for later access.
- **User-Friendly UI**: Built with Streamlit for a clean and intuitive interface.

---

## How It Works 🛠️

1. **Speak or Upload Ingredients**: Record or upload an audio file listing your ingredients.
2. **Transcription**: Whisper transcribes the audio into text.
3. **Recipe Generation**: Gemini generates a recipe based on the transcribed ingredients and selected dietary preference.
4. **Save Recipes**: Save your favorite recipes for later.
5. **View Saved Recipes**: Access all saved recipes in the app.

---

## Demo 🎥

![Demo](demo.gif)  
*Note: Replace this with an actual GIF or screenshot of your app.*

---

## Installation 🚀

1. Clone the repository:
   ```bash
   git clone https://github.com/your-username/voice-based-recipe-generator.git
   cd voice-based-recipe-generator
   ```
2. Install dependencies:
  ```sh
pip install -r requirements.txt
```
3. Set up environment variables:
Create a .env file in the root directory.
Add your Gemini API key:
```sh
GEMINI_API_KEY=your-api-key-here
```
4. Run the app:
```sh
streamlit run app.py
```

## Tech Stack
Whisper: OpenAI's speech-to-text model for transcribing audio.
Gemini: Google's language model for generating recipes.
Streamlit: For building the web app UI.
Python: Backend logic and integration.

## Contributing 🤝
Contributions are welcome! If you'd like to contribute, please follow these steps:
Fork the repository.
Create a new branch (git checkout -b feature/your-feature).
Commit your changes (git commit -m 'Add some feature').
Push to the branch (git push origin feature/your-feature).
Open a pull request.
