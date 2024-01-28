import os
import string
import csv
import argparse
import librosa  # pip install librosa==0.7.2
import num2words  # pip install num2words
import re


def replace_func(text):
    # remove extra charactors from the transcript
    for ch in ['\\', '`', '‘', '’', '*', '_', ',', '"', '{', '}', '[', ']', '(', ')', '>', '#', '+', '-', '.', '!', '$',
               ':', ';', '|', '~', '@', '*', '<', '?', '/']:
        if ch in text:
            text = text.replace(ch, "")
        elif ch == '&':
            text = text.replace(ch, "and")

    return text


def get_audio_info(file_name):
    return librosa.get_duration(filename=file_name), librosa.get_samplerate(file_name)


def main():
    parser = argparse.ArgumentParser(description="Pre Process File")
    parser.add_argument('--wav', required=True,
                        help='WAV Folder')
    parser.add_argument('--meta', required=True,
                        help='Path to file with metadata')
    args = parser.parse_args()

    # File containing audio file name and transcript
    in_file = open(os.path.join(args.meta, 'txt.done.data'), 'r')

    # Create target CSV file to write metadata info as per DeepSpeech requirements
    # Define a writer object to write rows to file
    out_file = open(os.path.join(os.getcwd(), 'output.csv'), 'a', newline='')
    csv_writer = csv.writer(out_file)

    # All CSV files must contain the following as the first line. Only run once
    csv_writer.writerow(['wav_filename', 'wav_filesize', 'transcript'])

    # Keep track of total audio files and files not added to CSV due to them being too long or invalid sample rate
    total_count = 0
    row_count = 0

    try:
        for line in in_file:
            total_count += 1
            try:
                fname, ftext, _ = line.split("\"")

                # Separate file name and transcript from metadata file. Preprocess transcript and get audio info too
                # convert all numbers to text using num2words
                fname = fname.strip()[1:].strip() + '.wav'
                ftext = ftext.strip().lower()
                ftext = replace_func(ftext).replace("  ", " ").strip()
                ftext = re.sub(r"(\d+)", lambda x: num2words.num2words(int(x.group(0))), ftext)
                fsr = get_audio_info(str(os.path.join(args.wav, fname)))
                # fdur, fsr = get_audio_info(str(os.path.join(args.wav, fname)))

                # Don't add files which don't fit into model specifications
                # Either not 48kHz or longer than 10 secs
                # if fsr == 48000:
                #     print("Different SR:", fname)
                #     continue
                # if fdur > 10:
                #     print("Too Long:", fname)
                #     continue
                if ftext == '':
                    print("No Transcript found")
                    continue

                # Write each row to CSV with size info
                fsize = os.path.getsize(os.path.join(args.wav, fname))
                print(fname, fsize, ftext)
                csv_writer.writerow([os.path.join(args.wav, fname), fsize, ftext])
                row_count += 1
            except Exception as e:
                print(str(e))
    except Exception as e:
        print(str(e))

    print("Added Rows:", row_count)
    print("Total Rows:", total_count, "\n")

    in_file.close()
    out_file.close()


if __name__ == "__main__":
    main()