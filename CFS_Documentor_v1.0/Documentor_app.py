import os
import sys
from PyQt5.QtWidgets import (
    QApplication, QMainWindow, QVBoxLayout, QHBoxLayout, QWidget,
    QPushButton, QLabel, QListWidget, QComboBox, QTextEdit
)
from PyQt5.QtGui import QIcon, QFont
from PyQt5.QtCore import Qt
from VoiceControls import VoiceControls
from Transcription import transcribe_audio  # Import the generate_transcript function

class TherapyApp(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("CFS Session Documentor")
        self.setGeometry(100, 100, 800, 600)

        # VoiceControls instance
        self.voice_control = VoiceControls()

        # UI Setup
        self.init_ui()

    def init_ui(self):
        # Central widget
        central_widget = QWidget()
        self.setCentralWidget(central_widget)

        # Main layout
        main_layout = QVBoxLayout()
        central_widget.setLayout(main_layout)

        # Title Label
        title = QLabel("Child & Family Services of Saginaw Documentor")
        title.setFont(QFont("Arial", 20, QFont.Bold))
        title.setAlignment(Qt.AlignCenter)
        title.setStyleSheet("color: #0078d7;")
        main_layout.addWidget(title)

        # Microphone Selector
        mic_layout = QHBoxLayout()
        mic_label = QLabel("Select Microphone:")
        mic_label.setFont(QFont("Arial", 12))
        mic_label.setStyleSheet("color: #333;")
        self.mic_selector = QComboBox()
        self.populate_mic_list()
        self.mic_selector.setStyleSheet(""" QComboBox { padding: 5px; border: 1px solid #0078d7; border-radius: 5px; background: #f0f0f0;} QComboBox:hover { border: 1px solid #005bb5;} """)
        mic_layout.addWidget(mic_label)
        mic_layout.addWidget(self.mic_selector)
        main_layout.addLayout(mic_layout)

        # Buttons Layout
        button_layout = QHBoxLayout()

        self.start_button = QPushButton("Start Recording")
        self.start_button.setIcon(QIcon("start_icon.png"))
        self.start_button.setStyleSheet(self.button_style("#0078d7", "#005bb5"))
        self.start_button.clicked.connect(self.start_recording)
        button_layout.addWidget(self.start_button)

        self.stop_button = QPushButton("Stop Recording")
        self.stop_button.setIcon(QIcon("stop_icon.png"))
        self.stop_button.setStyleSheet(self.button_style("#d9534f", "#c9302c"))
        self.stop_button.clicked.connect(self.stop_recording)
        button_layout.addWidget(self.stop_button)

        self.save_button = QPushButton("Save Recording")
        self.save_button.setIcon(QIcon("save_icon.png"))
        self.save_button.setStyleSheet(self.button_style("#5cb85c", "#4cae4c"))
        self.save_button.clicked.connect(self.save_recording)
        button_layout.addWidget(self.save_button)

        # Add Button for Generate Transcript
        self.transcript_button = QPushButton("Generate Transcript")
        self.transcript_button.setIcon(QIcon("transcript_icon.png"))
        self.transcript_button.setStyleSheet(self.button_style("#f0ad4e", "#ec971f"))
        self.transcript_button.clicked.connect(self.generate_transcript)
        button_layout.addWidget(self.transcript_button)

        main_layout.addLayout(button_layout)

        # Status label
        self.status_label = QLabel("Status: Idle")
        self.status_label.setFont(QFont("Arial", 12, QFont.Bold))
        self.status_label.setStyleSheet("color: #555; margin-top: 10px;")
        self.status_label.setAlignment(Qt.AlignCenter)
        main_layout.addWidget(self.status_label)

        # Saved sessions list
        self.sessions_list = QListWidget()
        self.sessions_list.setStyleSheet(""" QListWidget { border: 1px solid #ccc; border-radius: 5px; background: #fafafa; padding: 5px; } """)
        main_layout.addWidget(QLabel("Saved Sessions:"))
        main_layout.addWidget(self.sessions_list)

        # Text area to display transcript
        self.transcript_text = QTextEdit()
        self.transcript_text.setPlaceholderText("Transcript will appear here...")
        self.transcript_text.setReadOnly(True)
        self.transcript_text.setStyleSheet("background-color: #f9f9f9; border: 1px solid #ddd;")
        main_layout.addWidget(self.transcript_text)

    def button_style(self, color, hover_color):
        """Generate stylesheet for buttons."""
        return f""" QPushButton {{ background-color: {color}; color: white; border: none; border-radius: 10px; padding: 10px 20px; font-size: 14px; }} QPushButton:hover {{ background-color: {hover_color}; }} """

    def populate_mic_list(self):
        """Populate the microphone selection dropdown."""
        mics = self.voice_control.get_available_microphones()
        for index, name in mics:
            self.mic_selector.addItem(name, index)

    def start_recording(self):
        """Start audio recording."""
        mic_index = self.mic_selector.currentData()
        if mic_index is None:
            self.status_label.setText("Status: Please select a microphone.")
            return

        if self.voice_control.start_recording(mic_index):
            self.status_label.setText("Status: Recording...")
        else:
            self.status_label.setText("Status: Failed to start recording.")

    def stop_recording(self):
        """Stop audio recording."""
        if self.voice_control.stop_recording():
            self.status_label.setText("Status: Recording stopped.")
        else:
            self.status_label.setText("Status: Failed to stop recording.")

    def save_recording(self):
        """Save the recording."""
        file_name = self.voice_control.save_recording()
        if file_name:
            self.sessions_list.addItem(file_name)
            self.status_label.setText(f"Status: Recording saved as {file_name}.")
        else:
            self.status_label.setText("Status: No recording to save.")
    def generate_transcript(self):
        """Generate a transcript using Google Speech-to-Text."""
        # Check if an audio session is selected
        if not self.sessions_list.selectedItems():
            self.status_label.setText("Status: Please select a session.")
            return

        # Get the selected session file
        selected_file = self.sessions_list.selectedItems()[0].text()
        file_path = os.path.join("Recordings", selected_file)

        # Call the transcription function from Transcription.py
        try:
            transcript = transcribe_audio(file_path)
            if transcript:
                self.transcript_text.setText(transcript)
                self.status_label.setText(f"Status: Transcript generated for {selected_file}.")
            else:
                self.status_label.setText("Status: Failed to generate transcript.")
        except Exception as e:
            self.status_label.setText("Status: Error generating transcript.")
            print(f"Error: {e}")

    def closeEvent(self, event):
        """Clean up resources on exit."""
        self.voice_control.terminate()
        event.accept()


# Run the application
if __name__ == "__main__":
    app = QApplication(sys.argv)
    app.setStyleSheet("QMainWindow { background-color: #f0f0f0; }")  # Set app-wide background color
    window = TherapyApp()
    window.show()
    sys.exit(app.exec_())
