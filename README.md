# ADC Python Simulation ⚡️

**A small simulation that demonstrates analog-to-digital conversion (ADC):** generates a noisy sine wave, applies a simple IIR low-pass filter, quantizes it to ADC counts, and exports plots and an Excel workbook with the results.

---

## Table of Contents

- [Features](#features)
- [Requirements](#requirements)
- [Installation](#installation)
- [Usage](#usage)
- [Configuration](#configuration)
- [Output](#output)
- [Project Structure](#project-structure)
- [Development & Testing](#development--testing)
- [Contributing](#contributing)
- [License](#license)

---

## 🔧 Features

- Simulates a noisy analog signal (sine wave + Gaussian noise)
- Simple IIR low-pass filtering
- Quantization to ADC counts for a configurable bit resolution
- Exports PNG plots and an Excel workbook (`adc_output.xlsx`) with embedded images

---

## 🧰 Requirements

- Python 3.8+ recommended
- Minimal packages used by the script:
  - `numpy`
  - `matplotlib`
  - `pandas`
  - `xlsxwriter`

> Note: This repository includes a `requirements.txt` which contains many packages; for running the simulation only the minimal packages above are needed.

---

## 🚀 Installation

1. Create and activate a virtual environment:

```bash
# macOS / Linux / WSL
python -m venv .venv
source .venv/bin/activate

# Windows (cmd)
python -m venv .venv
.venv\Scripts\activate
```

2. Install runtime dependencies (minimal):

```bash
pip install numpy matplotlib pandas xlsxwriter
```

Or install everything listed in the repo `requirements.txt` (optional):

```bash
pip install -r requirements.txt
```

---

## ▶️ Usage

Run the simulation script directly:

```bash
python src/ADC.py
```

This will create an `exports/` folder (if it does not exist) and write:

- `noisy_signal.png`
- `filtered_signal.png`
- `quantized_signal.png`
- `adc_output.xlsx`

Open `adc_output.xlsx` to view the table of values with embedded graphs.

---

## ⚙️ Configuration

The script uses a few top-level variables for quick configuration. Open `src/ADC.py` and adjust the values as needed. Key parameters include:

- `sample_rate` (int) — number of samples per second (default: `1000`)
- `freq` (int) — sine frequency in Hz (default: `5`)
- `noise_amplitude` (float) — standard deviation of Gaussian noise added to the signal (default: `0.3`)
- `alpha` (float) — IIR low-pass filter coefficient between 0 and 1 (default: `0.1`)
- `resolution` (int) — ADC resolution in bits (default: `10`)
- `Vref` (float) — ADC reference voltage (default: `5.0`)

Example: to change the ADC to 12-bit resolution, edit at the top of `src/ADC.py`:

```python
resolution = 12
levels = 2**resolution
```

If you'd rather pass parameters at runtime, I can add a small CLI wrapper (let me know and I will add it).

---

## 📦 Output Format

- The PNGs are saved in `exports/` and show the noisy input, filtered signal, and quantized (ADC) signal.
- `adc_output.xlsx` contains a sheet `ADC Values` with columns:
  - `Time (s)`
  - `Noisy Signal (V)`
  - `Filtered Signal (V)`
  - `Quantized Signal (V)`
  - `ADC Counts`
- A `Graphs` sheet includes the embedded images for quick visualization inside Excel.

---

## 📁 Project Structure

```
ADC_Python_Simulation/
├── README.md
├── requirements.txt    # optional environment deps
├── exports/            # generated output (plots + excel)
└── src/
    └── ADC.py          # main simulation script
```

---

## Development & Testing

- If you add functions or split simulation logic into importable modules, consider adding unit tests using `pytest`.
- For small refactors, keep deterministic outputs by seeding the random generator (e.g., `np.random.seed(0)`) when writing tests.

---

## Contributing

Contributions are welcome! Typical ways to contribute:

- Open an issue to report a bug or request a change
- Submit a pull request with a small, well-scoped change and a short description

Please follow usual practices: fork, branch, test, and create a PR.

---

## License

This project is provided under the MIT License — feel free to adapt as needed.

---

If you want, I can:

- Add a CLI to `src/ADC.py` (allow command-line parameters and output directory), ✅
- Add unit tests and a GitHub Actions workflow, or
- Add an example notebook that runs the simulation and displays the plots inline.

Tell me which option you'd like next and I'll implement it.