import os
import pyaudio
import wave
from RecordingThread import RecordingThread

class VoiceControls:
    def __init__(self):
        self.recording_thread = None
        self.format = pyaudio.paInt16
        self.channels = 1
        self.rate = 44100
        self.chunk = 1024
        self.frames = []
        self.mic_index = None

    def get_available_microphones(self):
        """Fetch and return available microphones."""
        audio = pyaudio.PyAudio()
        devices = [
            (i, audio.get_device_info_by_index(i).get('name'))
            for i in range(audio.get_device_count())
        ]
        audio.terminate()
        return devices

    def start_recording(self, mic_index):
        """Start the recording with the selected microphone."""
        self.mic_index = mic_index
        self.frames = []
        self.recording_thread = RecordingThread(
            self.format, self.channels, self.rate, self.chunk, self.mic_index
        )
        self.recording_thread.frames_captured.connect(self.capture_frame)
        self.recording_thread.start()
        return True

    def capture_frame(self, data):
        """Capture individual audio frames."""
        self.frames.append(data)

    def stop_recording(self):
        """Stop the recording process."""
        if self.recording_thread and self.recording_thread.isRunning():
            self.recording_thread.stop()
            self.recording_thread.wait()
            return True
        return False

    def save_recording(self, folder="Recordings"):
        """Save the captured frames as a WAV file."""
        if not self.frames:
            return None

        os.makedirs(folder, exist_ok=True)
        file_name = f"session_{len(os.listdir(folder)) + 1}.wav"
        file_path = os.path.join(folder, file_name)

        try:
            with wave.open(file_path, 'wb') as wf:
                wf.setnchannels(self.channels)
                wf.setsampwidth(pyaudio.PyAudio().get_sample_size(self.format))
                wf.setframerate(self.rate)
                wf.writeframes(b''.join(self.frames))
            return file_name
        except Exception as e:
            print(f"Error saving file: {e}")
            return None

    def terminate(self):
        """Terminate the recording thread if still running."""
        if self.recording_thread and self.recording_thread.isRunning():
            self.recording_thread.stop()
            self.recording_thread.wait()
