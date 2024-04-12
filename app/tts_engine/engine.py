import os
import numpy as np
import soundfile as sf
from transformers import AutoProcessor, BarkModel

class TTSEngine:
    def __init__(self, transcript, model_name="suno/bark", voice_preset="v2/en_speaker_6", output_dir="data/audio_files"):
        self.transcript = transcript
        self.model_name = model_name
        self.voice_preset = voice_preset
        self.output_dir = output_dir

        # Initialize the processor and model
        self.processor = AutoProcessor.from_pretrained(self.model_name)
        self.model = BarkModel.from_pretrained(self.model_name)

        # Ensure the output directory exists
        os.makedirs(self.output_dir, exist_ok=True)

    def convert_to_speech(self):
        # Process the input
        inputs = self.processor(self.transcript, voice_preset=self.voice_preset, return_tensors="pt")

        # Generate the audio array
        audio_array = self.model.generate(**inputs).cpu().numpy().squeeze()

        # Define the output audio file path
        audio_path = os.path.join(self.output_dir, f"{hash(self.transcript)}.wav")

        # Save the audio file
        sf.write(audio_path, audio_array, samplerate=16000)  # Assuming a sample rate of 16000 Hz

        return audio_path

# Example usage
if __name__ == "__main__":
    transcript = "Hello, my dog is cute"
    tts_engine = TTSEngine(transcript)
    audio_path = tts_engine.convert_to_speech()
    print(f"Generated audio file at: {audio_path}")