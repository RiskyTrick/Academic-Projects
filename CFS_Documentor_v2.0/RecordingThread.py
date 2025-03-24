import pyaudio
import wave
from PyQt5.QtCore import QThread, pyqtSignal

class RecordingThread(QThread):
    frames_captured = pyqtSignal(bytes)

    def __init__(self, format, channels, rate, chunk, mic_index):
        super().__init__()
        self.format = format
        self.channels = channels
        self.rate = rate
        self.chunk = chunk
        self.mic_index = mic_index
        self.running = True

    def run(self):
        """Start recording."""
        audio = pyaudio.PyAudio()
        stream = audio.open(format=self.format, channels=self.channels,
                            rate=self.rate, input=True, frames_per_buffer=self.chunk,
                            input_device_index=self.mic_index)

        while self.running:
            data = stream.read(self.chunk)
            self.frames_captured.emit(data)

        stream.stop_stream()
        stream.close()
        audio.terminate()

    def stop(self):
        """Stop recording."""
        self.running = False
