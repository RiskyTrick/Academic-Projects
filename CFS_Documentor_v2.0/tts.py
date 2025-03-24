import pyaudio
import numpy as np
import deepspeech
import wave

class RealTimeSpeechToText:
    def __init__(self, model_path='deepspeech-0.9.3-models.pbmm'):
        self.model = deepspeech.Model(model_path)
        self.chunk = 1024  # Audio chunk size for real-time transcription
        self.rate = 16000  # Sample rate of the audio
        self.pyaudio = pyaudio.PyAudio()

    def start_stream(self):
        """Start real-time transcription from microphone."""
        stream = self.pyaudio.open(format=pyaudio.paInt16, channels=1, rate=self.rate, input=True, frames_per_buffer=self.chunk)
        print("Recording...")
        
        while True:
            data = stream.read(self.chunk)
            audio = np.frombuffer(data, dtype=np.int16)
            text = self.model.stt(audio)
            print(f"Transcription: {text}")

            # Optionally, you could emit the transcribed text to the UI here

    def stop_stream(self):
        """Stop the real-time transcription stream."""
        self.pyaudio.terminate()

# Example usage:
rt_stt = RealTimeSpeechToText(model_path='path_to_model.pbmm')
rt_stt.start_stream()
