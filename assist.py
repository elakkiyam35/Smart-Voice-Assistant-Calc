"""
Smart Voice Assistant Calculator Using Artificial Intelligence
Main entry point for both Web Application Server and Interactive CLI Voice Assistant.
"""

import sys
import argparse
import uvicorn
from core.math_engine import MathEngine
from core.conversational import ConversationManager
from core.speech_nlp import detect_intent

def run_cli_assistant():
    """
    Interactive command-line voice & text assistant using local TTS and SpeechRecognition.
    """
    print("=" * 60)
    print("   Smart Voice Assistant Calculator Using Artificial Intelligence")
    print("   Interactive CLI Mode")
    print("=" * 60)
    print("Initializing components...")

    math_engine = MathEngine(angle_mode='deg')
    manager = ConversationManager(math_engine)
    session_id = "cli_session"

    # Try importing pyttsx3 for local voice output
    tts_engine = None
    try:
        import pyttsx3
        tts_engine = pyttsx3.init()
        tts_engine.setProperty('rate', 170)
    except Exception as e:
        print(f"[Notice] Local pyttsx3 not available ({e}). Running in text-only mode.")

    def speak(text: str):
        print(f"\n🎙️ Assistant: {text}")
        if tts_engine:
            try:
                tts_engine.say(text)
                tts_engine.runAndWait()
            except Exception:
                pass

    welcome_msg = "Hello! Welcome to Smart AI Calculator. How can I help you today? You can choose voice calculation, text calculation, image calculation, or scientific calculation."
    speak(welcome_msg)
    print("\nType your mathematical question or 'exit' to quit.\n")

    while True:
        try:
            user_input = input("\n👤 You: ").strip()
            if not user_input:
                continue

            response = manager.process_message(user_input, session_id=session_id)
            speak(response.get('voice_output', response.get('text_output', '')))

            if response.get('visual_output'):
                vis = response['visual_output']
                print("\n┌" + "─" * 45 + "┐")
                print(f"│ {vis.get('operation_name', 'RESULT'):^43} │")
                print(f"│ {vis.get('expression', ''):^43} │")
                print("├" + "─" * 45 + "┤")
                print(f"│ ANSWER: {vis.get('answer', ''):^35} │")
                print("└" + "─" * 45 + "┘")

            if response.get('status') == 'exit':
                break

            if response.get('follow_up_prompt'):
                print(f"👉 {response['follow_up_prompt']}")
                if response.get('follow_up_options'):
                    opts = ", ".join(f"[{o['id']}] {o['title']}" for o in response['follow_up_options'])
                    print(f"   Options: {opts}")

        except (KeyboardInterrupt, EOFError):
            print("\nGoodbye!")
            break


def run_web_server(host: str = "127.0.0.1", port: int = 8000, reload: bool = False):
    """
    Starts the modern FastAPI Web Server and GUI Dashboard.
    """
    print("\n" + "=" * 65)
    print("   Smart Voice Assistant Calculator Using Artificial Intelligence")
    print(f"   Starting Web Application at: http://{host}:{port}")
    print("   Open your browser to access the complete Voice Calculator Dashboard")
    print("=" * 65 + "\n")
    uvicorn.run("server:app", host=host, port=port, reload=reload)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Smart Voice Assistant Calculator")
    parser.add_argument("--cli", action="store_true", help="Run interactive terminal CLI voice assistant")
    parser.add_argument("--host", default="127.0.0.1", help="Host to bind web server (default: 127.0.0.1)")
    parser.add_argument("--port", type=int, default=8000, help="Port to bind web server (default: 8000)")
    parser.add_argument("--reload", action="store_true", help="Enable auto-reload for development")

    args = parser.parse_args()

    if args.cli:
        run_cli_assistant()
    else:
        run_web_server(host=args.host, port=args.port, reload=args.reload)

