import tkinter as tk
from tkinter import messagebox, filedialog
import pyaudio
import wave
import threading
import os

class VoiceRecorderApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Advanced Voice Recorder")
        self.root.geometry("400x300")

        # Audio recording parameters
        self.chunk = 1024
        self.sample_format = pyaudio.paInt16  # 16 bits per sample
        self.channels = 2
        self.fs = 44100  # Record at 44100 samples per second
        self.frames = []  # List to store frames
        self.stream = None
        self.is_recording = False
        self.is_paused = False

        self.filepath = None  # Filepath for saving audio

        # Create GUI elements
        self.create_widgets()

    def create_widgets(self):
        self.record_button = tk.Button(self.root, text="Record", command=self.start_recording, width=10, font=("Arial", 14), bg="green", fg="white")
        self.record_button.pack(pady=10)

        self.pause_button = tk.Button(self.root, text="Pause", command=self.pause_recording, width=10, font=("Arial", 14), state=tk.DISABLED)
        self.pause_button.pack(pady=10)

        self.stop_button = tk.Button(self.root, text="Stop", command=self.stop_recording, width=10, font=("Arial", 14), state=tk.DISABLED, bg="red", fg="white")
        self.stop_button.pack(pady=10)

        self.play_button = tk.Button(self.root, text="Play", command=self.play_audio, width=10, font=("Arial", 14), state=tk.DISABLED, bg="blue", fg="white")
        self.play_button.pack(pady=10)

        self.status_label = tk.Label(self.root, text="Status: Idle", font=("Arial", 12))
        self.status_label.pack(pady=10)

    def start_recording(self):
        self.is_recording = True
        self.is_paused = False
        self.frames = []
        self.status_label.config(text="Status: Recording...")
        self.record_button.config(state=tk.DISABLED)
        self.pause_button.config(state=tk.NORMAL)
        self.stop_button.config(state=tk.NORMAL)

        # Start recording in a separate thread to avoid freezing the GUI
        threading.Thread(target=self.record).start()

    def record(self):
        audio = pyaudio.PyAudio()

        # Start audio stream
        self.stream = audio.open(format=self.sample_format,
                                 channels=self.channels,
                                 rate=self.fs,
                                 frames_per_buffer=self.chunk,
                                 input=True)

        while self.is_recording:
            if not self.is_paused:
                data = self.stream.read(self.chunk)
                self.frames.append(data)

        # Stop and close stream
        self.stream.stop_stream()
        self.stream.close()
        audio.terminate()

        # Ask the user to save the recorded file
        if len(self.frames) > 0:
            self.save_audio()

    def pause_recording(self):
        if self.is_paused:
            self.is_paused = False
            self.pause_button.config(text="Pause")
            self.status_label.config(text="Status: Recording...")
        else:
            self.is_paused = True
            self.pause_button.config(text="Resume")
            self.status_label.config(text="Status: Paused")

    def stop_recording(self):
        self.is_recording = False
        self.status_label.config(text="Status: Stopped")
        self.record_button.config(state=tk.NORMAL)
        self.pause_button.config(state=tk.DISABLED)
        self.stop_button.config(state=tk.DISABLED)

    def save_audio(self):
        # Ask the user where to save the file
        file = filedialog.asksaveasfilename(defaultextension=".wav", filetypes=[("WAV files", "*.wav")])
        if file:
            self.filepath = file
            with wave.open(file, 'wb') as wf:
                wf.setnchannels(self.channels)
                wf.setsampwidth(pyaudio.PyAudio().get_sample_size(self.sample_format))
                wf.setframerate(self.fs)
                wf.writeframes(b''.join(self.frames))

            self.play_button.config(state=tk.NORMAL)
            messagebox.showinfo("Audio Saved", f"Audio file saved at {file}")

    def play_audio(self):
        if self.filepath:
            os.system(f"start {self.filepath}")

if __name__ == "__main__":
    root = tk.Tk()
    app = VoiceRecorderApp(root)
    root.mainloop()
