from openai import OpenAI
import re
import os

# import librosa
# import librosa.display
# import matplotlib.pyplot as plt
# import numpy as np

client = OpenAI()
base_file_path = "/Users/daniel_huang/Desktop/Fall-2024-Practicum"


def speech_to_text(file_name):
    file_path = os.path.join(base_file_path, "Speeches", f"{file_name}.mp3")
    output_dir = os.path.join(base_file_path, "Text_Transcripts")
    output_file_path = os.path.join(output_dir, f"{file_name}-transcript.txt")

    audio_file = open(file_path, "rb")
    transcription = client.audio.transcriptions.create(
        model="whisper-1", file=audio_file
    )

    # Write the formatted transcription text to the file
    with open(output_file_path, "w") as file:
        file.write(transcription.text)

    print("Formatted transcription saved to", output_file_path)


def Transcript_Counter(file_name):
    transcript_file_path = os.path.join(
        base_file_path, "Text_Transcripts", f"{file_name}-transcript.txt"
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

    output_file_name = os.path.join(
        base_file_path, "Text_Counter", f"{file_name}-count.txt"
    )
    with open(output_file_name, "w") as output_file:
        for word, count in word_counts.items():
            output_file.write(f"{word}: {count}\n")


def main():
    file_name = input("Input speech file name to check: ")
    # Ensure speech_to_text function is defined
    speech_to_text(file_name)
    Transcript_Counter(file_name)


if __name__ == "__main__":
    main()

# # Load the MP3 file
# audio_path = "/Users/daniel_huang/Desktop/Practicum/Speeches/trump_farewell_address.mp3"
# y, sr = librosa.load(audio_path)

# # Generate the spectrogram
# S = librosa.feature.melspectrogram(y=y, sr=sr, n_mels=128)
# S_dB = librosa.power_to_db(S, ref=np.max)

# # Plot the spectrogram
# plt.figure(figsize=(10, 4))
# librosa.display.specshow(S_dB, sr=sr, x_axis="time", y_axis="mel")
# plt.colorbar(format="%+2.0f dB")
# plt.title("Mel-frequency spectrogram")
# plt.tight_layout()
# plt.show()
