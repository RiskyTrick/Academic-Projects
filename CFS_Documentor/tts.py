from vosk import Model, KaldiRecognizer
import pyaudio
import json


class RealTimeSpeechToText:
    def __init__(self, model_path="model"):
        """Initialize Vosk real-time transcription."""
        self.model = Model(model_path)
        self.recognizer = KaldiRecognizer(self.model, 16000)
        self.chunk = 1024
        self.rate = 16000
        self.pyaudio = pyaudio.PyAudio()

    def start_stream(self):
        """Start real-time transcription from microphone."""
        stream = self.pyaudio.open(format=pyaudio.paInt16, channels=1, rate=self.rate,
                                   input=True, frames_per_buffer=self.chunk)
        print("Recording and transcribing in real-time...")

        try:
            while True:
                data = stream.read(self.chunk, exception_on_overflow=False)
                if self.recognizer.AcceptWaveform(data):
                    result = json.loads(self.recognizer.Result())
                    print(f"Real-time Transcript: {result.get('text', '')}")
        except KeyboardInterrupt:
            print("Real-time transcription stopped.")
        finally:
            stream.stop_stream()
            stream.close()

    def stop_stream(self):
        """Terminate the transcription stream."""
        self.pyaudio.terminate()
