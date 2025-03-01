import os
from vosk import Model, KaldiRecognizer
from pydub import AudioSegment
import wave
import json

def transcribe_audio(audio_path):
    """Transcribe audio to text using Vosk, converting MP3 to WAV if needed."""
    try:
        # Convert MP3 to WAV if necessary
        if audio_path.endswith(".mp3"):
            mp3_audio = AudioSegment.from_mp3(audio_path)
            wav_path = audio_path.replace(".mp3", ".wav")
            mp3_audio.export(wav_path, format="wav")
            audio_path = wav_path

        # Use absolute path for the model directory
        model_path = os.path.join(os.getcwd(), "model")
        if not os.path.exists(model_path):
            raise FileNotFoundError("Vosk model directory not found. Ensure 'model' directory exists in the project folder.")

        model = Model(model_path)
        recognizer = KaldiRecognizer(model, 16000)

        # Open the WAV audio file
        with wave.open(audio_path, "rb") as wf:
            if wf.getnchannels() != 1 or wf.getsampwidth() != 2 or wf.getframerate() != 16000:
                raise ValueError("Audio file must be WAV format mono PCM at 16kHz.")

            recognizer.SetWords(True)
            transcript = ""

            while True:
                data = wf.readframes(4000)
                if len(data) == 0:
                    break
                if recognizer.AcceptWaveform(data):
                    result = json.loads(recognizer.Result())
                    transcript += result.get("text", "") + " "

            # Get the final partial result
            result = json.loads(recognizer.FinalResult())
            transcript += result.get("text", "")

        return transcript.strip()

    except Exception as e:
        print(f"Error during transcription: {e}")
        return None
