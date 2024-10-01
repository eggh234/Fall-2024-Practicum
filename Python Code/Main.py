from openai import OpenAI
import matplotlib.pyplot as plt
import numpy as np
from pydub import AudioSegment
import matplotlib.pyplot as plt
from scipy.io import wavfile
import re
import os
import base64
import requests

client = OpenAI()


def encode_image(image_path):
    with open(image_path, "rb") as image_file:
        return base64.b64encode(image_file.read()).decode("utf-8")


def analyze_spectrogram(file_name, path):
    image_path = os.path.join(path, "Spectograms", file_name + "-spectogram.png")
    base64_image = encode_image(image_path)

    api_key = os.getenv("OPENAI_API_KEY")
    headers = {"Content-Type": "application/json", "Authorization": f"Bearer {api_key}"}

    payload = {
        "model": "gpt-4o",
        "messages": [
            {
                "role": "user",
                "content": [
                    {
                        "type": "text",
                        "text": "Give this spectogram a rating of 0 - 10 on humaness, return it in this format: score: rating amount",
                    },
                    {
                        "type": "image_url",
                        "image_url": {"url": f"data:image/jpeg;base64,{base64_image}"},
                    },
                ],
            }
        ],
        "max_tokens": 300,
    }

    response = requests.post(
        "https://api.openai.com/v1/chat/completions", headers=headers, json=payload
    )
    response_dict = response.json()
    message_content = response_dict["choices"][0]["message"]["content"]
    print(message_content)


def get_directory_path():
    # Get the current working directory
    current_dir = os.getcwd()
    parent_dir = os.path.dirname(current_dir)

    return parent_dir


def MP3_to_Chart(file_name, path):
    try:
        # Construct the file paths
        file_path = os.path.join(path, "Speeches", file_name)
        output_file_path = os.path.join(
            path,
            "Spectograms",
            f"{os.path.splitext(file_name)[0]}" + ".mp3-spectogram.png",
        )
        temp_file_path = os.path.join(path, "Spectograms", "temp.wav")

        print("Creating Spectrogram")

        # Read mp3 and convert to wav
        mp3_audio = AudioSegment.from_file(file_path, format="mp3")
        mp3_audio.export(temp_file_path, format="wav")

        # Read wav file
        FS, data = wavfile.read(temp_file_path)

        # Convert to mono if stereo
        if len(data.shape) == 2:
            data = np.mean(data, axis=1)

        # Plot spectrogram with custom colormap
        plt.figure(figsize=(10, 4))
        plt.specgram(data, Fs=FS, NFFT=128, noverlap=0, cmap="inferno")
        plt.gca().set_facecolor("purple")  # Set background color to purple
        plt.colorbar(format="%+2.0f dB")
        plt.title("Spectrogram of" + file_name)
        plt.xlabel("Time")
        plt.ylabel("Frequency")

        # Save and show the plot
        plt.savefig(output_file_path)
        plt.show()

        # Clean up temporary file
        os.remove(temp_file_path)
    except Exception as e:
        print(f"An error occurred: {e}")


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
    analyze_spectrogram(file_name, path)


if __name__ == "__main__":
    main()
