###############################################################################
# Import required libraries
###############################################################################
import numpy as np
import matplotlib.pyplot as plt
import soundfile as sf
import os

from lib import ess_gen_farina, ess_parse_farina

###############################################################################
# Create Exponential Sine Sweep from parameters
###############################################################################
fs = 48000  # Sampling Frequency [Hz]

f1 = 20  # Initial frequency [Hz]
f2 = fs // 2  # Final frequency [Hz]

T_sweep = 10  # Sweep duration [sec.]
T_idle = 3  # Idle duration [sec.]

fade_in = int(0.100 * fs)  # fade-in window of 100 ms [samples]

t_sweep = np.arange(0, (T_sweep + T_idle) * fs) / fs  # Time vector [sec.]

###############################################################################
# Generate exponential sine sweep and its inverse filter
###############################################################################
sweep, inverse = ess_gen_farina(
    f1, f2, T_sweep, T_idle, fs, fade_in=fade_in, cut_zerocross=True
)

###############################################################################
# Perform deconvolution with measured sweep
###############################################################################
src_folder = "./fixed_position_sinesweep"
dst_folder = "./RIRs"

for file in os.listdir(src_folder):
    measured_sweep = sf.read(os.path.join(src_folder, file))[0]
    rir = ess_parse_farina(measured_sweep, inverse, T_sweep, T_idle, fs, causality=True)
    sf.write(os.path.join(dst_folder, file), rir, fs, subtype="FLOAT")
