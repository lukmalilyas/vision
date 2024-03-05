import os  # read files and directories
import deepspeech #transcript using asr
import numpy as np #convert audio data to a NumPy array
import jiwer #ji Speech Error Rate - calc wer
import wave #write wav files

#DeepSpeech model and scorer files
model_path = "C:/Users/Acer/Desktop/recipe_audio/deepspeech/deepspeech-0.9.3-models.pbmm" #trained model
scorer_path = "C:/Users/Acer/Desktop/recipe_audio/deepspeech/deepspeech-0.9.3-models.scorer" #to improve accuracy

#.wav files and corresponding .txt files
data_directory = "C:/Users/Acer/Desktop/recipe_audio/wav/"

def read_text_file(text_file_path): #read reference text
    with open(text_file_path, 'r') as file:
        return file.read().strip()

def transcribe_deepspeech(wav_path, model, scorer):
    # Initialize DeepSpeech model
    ds_model = deepspeech.Model(model)
    ds_model.enableExternalScorer(scorer)

    # Read the WAV file using wave module
    with wave.open(wav_path, 'rb') as wave_file:
        # Get the audio data
        audio_data = wave_file.readframes(wave_file.getnframes())
        audio_data = np.frombuffer(audio_data, dtype=np.int16)

    # Transcribe audio
    text = ds_model.stt(audio_data)
    return text

total_wer = 0
num_files = 0


for filename in os.listdir(data_directory): #loop through all .wav files and get respective text file
    if filename.endswith(".wav"):
        wav_path = os.path.join(data_directory, filename)

        text_file_path = os.path.join(data_directory, os.path.splitext(filename)[0] + ".txt")
        reference_transcription = read_text_file(text_file_path)

        # Transcribe audio
        hypothesis_transcription = transcribe_deepspeech(wav_path, model_path, scorer_path)
        print(f"Reference: {reference_transcription}")
        print(f"Hypothesis: {hypothesis_transcription}")

        # Calculate WER
        wer_rate = jiwer.wer(reference_transcription, hypothesis_transcription)
        total_wer += wer_rate
        num_files += 1

        print(f"Word Error Rate (WER) for {filename}: {wer_rate:.4f}")

if num_files > 0:
    overall_wer = total_wer / num_files
    print(f"\nOverall Word Error Rate for {num_files} files: {overall_wer:.4f}")
else:
    print("No valid files found for evaluation.")
