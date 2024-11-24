# CSV to WAV Converter

This script, `csv2wav.py`, is designed to convert CSV files generated by the Rigol MSO5354 oscilloscope into WAV audio files. The script reads the CSV file, extracts the numerical data, applies a low-pass filter, downsamples the data to 48 kHz, and then writes it to a WAV file.

## Requirements

- Python 3
- NumPy
- SciPy

## Installation

To install the required Python packages, run:

```bash
pip install numpy scipy
```

## Usage

To use the script, run the following command:

```bash
python3 csv2wav.py <input_csv_file> <output_wav_file>
```

Replace `<input_csv_file>` with the path to your CSV file and `<output_wav_file>` with the desired path for the output WAV file.

## Example

```bash
python3 csv2wav.py example.csv output.wav
```

This command will convert `example.csv` to `output.wav`.

## Notes

- The script assumes that the CSV file contains a header with a `tInc` value, which is used to calculate the sample rate.
- The audio data is normalized and converted to 16-bit PCM format before being saved as a WAV file.
