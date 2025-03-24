import speech_recognition as sr

# Function to transcribe audio to text using SpeechRecognition
def transcribe_audio(audio_path):
    recognizer = sr.Recognizer()

    try:
        # Open the audio file and recognize speech
        with sr.AudioFile(audio_path) as source:
            audio_data = recognizer.record(source)  # Capture the audio data from the file
            print("Transcribing audio...")

            # Use Google's web speech API for transcription
            text = recognizer.recognize_google(audio_data)  # You can also use other engines like Sphinx, etc.
            print("Transcription successful.")
            return text
    except Exception as e:
        print(f"Error during transcription: {e}")
        return None
