import os
import speech_recognition as sr
from pydub import AudioSegment
from jiwer import wer

def convert_m4a_to_wav(m4a_path, wav_path):
    audio = AudioSegment.from_file(m4a_path, format="m4a")
    audio.export(wav_path, format="wav")

def transcribe_audio(audio_path, recognizer):
    with sr.AudioFile(audio_path) as source:
        audio = recognizer.record(source)

    try:
        transcription = recognizer.recognize_google(audio)
        return transcription.lower()  # Convert to lowercase for consistency
    except sr.UnknownValueError:
        print(f"Sorry, could not understand audio in {audio_path}")
        return ""
    except sr.RequestError as e:
        print(f"Error fetching results for {audio_path}: {e}")
        return ""

if __name__ == "__main__":
    recognizer = sr.Recognizer()

    audio_folder = "C:/Users/Acer/Desktop/recipe_audio/"

    total_wer = 0
    num_files = 0

    for audio_file in os.listdir(audio_folder):
        if audio_file.endswith(".m4a"):
            m4a_path = os.path.join(audio_folder, audio_file)
            wav_path = os.path.splitext(m4a_path)[0] + ".wav"
            convert_m4a_to_wav(m4a_path, wav_path)

            reference_transcription_file = os.path.splitext(m4a_path)[0] + ".txt"

            # Check if a corresponding reference transcription file exists
            if os.path.exists(reference_transcription_file):
                with open(reference_transcription_file, "r") as file:
                    reference_transcription = file.read().strip()
            else:
                reference_transcription = ""

            hypothesis_transcription = transcribe_audio(wav_path, recognizer)

            if hypothesis_transcription:
                wer_rate = wer(reference_transcription, hypothesis_transcription)
                total_wer += wer_rate
                num_files += 1

                # Print the reference and hypothesis transcriptions to the console
                print(f"File: {audio_file}, Word Error Rate: {wer_rate}")
                print(f"Reference Transcription: {reference_transcription}")
                print(f"Hypothesis Transcription: {hypothesis_transcription}")

            else:
                print(f"Error in transcription for {audio_file}")

    if num_files > 0:
        overall_wer = total_wer / num_files
        print(f"\nOverall Word Error Rate for {num_files} files: {overall_wer}")
    else:
        print("No valid files found for evaluation.")
