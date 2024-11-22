import os
import pickle
import wave
import time

import numpy as np
import pyaudio
from pydub import AudioSegment
import preprocessing
from utils import get_all_words


class HMMRecognition:
    def __init__(self):
        self.model = {}

        self.class_names = get_all_words()
        self.audio_format = 'wav'

        self.record_folder = 'datasets_test'
        self.trimmed_folder = 'datasets_test'

        self.record_path = f'datasets_test'
        self.trimmed_path = f'datasets_test'

        self.model_path = 'models_train'

        self.load_model()

    @staticmethod
    def detect_leading_silence(sound, silence_threshold=-42.0, chunk_size=10):
        trim_ms = 0  # ms

        assert chunk_size > 0  # to avoid infinite loop
        while sound[trim_ms:trim_ms + chunk_size].dBFS < silence_threshold and trim_ms < len(sound):
            trim_ms += chunk_size

        return trim_ms

    def load_model(self):
        for key in self.class_names:
            name = f"{self.model_path}/full/model_{key}.pkl"
            with open(name, 'rb') as file:
                self.model[key] = pickle.load(file)

    def predict(self, file_name: str):
        # Predict
        record_mfcc = preprocessing.get_mfcc(file_name)
        scores = [self.model[cname].score(record_mfcc) for cname in self.class_names]
        print('scores', scores)
        predict_word = np.argmax(scores)
        print(self.class_names[predict_word])

    def predict_record(self):
        file_name = self.record_path

        # Trim silence
        sound = AudioSegment.from_file(file_name, format=self.audio_format)

        start_trim = self.detect_leading_silence(sound)
        end_trim = self.detect_leading_silence(sound.reverse())

        duration = len(sound)

        trimmed_sound = sound[start_trim:duration - end_trim]
        trimmed_sound.export(self.trimmed_path, format=self.audio_format)

        # Predict
        record_mfcc = preprocessing.get_mfcc(self.trimmed_path)
        scores = [self.model[cname].score(record_mfcc) for cname in self.class_names]
        print('scores', scores)
        predict_word = np.argmax(scores)
        print(self.class_names[predict_word])

    def record(self, label="unknown"):
        CHUNK = 1024
        FORMAT = pyaudio.paInt16
        CHANNELS = 1
        RATE = 22050
        RECORD_SECONDS = 2

        p = pyaudio.PyAudio()

        stream = p.open(format=FORMAT,
                        channels=CHANNELS,
                        rate=RATE,
                        input=True,
                        frames_per_buffer=CHUNK)

        frames = []

        print('recording ...')
        for i in range(0, int(RATE / CHUNK * RECORD_SECONDS)):
            data = stream.read(CHUNK)
            frames.append(data)

        print('stopped record!')
        stream.stop_stream()
        stream.close()
        p.terminate()

        now_str = time.strftime("%Y%m%d_%H%M%S")

        print(f"{self.record_folder}/{label}/{label} {now_str}.wav")
        self.record_path = f"{self.record_folder}/{label}/{label} _ {now_str}.wav"
        self.trimmed_path = f"{self.trimmed_folder}/{label}/{label} _ {now_str}.wav"

        wf = wave.open(self.record_path, 'wb')
        wf.setnchannels(CHANNELS)
        wf.setsampwidth(p.get_sample_size(FORMAT))
        wf.setframerate(RATE)
        wf.writeframes(b''.join(frames))
        wf.close()


if __name__ == '__main__':
    hmm_reg = HMMRecognition()
    # hmm_reg.predict(file_name='datasets/cothe/cothe (1).wav')
    # hmm_reg.predict(file_name='datasets/khong/2.wav')
    # hmm_reg.predict(file_name='datasets/nhung/nhung_ (1).wav')
    hmm_reg.record("hai")
    hmm_reg.predict_record()
    # hmm_reg.predict('datasets_split/thodia/E52.wav')