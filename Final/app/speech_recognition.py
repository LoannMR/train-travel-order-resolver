from vosk import Model, KaldiRecognizer
import pyaudio

# load model
model = Model("./models/vosk-model-fr-0.22")
recognizer = KaldiRecognizer(model, 16000)

def start_voice_recognition():
    """
    Speach to text.
    Stop the voice recognition by saying "stop" or until a specific time
    """
    mic = pyaudio.PyAudio()
    stream = mic.open(format=pyaudio.paInt16, channels=1, rate=16000, input=True, frames_per_buffer=8192)
    stream.start_stream()

    print("Listening...")
    while True:
        data = stream.read(4096)
        if recognizer.AcceptWaveform(data):
            text = recognizer.Result()
            text = text[14:-3]  # Get the sentence
            print(text)
            break  # Stop after the first sentence is recognized

    # Close the stream and PyAudio instance
    stream.stop_stream()
    stream.close()
    mic.terminate()

    return text