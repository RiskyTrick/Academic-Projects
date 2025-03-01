import os
from datetime import datetime
from pydub import AudioSegment

class SessionManager:
    def __init__(self, base_folder="Recordings"):
        """Initialize session manager with a base folder."""
        self.base_folder = base_folder
        os.makedirs(self.base_folder, exist_ok=True)

    def save_session(self, client_name, session_topic, audio_data, audio_format="mp3"):
        """Save a session with metadata and audio as MP3."""
        client_folder = os.path.join(self.base_folder, client_name)
        os.makedirs(client_folder, exist_ok=True)

        timestamp = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
        session_folder = os.path.join(client_folder, f"{session_topic}_{timestamp}")
        os.makedirs(session_folder, exist_ok=True)

        audio_file_path = os.path.join(session_folder, f"session_audio.{audio_format}")
        metadata_file_path = os.path.join(session_folder, "metadata.txt")

        try:
            # Save MP3 audio data
            audio = AudioSegment(data=audio_data, sample_width=2, frame_rate=44100, channels=1)
            audio.export(audio_file_path, format=audio_format)

            # Save metadata
            with open(metadata_file_path, "w") as f:
                f.write(f"Client: {client_name}\nTopic: {session_topic}\nTimestamp: {timestamp}\n")

            return session_folder
        except Exception as e:
            print(f"Error saving session: {e}")
            return None

    def get_all_sessions(self):
        """Retrieve all saved sessions with clean names."""
        sessions = []
        for root, dirs, _ in os.walk(self.base_folder):
            for dir_name in dirs:
                sessions.append(dir_name)  # Add only folder names
        return sessions

    def get_session_audio_path(self, session_folder):
        """Get the path to the MP3 audio file in a session folder."""
        audio_path = os.path.join(self.base_folder, session_folder, "session_audio.mp3")
        return audio_path if os.path.exists(audio_path) else None

    def delete_session(self, session_folder):
        """Delete a session folder and its contents."""
        full_path = os.path.join(self.base_folder, session_folder)
        if os.path.exists(full_path):
            for root, dirs, files in os.walk(full_path, topdown=False):
                for name in files:
                    os.remove(os.path.join(root, name))
                for name in dirs:
                    os.rmdir(os.path.join(root, name))
            os.rmdir(full_path)
            return True
        return False
