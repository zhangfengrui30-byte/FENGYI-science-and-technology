# Sereni OpenGL Guided Calm Prototype

Sereni is a high-fidelity desktop prototype for a student mental-health support
application. The interface is rendered with the standard OpenGL API through
Python, PyOpenGL, and GLFW. It includes visual interaction, breathing animation,
image textures, and calming audio playback.

This version intentionally uses an OpenGL desktop client instead of a Flask
webpage, matching the assignment requirement to demonstrate a standard API plus
visual and audio techniques.

## Project Structure

```text
sereni_opengl/
├── main.py
├── ui/
│   ├── window.py
│   ├── renderer.py
│   └── components.py
├── audio/
│   └── player.py
├── assets/
│   ├── sounds/
│   └── textures/
├── screens/
│   ├── home.py
│   ├── reflection.py
│   ├── breathing.py
│   └── resources.py
└── requirements.txt
```

## Features

- OpenGL-rendered desktop app window
- High-fidelity Sereni visual style
- Home, AI Reflection, Guided Breathing, and Campus Resources screens
- Large calming video-style panel rendered as an OpenGL texture
- Soft breathing circle animation with Inhale, Hold, and Exhale states
- Momo companion texture inside the breathing guide
- Play, pause, replay, save, and back interactions
- Looping WAV background music for the breathing guide
- Keyboard support: `Esc` returns home or exits, `Space` starts breathing

## Install

```bash
cd sereni_opengl
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

If you already use the repository-level virtual environment, run:

```bash
source .venv/bin/activate
pip install -r sereni_opengl/requirements.txt
```

## Run

From the repository root:

```bash
source .venv/bin/activate
python sereni_opengl/main.py
```

Or from inside `sereni_opengl/`:

```bash
python main.py
```

## Visual and Audio Techniques

- Visual: gradient backgrounds, transparency blending, rounded OpenGL panels,
  animated breathing circles, texture-loaded imagery, and text rendered as
  OpenGL textures.
- Audio: `simpleaudio` WAV playback with looping calm music during the guided
  breathing screen.

## Nielsen Usability Principles

The prototype supports system status visibility through screen titles and audio
state, user control through back/pause/replay actions, consistency through shared
buttons and cards, error prevention through large click targets, and minimalist
design through a focused calm interaction flow.
