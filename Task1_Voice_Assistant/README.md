# Task 1 – Personal Voice Assistant (Rhombix Technologies)

A Python voice assistant: speech recognition, text-to-speech, web/Wikipedia search,
weather, notes, calculator, and app/site launcher.

## Setup
    pip install -r requirements.txt
    python voice_assistant.py          # voice mode
    python voice_assistant.py --text   # keyboard mode

PyAudio notes: Windows `pip install pyaudio`; macOS `brew install portaudio` first;
Ubuntu `sudo apt install portaudio19-dev python3-pyaudio espeak`.

## Example commands
- "what time is it" / "what's the date"
- "who is Imran Khan" / "wikipedia Python programming"
- "search for best python projects" / "search youtube lo-fi music"
- "open github" / "open calculator"
- "weather in Peshawar"
- "note buy milk" / "read notes" / "clear notes"
- "calculate 12 plus 8" / "tell me a joke" / "exit"
