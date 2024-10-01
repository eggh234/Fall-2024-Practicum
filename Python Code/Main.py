from openai import OpenAI
import matplotlib.pyplot as plt
import numpy as np
from pydub import AudioSegment
import matplotlib.pyplot as plt
from scipy.io import wavfile
import re
import os

client = OpenAI()


def get_directory_path():
    # Get the current working directory
    current_dir = os.getcwd()
    parent_dir = os.path.dirname(current_dir)

    return parent_dir


def MP3_to_Chart(file_name, path):
    # Construct the file path
    file_path = os.path.join(path, "Speeches", file_name)
    output_file_path = os.path.join(
        path,
        "Spectograms",
        f"{os.path.splitext(file_name)[0]}-spectrogram.png",
    )
    temp_file_path = os.path.join(path, "Spectograms")
    print("Creating Spectogram")
    mp3_audio = AudioSegment.from_file(file_path, format="mp3")  # read mp3
    wname = os.path.join(temp_file_path, "temp.wav")  # use temporary file
    mp3_audio.export(wname, format="wav")  # convert to wav
    FS, data = wavfile.read(wname)  # read wav file

    # Convert to mono if stereo
    if len(data.shape) == 2:
        data = np.mean(data, axis=1)

    plt.specgram(data, Fs=FS, NFFT=128, noverlap=0)  # plot
    plt.savefig(output_file_path)
    plt.show()


def Speech_to_text(file_name, path):
    file_path = os.path.join(path, "Speeches", f"{file_name}")
    output_dir = os.path.join(path, "Text_Transcripts")
    output_file_path = os.path.join(output_dir, f"{file_name}-transcript.txt")

    audio_file = open(file_path, "rb")
    transcription = client.audio.transcriptions.create(
        model="whisper-1", file=audio_file
    )

    # Write the formatted transcription text to the file
    with open(output_file_path, "w") as file:
        file.write(transcription.text)

    print("Formatted transcription saved to", output_file_path)


def Transcript_Counter(file_name, path):
    transcript_file_path = os.path.join(
        path, "Text_Transcripts", f"{file_name}-transcript.txt"
    )

    word_counts = {}
    timestamp_pattern = re.compile(r"\(.*?\)")

    with open(transcript_file_path, "r") as file:
        text = file.read()
        text = timestamp_pattern.sub("", text)  # Remove timestamps
        words = text.split()

        for word in words:
            word = word.lower().strip('.,!?;:"()[]{}')  # Normalize the word
            if word in word_counts:
                word_counts[word] += 1
            else:
                word_counts[word] = 1

    output_file_name = os.path.join(path, "Text_Counter", f"{file_name}-count.txt")
    with open(output_file_name, "w") as output_file:
        for word, count in word_counts.items():
            output_file.write(f"{word}: {count}\n")


def main():
    path = get_directory_path()
    speeches_path = os.path.join(path, "Speeches")
    try:
        # List all files in the directory
        files = os.listdir(speeches_path)
        print("Speech files in the directory:")
        for file in files:
            print(file)
    except FileNotFoundError:
        print(f"The directory {speeches_path} does not exist.")
    except Exception as e:
        print(f"An error occurred: {e}")

    # Prompt the user to input a speech file name and check for validity
    while True:
        file_name = input("Input speech file name to check: ")
        if file_name in files:
            print("Transcribing MP3 File to Text")
            break
        else:
            print(
                f"File '{file_name}' does not exist in the directory. Please try again."
            )

    Speech_to_text(file_name, path)
    Transcript_Counter(file_name, path)
    MP3_to_Chart(file_name, path)
    # Give_Rating(file_name)


if __name__ == "__main__":
    main()
