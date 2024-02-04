import os
import string
import csv
import librosa
import num2words
import re

def replace_func(text):
    # remove extra characters from the transcript
    for ch in ['\\', '`', '‘', '’', '*', '_', ',', '"', '{', '}', '[', ']', '(', ')', '>', '#', '+', '-', '.', '!', '$',
               ':', ';', '|', '~', '@', '*', '<', '?', '/']:
        if ch in text:
            text = text.replace(ch, "")
        elif ch == '&':
            text = text.replace(ch, "and")

    return text

def get_audio_info(file_name):
    return librosa.get_duration(path=file_name), librosa.get_samplerate(path=file_name)

def main():
    # Modify the following paths as needed
    transcripts_folder = r'C:\Users\Acer\Downloads\Recipes\txt'
    audio_folder = r'C:\Users\Acer\Downloads\Recipes\wav'
    csv_output_folder = r'C:\Users\Acer\Downloads\Recipes\csv'

    # Create target CSV file to write metadata info as per DeepSpeech requirements
    # Define a writer object to write rows to file
    out_file_path = os.path.join(csv_output_folder, 'output.csv')
    out_file = open(out_file_path, 'a', newline='')
    csv_writer = csv.writer(out_file)

    # All CSV files must contain the following as the first line. Only run once
    csv_writer.writerow(['wav_filename', 'wav_filesize', 'transcript'])

    # Keep track of total audio files and files not added to CSV due to them being too long or invalid sample rate
    total_count = 0
    row_count = 0

    try:
        # Iterate through each audio file in the specified folder
        for fname in os.listdir(audio_folder):
            if fname.endswith(".wav"):
                total_count += 1
                try:
                    # Construct full path to audio file and transcript file
                    audio_path = os.path.join(audio_folder, fname)
                    transcript_path = os.path.join(transcripts_folder, fname.replace(".wav", ".txt"))

                    # Read transcript file
                    with open(transcript_path, 'r') as transcript_file:
                        ftext = transcript_file.read().strip().lower()

                    # Preprocess transcript and get audio info
                    ftext = replace_func(ftext).replace("  ", " ").strip()
                    ftext = re.sub(r"(\d+)", lambda x: num2words.num2words(int(x.group(0))), ftext)
                    fdur, fsr = get_audio_info(audio_path)

                    # Don't add files which don't fit into model specifications
                    # Either not 16kHz
                    if fsr != 16000:
                        print("Invalid sample rate:", fname)
                        continue
                    if ftext == '':
                        print("No Transcript found")
                        continue

                    # Write each row to CSV with size info
                    fsize = os.path.getsize(audio_path)
                    print(fname, fsize, ftext)
                    csv_writer.writerow([audio_path, fsize, ftext])
                    row_count += 1
                except Exception as e:
                    print(str(e))
    except Exception as e:
        print(str(e))

    print("Added Rows:", row_count)
    print("Total Rows:", total_count, "\n")

    out_file.close()

if __name__ == "__main__":
    main()
