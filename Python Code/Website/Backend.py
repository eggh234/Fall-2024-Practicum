from flask import (
    Flask,
    render_template,
    request,
    redirect,
    url_for,
)
import os
import requests
import base64
from pydub import AudioSegment
import matplotlib.pyplot as plt
import numpy as np
from scipy.io import wavfile

app = Flask(__name__)

# Set the paths to the correct directories
SPEECHES_FOLDER = "/Users/daniel_huang/Desktop/Fall-2024-Practicum/Speeches"
SPECTOGRAMS_FOLDER = "/Users/daniel_huang/Desktop/Fall-2024-Practicum/Spectograms"
TEXT_TRANSCRIPTS_FOLDER = (
    "/Users/daniel_huang/Desktop/Fall-2024-Practicum/Text_Transcripts"
)


# Function to encode image to base64 format
def encode_image(image_path):
    """Encodes the image at the given path to base64"""
    with open(image_path, "rb") as image_file:
        return base64.b64encode(image_file.read()).decode("utf-8")


# Function to analyze spectrograms and send request to the OpenAI API
def analyze_spectrogram(file_name, path):
    """
    Analyze spectrogram by sending multiple base64-encoded images and text-based content to OpenAI API.
    """
    # Paths for various spectrogram images
    image_paths = [
        os.path.join(path, "Spectograms", f"{file_name}-spectogram.png"),
        os.path.join(path, "Spectograms", "Robo-Voice.mp3-spectogram.png"),
        os.path.join(path, "Spectograms", "Trump-Fake.mp3-spectogram.png"),
        os.path.join(
            path, "Spectograms", "Dream-English-Traditional-ABC01.mp3-spectogram.png"
        ),
        os.path.join(path, "Spectograms", "trump_farewell_address.mp3-spectogram.png"),
        os.path.join(path, "Spectograms", "first-light-239806.mp3-spectogram.png"),
        os.path.join(path, "Spectograms", "Oliver-Pool-Jump.mp3-spectogram.png"),
        os.path.join(path, "Spectograms", "House_Party.mp3-spectogram.png"),
    ]

    # Encode the images to base64
    base64_images = [encode_image(image_path) for image_path in image_paths]

    # Prepare the API request payload
    api_key = os.getenv(
        "OPENAI_API_KEY"
    )  # Ensure the API key is properly set in your environment
    headers = {"Content-Type": "application/json", "Authorization": f"Bearer {api_key}"}

    # Construct the payload for the OpenAI API
    payload = {
        "model": "gpt-4o-mini",
        "messages": [
            {
                "role": "user",
                "content": [
                    {
                        "type": "text",
                        "text": "Is the first spectrogram human?"
                        "Use the 2nd and 3rd robo file and all files starting from 4th are human file to differentiate between real or fake voice give a rating of 0-10 then decide only give rating for first file. "
                        "Dont mention any other files except for the current one. be more lenient on grading currently even human files are getting 4s. When you reference it just say the provieded file not the first file: "
                        "output format: Score: /n Reason: ",
                    },
                    {
                        "type": "image_url",
                        "image_url": {
                            "url": f"data:image/jpeg;base64,{base64_images[0]}"
                        },
                    },
                    {
                        "type": "image_url",
                        "image_url": {
                            "url": f"data:image/jpeg;base64,{base64_images[1]}"
                        },
                    },
                    {
                        "type": "image_url",
                        "image_url": {
                            "url": f"data:image/jpeg;base64,{base64_images[2]}"
                        },
                    },
                    {
                        "type": "image_url",
                        "image_url": {
                            "url": f"data:image/jpeg;base64,{base64_images[3]}"
                        },
                    },
                    {
                        "type": "image_url",
                        "image_url": {
                            "url": f"data:image/jpeg;base64,{base64_images[4]}"
                        },
                    },
                    {
                        "type": "image_url",
                        "image_url": {
                            "url": f"data:image/jpeg;base64,{base64_images[5]}"
                        },
                    },
                    {
                        "type": "image_url",
                        "image_url": {
                            "url": f"data:image/jpeg;base64,{base64_images[6]}"
                        },
                    },
                    {
                        "type": "image_url",
                        "image_url": {
                            "url": f"data:image/jpeg;base64,{base64_images[7]}"
                        },
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
    try:
        # Make the API request
        response = requests.post(
            "https://api.openai.com/v1/chat/completions", headers=headers, json=payload
        )
        response.raise_for_status()  # Raise an exception for 4XX/5XX errors

        # Log the entire response for debugging
        response_dict = response.json()
        print("API Response:", response_dict)  # Print the full response

        # Extract the message content if available
        if "choices" in response_dict:
            message_content = response_dict["choices"][0]["message"]["content"]
        else:
            message_content = "No 'choices' key in API response. Check API request."

    except requests.exceptions.RequestException as e:
        # Handle any issues with the API request (e.g., connection errors, timeouts, etc.)
        print(f"API request failed: {e}")
        message_content = f"API request failed: {e}"

    return message_content  # Return the score and reason or error message


@app.route("/")
def index():
    return render_template("index.html")


@app.route("/upload", methods=["POST"])
def upload_file():
    if "file" not in request.files:
        return redirect(request.url)

    file = request.files["file"]
    if file.filename == "":
        return redirect(request.url)

    if file:
        # Save the uploaded file to the speeches folder
        file_path = os.path.join(SPEECHES_FOLDER, file.filename)
        file.save(file_path)

        # Call the spectrogram analyzer to process the file
        chatgpt_output = analyze_spectrogram(
            file.filename, "/Users/daniel_huang/Desktop/Fall-2024-Practicum"
        )

        return redirect(
            url_for("results", filename=file.filename, chatgpt_output=chatgpt_output)
        )


@app.route("/results/<filename>")
def results(filename):
    # Path for the transcription file
    transcript_file_path = os.path.join(
        TEXT_TRANSCRIPTS_FOLDER, f"{filename}-transcript.txt"
    )

    # Path for the spectrogram image
    spectrogram_image_path = os.path.join(
        SPECTOGRAMS_FOLDER, f"{filename}-spectogram.png"
    )

    # Read the transcription if it exists
    transcription = ""
    if os.path.exists(transcript_file_path):
        with open(transcript_file_path, "r") as file:
            transcription = file.read()

    # Get the chatgpt_output from the uploaded file
    chatgpt_output = request.args.get("chatgpt_output", "No response")

    # Serve the results page
    return render_template(
        "results.html",
        filename=filename,
        transcription=transcription,
        spectrogram_image_url=(
            url_for("static", filename=f"Spectograms/{filename}-spectogram.png")
            if os.path.exists(spectrogram_image_path)
            else None
        ),
        chatgpt_output=chatgpt_output,
    )


if __name__ == "__main__":
    app.run(debug=True)
