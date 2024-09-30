from openai import OpenAI
import re
import os

# import librosa
# import librosa.display
# import matplotlib.pyplot as plt
# import numpy as np

client = OpenAI()


def speech_to_text(file_path):
    file_name = os.path.basename(file_path)

    # Define the directory for the output file
    output_dir = "/Users/daniel_huang/Desktop/Practicum/Text_Transcripts"

    # Create the output file path
    output_file_path = os.path.join(output_dir, f"{file_name}-transcript.txt")

    audio_file = open(
        file_path,
        "rb",
    )
    transcription = client.audio.transcriptions.create(
        model="whisper-1", file=audio_file
    )

    # Write the formatted transcription text to the file
    with open(output_file_path, "w") as file:
        file.write(transcription.text)

    print("Formatted transcription saved to", output_file_path)


def main():
    speech_to_text(
        "/Users/daniel_huang/Desktop/Practicum/Speeches/Dream-English-Traditional-ABC01.mp3"
    )


if __name__ == "__main__":
    main()


def count_words_in_text_file(file_path):
    word_counts = {}
    timestamp_pattern = re.compile(r"\(.*?\)")

    with open(file_path, "r") as file:
        text = file.read()
        text = timestamp_pattern.sub("", text)  # Remove timestamps
        words = text.split()

        for word in words:
            word = word.lower().strip('.,!?;:"()[]{}')  # Normalize the word
            if word in word_counts:
                word_counts[word] += 1
            else:
                word_counts[word] = 1

    return word_counts


def write_word_counts_to_file(word_counts, output_file_path):
    with open(output_file_path, "w") as file:
        for word, count in word_counts.items():
            file.write(f"{word}: {count}\n")


file_path = "/Users/daniel_huang/Desktop/Practicum/Text_Transcripts/Speech1.txt"
output_file_path = (
    "/Users/daniel_huang/Desktop/Practicum/Text_Transcripts/Speech1_count.txt"
)
word_counts = count_words_in_text_file(file_path)
write_word_counts_to_file(word_counts, output_file_path)

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
