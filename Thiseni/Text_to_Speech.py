import pyttsx3

def text_to_speech(file_path):
    # Initialize the text-to-speech engine
    engine = pyttsx3.init()

    # Set properties (optional)
    engine.setProperty('rate', 150)  # Speed of speech
    engine.setProperty('volume', 1)  # Volume level (0.0 to 1.0)

    # Read the content of the text file
    try:
        with open(file_path, 'r') as file:
            text_content = file.read()
    except FileNotFoundError:
        print(f"File not found: {file_path}")
        return

    # Convert text to speech
    engine.say(text_content)
    engine.runAndWait()

if __name__ == "__main__":
    file_path = "C:/Users/Acer/Desktop/New folder/nlu.txt"
    text_to_speech(file_path)
