import matplotlib
matplotlib.use('Agg')
import numpy as np
import matplotlib.pyplot as plt
import os
import pandas as pd
import xlsxwriter


# -----------------------------
# ADC PARAMETERS
# -----------------------------
sample_rate = 1000
min_AnaVal = 0
max_AnaVal = 5.0
min_DigiVal = 0
max_DigiVal = 1023
Vref = 5.0
resolution = 10
levels = 2**resolution

# -----------------------------
# CREATE A FAKE ANALOG SIGNAL
# -----------------------------
t = np.linspace(0, 1, sample_rate)
freq = 5
analog_signal = 2.5 + 2*np.sin(2*np.pi*freq*t)

# -----------------------------
# ADD NOISE (REALISTIC INPUT)
# -----------------------------
noise_amplitude = 0.3
noise = np.random.normal(0, noise_amplitude, size=analog_signal.shape)

# This is now the REAL analog input to the ADC
noisy_signal = analog_signal + noise


# -----------------------------
# LOW-PASS FILTER (IIR)
# -----------------------------
filtered_signal = np.zeros_like(noisy_signal)
alpha = 0.1

for i in range(1, len(noisy_signal)):
    filtered_signal[i] = alpha * noisy_signal[i] + (1 - alpha) * filtered_signal[i - 1]


adc_counts = np.round((filtered_signal / Vref) * (levels - 1))
adc_counts = np.clip(adc_counts, 0, levels - 1)
reconstructed_signal = (adc_counts / (levels - 1)) * Vref
# -----------------------------
# SUBPLOTS (ONE WINDOW)
# -----------------------------
fig, (ax1, ax2, ax3) = plt.subplots(3, 1, figsize=(12, 10), sharex=True)

ax1.plot(t, noisy_signal, color="orange")
ax1.set_title("Noisy Signal")
ax1.grid(True)

ax2.plot(t, filtered_signal, color="green")
ax2.set_title("Filtered Signal (IIR Low-Pass)")
ax2.grid(True)

ax3.step(t, reconstructed_signal, where='mid', color="blue")
ax3.set_title("Quantized Filtered Signal (ADC Steps)")
ax3.grid(True)

plt.tight_layout()
#plt.show()

# -----------------------------------------
# EXPORT FOLDER (Documents)
# -----------------------------------------
export_folder = r"exports"
if not os.path.exists(export_folder):
    os.makedirs(export_folder)

# -----------------------------------------
# SAVE PLOTS AS PNG FILES
# -----------------------------------------

export_folder = "exports"

# Create export folder
os.makedirs(export_folder, exist_ok=True)

# Define output paths
noisy_plot_path = os.path.join(export_folder, "noisy_signal.png")
filtered_plot_path = os.path.join(export_folder, "filtered_signal.png")
quantized_plot_path = os.path.join(export_folder, "quantized_signal.png")



if not os.path.exists(export_folder):
    os.makedirs(export_folder)
    filtered_plot_path = os.path.join(export_folder, "filtered_signal.png")
    quantized_plot_path = os.path.join(export_folder, "quantized_signal.png")

# Save the last three figures you created
plt.figure(figsize=(12, 4))
plt.plot(t, noisy_signal, color="orange")
plt.title("Noisy Signal")
plt.grid(True)
plt.savefig(noisy_plot_path)
plt.close()

plt.figure(figsize=(12, 4))
plt.plot(t, filtered_signal, color="green")
plt.title("Filtered Signal")
plt.grid(True)
plt.savefig(filtered_plot_path)
plt.close()

plt.figure(figsize=(12, 4))
plt.step(t, reconstructed_signal, where='mid', color="blue")
plt.title("Quantized Filtered Signal (ADC Steps)")
plt.grid(True)
plt.savefig(quantized_plot_path)
plt.close()

# -----------------------------------------
# BUILD DATAFRAME FOR EXCEL
# -----------------------------------------
df = pd.DataFrame({
    "Time (s)": t,
    "Noisy Signal (V)": noisy_signal,
    "Filtered Signal (V)": filtered_signal,
    "Quantized Signal (V)": reconstructed_signal,
    "ADC Counts": adc_counts.astype(int)
})

# -----------------------------------------
# CREATE EXCEL FILE WITH EMBEDDED IMAGES
# -----------------------------------------
excel_path = os.path.join(export_folder, "adc_output.xlsx")

with pd.ExcelWriter(excel_path, engine="xlsxwriter") as writer:
    # Write data sheet
    df.to_excel(writer, sheet_name="ADC Values", index=False)

    workbook = writer.book
    worksheet = workbook.add_worksheet("Graphs")

    # Insert images into the "Graphs" sheet
    worksheet.insert_image("A1", noisy_plot_path)
    worksheet.insert_image("A25", filtered_plot_path)
    worksheet.insert_image("A49", quantized_plot_path)

print("Export complete! Files saved to:", export_folder)
