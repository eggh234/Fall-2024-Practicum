from openai import OpenAI

client = OpenAI()

audio_file = open(
    "/Users/daniel_huang/Desktop/Practicum/Speeches/Dream English Traditional ABC01.mp3",
    "rb",
)
transcription = client.audio.transcriptions.create(model="whisper-1", file=audio_file)

print(transcription.text)

# Define the file path for the output text file
output_file_path = (
    "/Users/daniel_huang/Desktop/Practicum/Text_Transcripts/Transcript.txt"
)

# Write the formatted transcription text to the file
with open(output_file_path, "w") as file:
    file.write(transcription.text)

print("Formatted transcription saved to", output_file_path)
