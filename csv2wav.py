#!/bin/env python3

import csv
import numpy as np
import wave
import sys

def csv_to_wav(csv_filename, wav_filename, sample_rate=44100):
    # Read the CSV file and extract sample rate from header
    with open(csv_filename, 'r') as csvfile:
        reader = csv.reader(csvfile)
        # Read the header
        header = next(reader)
        # Extract tInc value from the header
        tInc_str = header[1].split('=')[1].strip().split('s')[0]
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

    # Convert to 16-bit PCM
    audio_data = (audio_data * 32767).astype(np.int16)

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
