# Sereni Guided Calm Video Prototype

This project is a high-fidelity mobile app prototype for the Sereni mental
health flow. It recreates the Guided Calm Video page as a runnable Flask web
app with an iPhone-style interface.

## Features

- iPhone-style mobile frame and status bar
- Guided Calm Video screen
- Rounded video player with calming image background
- Soft breathing animation with Inhale, Hold, and Exhale states
- Momo companion in the video corner
- Play, pause, replay, save, volume, and fullscreen interactions
- 1-minute calming background music
- Toast messages and modal feedback
- Voice check-in panel with browser recording and speech recognition support
- Flask backend with a reserved OpenAI API integration endpoint

## Run Locally

```bash
source .venv/bin/activate
python app.py
```

Open:

```text
http://127.0.0.1:5000
```

## Main Files

- `index.html` - frontend UI, styling, and JavaScript interactions
- `app.py` - Flask server and API routes
- `requirements.txt` - Python dependencies
- `assets/sereni-generated-v2/` - local visual and audio assets

## OpenAI Setup

The app works in demo mode without an API key. To enable real AI responses,
create a `.env` file and add:

```text
OPENAI_API_KEY=your_api_key_here
OPENAI_MODEL=gpt-4.1-mini
```
