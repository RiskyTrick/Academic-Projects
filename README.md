# CFS Session Documentor

NOTE: This keeps changing ! this is not the final version ! there are many updated to later variations

## Project Description
CFS Session Documentor is a tool designed to assist therapists in generating structured therapeutic notes (SOAP, DAP, BIRP, GIRP, etc.) based on recorded sessions. The application transcribes audio recordings using AI-based speech-to-text processing and generates structured notes, reducing the documentation workload for therapists.

This project is developed for **Child and Family Services (CFS)** and a level 1 variant is being used for the CSIS 516 Final Project.

## Features
- **Voice Recording & Management**: Record therapy sessions and save audio files.
- **Speech-to-Text Transcription**: Convert recorded audio into text using Google's SpeechRecognition API.
- **AI-Powered Note Generation**: Generate structured therapeutic notes using an AI transformer model.
- **User-Friendly Interface**: Built with PyQt5 for a seamless experience.
- **Session Management**: Store and manage recorded sessions for later review.
- **Microphone Selection**: Choose from available microphones for recording.

## Technologies Used
- **Python 3.x**
- **PyQt5** (User Interface)
- **PyAudio** (Audio Recording)
- **SpeechRecognition** (Transcription)
- **DeepSpeech** (Real-time Speech-to-Text Processing)
- **OS & Wave** (File Handling)

## Installation
1. **Clone the Repository**

   ```
2. **Create a Virtual Environment (Optional but Recommended)**
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows use `venv\Scripts\activate`
   ```
3. **Install Dependencies**
   ```bash
   pip install -r requirements.txt
   ```
4. **Run the Application**
   ```bash
   python Documentor_app.py  (or) looks_good_model1.py
   ```

## Usage
1. **Start the Application**: Launch the app using the command above.
2. **Select a Microphone**: Choose an available microphone from the settings.
3. **Record a Session**: Click "Start Recording" to begin capturing audio.
4. **Stop & Save**: Click "Stop Recording" and save the file.
5. **Transcribe Audio**: Select a saved session and generate a transcript.
6. **Generate Notes**: AI processes the transcript to generate structured therapeutic notes.

## Project Structure
```
CFS-Session-Documentor/
│-- Documentor_app.py     # Main application UI
│-- RecordingThread.py    # Handles audio recording in a separate thread
│-- Transcription.py      # Converts audio to text using SpeechRecognition
│-- tts.py                # Implements real-time speech-to-text with DeepSpeech
│-- VoiceControls.py      # Manages microphone selection and audio saving
│-- requirements.txt      # Required dependencies
│-- README.md             # Project documentation
│-- Recordings/           # Folder for saved session audio files
```


## Video Demo
//yet to be created 

## Future Enhancements
- **Support for Multiple Languages**
- **Cloud-Based Storage & Access**
- **Advanced AI Model for More Context-Aware Notes**
- **Integration with EMR Systems**
