"""
Rhombix Technologies - Python Internship
Task 1: Personal Voice Assistant

Usage:
    python voice_assistant.py          # voice mode (microphone)
    python voice_assistant.py --text   # keyboard mode (no microphone needed)
"""

import argparse
import datetime
import logging
import os
import platform
import re
import subprocess
import sys
import webbrowser
from urllib.parse import quote_plus

import requests

try:
    import pyttsx3
except ImportError:
    pyttsx3 = None

try:
    import speech_recognition as sr
except ImportError:
    sr = None

try:
    import wikipedia
except ImportError:
    wikipedia = None

try:
    import pyjokes
except ImportError:
    pyjokes = None

ASSISTANT_NAME = "Rhombix"
NOTES_FILE = "notes.txt"

logging.basicConfig(
    filename="assistant.log",
    level=logging.INFO,
    format="%(asctime)s | %(levelname)s | %(message)s",
)

SITES = {
    "google": "https://www.google.com",
    "youtube": "https://www.youtube.com",
    "github": "https://www.github.com",
    "linkedin": "https://www.linkedin.com",
    "gmail": "https://mail.google.com",
    "stackoverflow": "https://stackoverflow.com",
    "rhombix": "https://www.rhombixtechnologies.com",
}


class VoiceAssistant:
    def __init__(self, text_mode=False):
        self.text_mode = text_mode or sr is None
        self.engine = None
        self.recognizer = None

        if pyttsx3 is not None:
            try:
                self.engine = pyttsx3.init()
                self.engine.setProperty("rate", 170)
            except Exception as exc:  # no audio driver etc.
                logging.warning("TTS init failed: %s", exc)

        if not self.text_mode:
            self.recognizer = sr.Recognizer()
            self.recognizer.pause_threshold = 0.8
            try:
                sr.Microphone()  # verify a mic exists (needs PyAudio)
            except Exception as exc:
                logging.warning("Microphone unavailable: %s", exc)
                print("[!] Microphone not available, switching to text mode.")
                self.text_mode = True

    # ---------- I/O ----------
    def speak(self, text):
        print(f"{ASSISTANT_NAME}: {text}")
        logging.info("SPOKE: %s", text)
        if self.engine:
            try:
                self.engine.say(text)
                self.engine.runAndWait()
            except Exception as exc:
                logging.warning("TTS failed: %s", exc)

    def listen(self):
        """Return lowercase command text, or '' if nothing understood."""
        if self.text_mode:
            try:
                return input("You: ").strip().lower()
            except (EOFError, KeyboardInterrupt):
                return "exit"

        with sr.Microphone() as source:
            print("Listening...")
            self.recognizer.adjust_for_ambient_noise(source, duration=0.5)
            try:
                audio = self.recognizer.listen(source, timeout=6, phrase_time_limit=8)
            except sr.WaitTimeoutError:
                return ""
        try:
            query = self.recognizer.recognize_google(audio, language="en-US")
            print(f"You: {query}")
            logging.info("HEARD: %s", query)
            return query.lower()
        except sr.UnknownValueError:
            return ""
        except sr.RequestError:
            self.speak("Speech service is unreachable. Check your internet connection.")
            return ""

    # ---------- Skills ----------
    def greet(self):
        hour = datetime.datetime.now().hour
        part = "morning" if hour < 12 else "afternoon" if hour < 18 else "evening"
        self.speak(f"Good {part}! I am {ASSISTANT_NAME}, your personal assistant. "
                   f"Say 'help' to hear what I can do.")

    def tell_time(self):
        self.speak("The time is " + datetime.datetime.now().strftime("%I:%M %p"))

    def tell_date(self):
        self.speak("Today is " + datetime.datetime.now().strftime("%A, %d %B %Y"))

    def search_wikipedia(self, topic):
        if wikipedia is None:
            return self.speak("The wikipedia package is not installed.")
        self.speak(f"Searching Wikipedia for {topic}")
        try:
            self.speak(wikipedia.summary(topic, sentences=2, auto_suggest=False))
        except wikipedia.DisambiguationError as e:
            self.speak(f"That is ambiguous. Did you mean {', '.join(e.options[:3])}?")
        except wikipedia.PageError:
            self.speak("I could not find a page on that topic.")
        except Exception as exc:
            logging.error("Wikipedia error: %s", exc)
            self.speak("Something went wrong while searching Wikipedia.")

    def web_search(self, query):
        self.speak(f"Searching Google for {query}")
        webbrowser.open("https://www.google.com/search?q=" + quote_plus(query))

    def youtube_search(self, query):
        self.speak(f"Searching YouTube for {query}")
        webbrowser.open("https://www.youtube.com/results?search_query=" + quote_plus(query))

    def open_site(self, name):
        url = SITES.get(name)
        if url:
            self.speak(f"Opening {name}")
            webbrowser.open(url)
        else:
            self.speak(f"I don't know the website {name}. Try 'search for {name}'.")

    def open_app(self, name):
        system = platform.system()
        apps = {
            "Windows": {"notepad": "notepad", "calculator": "calc", "paint": "mspaint",
                        "command prompt": "cmd", "explorer": "explorer"},
            "Darwin": {"notepad": "TextEdit", "calculator": "Calculator", "terminal": "Terminal"},
            "Linux": {"calculator": "gnome-calculator", "terminal": "x-terminal-emulator",
                      "notepad": "gedit"},
        }.get(system, {})
        target = apps.get(name)
        if not target:
            return self.speak(f"I can't open {name} on this system.")
        try:
            if system == "Darwin":
                subprocess.Popen(["open", "-a", target])
            else:
                subprocess.Popen(target if system == "Windows" else [target],
                                 shell=(system == "Windows"))
            self.speak(f"Opening {name}")
        except Exception as exc:
            logging.error("open_app failed: %s", exc)
            self.speak(f"I couldn't open {name}.")

    def weather(self, city):
        if not city:
            return self.speak("Which city? Say for example: weather in Peshawar.")
        try:
            r = requests.get(f"https://wttr.in/{quote_plus(city)}?format=j1", timeout=8)
            r.raise_for_status()
            cur = r.json()["current_condition"][0]
            self.speak(f"In {city.title()} it is {cur['weatherDesc'][0]['value']}, "
                       f"{cur['temp_C']} degrees Celsius, feels like {cur['FeelsLikeC']}. "
                       f"Humidity is {cur['humidity']} percent.")
        except Exception as exc:
            logging.error("Weather error: %s", exc)
            self.speak("I couldn't fetch the weather right now.")

    def joke(self):
        self.speak(pyjokes.get_joke() if pyjokes else
                   "Why do programmers prefer dark mode? Because light attracts bugs.")

    def add_note(self, text):
        if not text:
            return self.speak("What should I note down?")
        with open(NOTES_FILE, "a", encoding="utf-8") as f:
            f.write(f"[{datetime.datetime.now():%Y-%m-%d %H:%M}] {text}\n")
        self.speak("Note saved.")

    def read_notes(self):
        if not os.path.exists(NOTES_FILE) or os.path.getsize(NOTES_FILE) == 0:
            return self.speak("You have no notes.")
        with open(NOTES_FILE, encoding="utf-8") as f:
            lines = f.read().strip().splitlines()[-5:]
        self.speak(f"Here are your last {len(lines)} notes.")
        for line in lines:
            self.speak(line)

    def clear_notes(self):
        open(NOTES_FILE, "w").close()
        self.speak("All notes cleared.")

    def calculate(self, query):
        words = {"plus": "+", "minus": "-", "times": "*", "multiplied by": "*",
                 "x": "*", "divided by": "/", "over": "/", "into": "*"}
        expr = query
        for w, sym in words.items():
            expr = re.sub(rf"\b{w}\b", sym, expr)
        expr = re.sub(r"[^0-9+\-*/(). ]", "", expr).strip()
        if not re.search(r"\d\s*[+\-*/]\s*\d", expr):
            return self.speak("Try something like: calculate 12 plus 8.")
        try:
            result = eval(expr, {"__builtins__": {}}, {})  # sanitized above
            self.speak(f"The answer is {round(result, 4)}")
        except ZeroDivisionError:
            self.speak("I can't divide by zero.")
        except Exception:
            self.speak("Sorry, I couldn't calculate that.")

    def help(self):
        self.speak("I can tell the time and date, search Wikipedia, Google and YouTube, "
                   "open websites and apps, give weather, tell jokes, calculate, "
                   "and manage notes. Say exit to quit.")

    # ---------- Command router ----------
    def handle(self, q):
        """Return False to stop the assistant."""
        if not q:
            return True

        if any(w in q for w in ("exit", "quit", "goodbye", "stop listening", "bye")):
            self.speak("Goodbye! Have a great day.")
            return False
        if "help" in q or "what can you do" in q:
            self.help()
        elif "time" in q:
            self.tell_time()
        elif "date" in q or "today" in q:
            self.tell_date()
        elif q.startswith(("wikipedia", "who is", "what is", "tell me about")):
            topic = re.sub(r"^(wikipedia|who is|what is|tell me about)\s*", "", q)
            self.search_wikipedia(topic)
        elif "youtube" in q and ("search" in q or "play" in q):
            self.youtube_search(re.sub(r"(search|play|on youtube|youtube|for)", "", q).strip())
        elif q.startswith(("search for", "search", "google")):
            self.web_search(re.sub(r"^(search for|search|google)\s*", "", q))
        elif q.startswith("open "):
            name = q[5:].strip()
            if name in SITES:
                self.open_site(name)
            else:
                self.open_app(name)
        elif "weather" in q:
            m = re.search(r"weather (?:in|of|for)\s+(.+)", q)
            self.weather(m.group(1) if m else "")
        elif "joke" in q:
            self.joke()
        elif q.startswith(("note", "remember", "take a note")):
            self.add_note(re.sub(r"^(take a note|note down|note|remember)\s*(that)?\s*", "", q))
        elif "read" in q and "note" in q:
            self.read_notes()
        elif "clear" in q and "note" in q:
            self.clear_notes()
        elif q.startswith(("calculate", "what's", "how much is")) or re.search(r"\d\s*(plus|minus|times|divided by)", q):
            self.calculate(q)
        elif any(w in q for w in ("hello", "hi", "hey")):
            self.speak("Hello! How can I help you?")
        elif "your name" in q:
            self.speak(f"My name is {ASSISTANT_NAME}.")
        else:
            self.speak("I didn't understand that. Say 'help' to see my commands.")
        return True

    def run(self):
        self.greet()
        running = True
        while running:
            try:
                running = self.handle(self.listen())
            except KeyboardInterrupt:
                self.speak("Goodbye!")
                break
            except Exception as exc:
                logging.exception("Unhandled error: %s", exc)
                self.speak("Something went wrong, but I'm still here.")


def main():
    parser = argparse.ArgumentParser(description="Rhombix Personal Voice Assistant")
    parser.add_argument("--text", action="store_true", help="use keyboard instead of microphone")
    args = parser.parse_args()
    VoiceAssistant(text_mode=args.text).run()


if __name__ == "__main__":
    main()
