import os
import pandas as pd

# Path to the directory containing audio files
audio_directory = "C:\\Users\\Acer\\Downloads\\Recipes\\wav"

# Path to the directory containing transcripts
transcript_directory = "C:\\Users\\Acer\\Downloads\\Recipes\\txt"

# Output CSV file
csv_file = "C:\\Users\\Acer\\Downloads\\Recipes\\csv\\Recipes.csv"

# Initialize an empty list to store data
data = []

# Iterate over audio files
for audio_file in os.listdir(audio_directory):
    if audio_file.endswith(".wav"):
        audio_path = os.path.join(audio_directory, audio_file)
        transcript_file = os.path.join(transcript_directory, audio_file.replace(".wav", ".txt"))

        if os.path.exists(transcript_file):
            # Get WAV file size
            wav_filesize = os.path.getsize(audio_path)
            wav_filesize_kb = wav_filesize / 1024  # Convert to kilobytes

            with open(transcript_file, 'r') as file:
                transcript = file.read().strip()

            data.append([audio_path, wav_filesize_kb, transcript])
        else:
            print(f"Transcript file not found for {audio_file}")

# Create a DataFrame from the list
df = pd.DataFrame(data, columns=["wav_filename", "wav_filesize", "transcript"])

# Save DataFrame to CSV
df.to_csv(csv_file, index=False)

print(f"CSV file '{csv_file}' created successfully.")
