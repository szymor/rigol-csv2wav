#!/bin/env python3

import csv
import numpy as np
import wave
import sys
from scipy.signal import resample, butter, filtfilt

def csv_to_wav(csv_filename, wav_filename):
    # Read the CSV file and extract sample rate from header
    with open(csv_filename, 'r') as csvfile:
        reader = csv.reader(csvfile)
        # Read the header
        header = next(reader)
        # Extract tInc value from the header
        tInc_str = header[2].split('=')[1].strip().split('s')[0]
        tInc = float(tInc_str)
        # Calculate sample rate
        sample_rate = int(1 / tInc)
        # Read the data
        data = [float(row[0]) for row in reader if row[0]]

    # Convert data to numpy array
    audio_data = np.array(data, dtype=np.float32)

    # Normalize the data
    max_val = np.max(np.abs(audio_data))
    if max_val > 0:
        audio_data = audio_data / max_val

    # Apply low-pass filter with cutoff frequency of 22 kHz
    cutoff_freq = 22000  # 22 kHz
    nyquist_rate = sample_rate / 2
    normal_cutoff = cutoff_freq / nyquist_rate
    b, a = butter(5, normal_cutoff, btype='low', analog=False)
    audio_data = filtfilt(b, a, audio_data)

    # Downsample to 48 kHz
    target_sample_rate = 48000
    num_samples = int(len(audio_data) * target_sample_rate / sample_rate)
    audio_data = resample(audio_data, num_samples)

    # Convert to 16-bit PCM
    audio_data = (audio_data * 32767).astype(np.int16)

    # Update sample rate to 48 kHz
    sample_rate = target_sample_rate

    # Write to WAV file
    with wave.open(wav_filename, 'w') as wavfile:
        wavfile.setnchannels(1)  # mono
        wavfile.setsampwidth(2)  # 2 bytes for 16-bit audio
        wavfile.setframerate(sample_rate)
        wavfile.writeframes(audio_data.tobytes())

if __name__ == "__main__":
    if len(sys.argv) != 3:
        print("Usage: csv2wav.py <input_csv_file> <output_wav_file>")
        sys.exit(1)

    csv_filename = sys.argv[1]
    wav_filename = sys.argv[2]
    csv_to_wav(csv_filename, wav_filename)
