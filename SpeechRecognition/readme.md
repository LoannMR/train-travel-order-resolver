# SpeechRecognition

### conda

- conda env create -f venv-mac.yml -n SpeechRecognition

### models link

https://alphacephei.com/vosk/models

#### Error PyAudio

https://stackoverflow.com/questions/68251169/unable-to-install-pyaudio-on-m1-mac-portaudio-already-installed

##### Apple Silicon

brew install portaudio
pip install sounddevice
conda install -c anaconda numpy
conda install -c anaconda scipy
conda install -c conda-forge pydub
