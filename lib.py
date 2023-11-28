import matplotlib.pyplot as plt
import numpy as np
import numpy as np
from scipy.signal import correlate


def edc_analyze(signal, sampling_rate, threshold=0.1, plot=True):
    # Compute the energy decay curve (EDC)
    edc = np.cumsum(signal[::-1] ** 2)[::-1]

    # Normalize EDC to values between 0 and 1
    edc /= np.max(edc)

    # Find the index where EDC drops below the threshold
    early_echo_index = np.argmax(edc < threshold)

    # Plot the EDC if requested
    if plot:
        time = np.arange(0, len(edc)) / sampling_rate
        plt.figure(figsize=(12, 4))
        plt.plot(time, edc, label="Energy Decay Curve")
        plt.axvline(
            x=time[early_echo_index],
            color="r",
            linestyle="--",
            label="Early Echoes Threshold",
        )
        plt.title("Energy Decay Curve and Early Echoes Detection")
        plt.xlabel("Time (s)")
        plt.ylabel("Normalized Energy")
        plt.legend()
        plt.show()

    return early_echo_index, time[early_echo_index]


def align_signals(signal1, signal2):
    """
    Align two signals in time using cross-correlation.

    Parameters:
    - signal1: The first signal.
    - signal2: The second signal.

    Returns:
    - aligned_signal1: The aligned first signal.
    - aligned_signal2: The aligned second signal.
    """

    # Calculate cross-correlation
    cross_corr = correlate(signal2, signal1, mode="full")

    # Find the time offset (index of the maximum correlation)
    time_offset = np.argmax(cross_corr) - len(signal1) + 1

    # Apply the time shift to align the signals
    if time_offset > 0:
        aligned_signal1 = signal1[time_offset:]
        aligned_signal2 = signal2[: len(signal2) - time_offset]
    elif time_offset < 0:
        aligned_signal1 = signal1[: len(signal1) + time_offset]
        aligned_signal2 = signal2[-time_offset:]
    else:
        aligned_signal1 = signal1
        aligned_signal2 = signal2

    return aligned_signal1, aligned_signal2


import numpy as np
from scipy.signal import correlate, find_peaks


def align_signals_peaks(*signals):
    """
    Align multiple signals in time using peak alignment of cross-correlation.

    Parameters:
    - signals: Variable number of input signals.

    Returns:
    - aligned_signals: Tuple of aligned signals.
    """

    num_signals = len(signals)

    # Calculate cross-correlation for each pair of signals
    cross_corrs = []
    for i in range(num_signals):
        for j in range(i + 1, num_signals):
            cross_corr = correlate(signals[i], signals[j], mode="full")
            cross_corrs.append(cross_corr)

    # Find the peaks in cross-correlation
    peak_indices = np.argmax(np.abs(cross_corrs), axis=1)

    # Find the time offset using peak indices
    time_offsets = [
        (index - len(signals[i]) + 1) for i, index in enumerate(peak_indices)
    ]

    # Find the maximum time offset (most delayed signal)
    max_offset = max(time_offsets, key=abs)

    # Apply the time shift to align the signals
    aligned_signals = []
    for i in range(num_signals):
        if max_offset > 0:
            aligned_signals.append(signals[i][max_offset:])
        elif max_offset < 0:
            aligned_signals.append(signals[i][: len(signals[i]) + max_offset])
        else:
            aligned_signals.append(signals[i])

    return tuple(aligned_signals)


import numpy as np


def construct_interpolated_point_cloud(P, Q, kappa, T_bar):
    K = 0  # Point index
    T_prime = np.copy(T_bar)  # Redistributed transport plan
    interpolated_points = np.empty((0, 3))  # Initialize an empty array for the result

    # Iterate over rows (i) in transport plan T_bar
    for i in range(len(P)):
        if np.linalg.norm(T_bar[i, :]) == 0:
            # Add a vanishing point
            r = (1 - kappa) * P[i, 2]  # Assuming P has a third column for weights
            z = P[i, :2]  # Static position
            K += 1
            point = np.array([r, *z])
            interpolated_points = np.vstack((interpolated_points, point))
        else:
            T_prime[i, :] += (
                (1 - kappa) * P[i, 2] * T_bar[i, :] / np.linalg.norm(T_bar[i, :])
            )

            # Iterate over columns (j) in transport plan T_bar
            for j in range(len(Q)):
                if np.linalg.norm(T_bar[:, j]) == 0:
                    # Add an appearing point
                    r = kappa * Q[j, 2]  # Assuming Q has a third column for weights
                    z = Q[j, :2]  # Static position
                    K += 1
                    point = np.array([r, *z])
                    interpolated_points = np.vstack((interpolated_points, point))
                else:
                    T_prime[:, j] += (
                        kappa * Q[j, 2] * T_bar[:, j] / np.linalg.norm(T_bar[:, j])
                    )

                    # Check if the redistributed transport plan is greater than zero
                    if T_prime[i, j] > 0:
                        # Add a moving point
                        r = T_prime[i, j] * P[i, 2]
                        z = (1 - kappa) * P[i, :2] + kappa * Q[
                            j, :2
                        ]  # Position interpolation
                        K += 1
                        point = np.array([r, *z])
                        interpolated_points = np.vstack((interpolated_points, point))

    return interpolated_points


def cal_dtw_matrix(s, t):
    n, m = len(s), len(t)

    # Initialize the DTW matrix and path matrices
    dtw_matrix = np.full((n + 1, m + 1), np.inf)
    path_matrix = np.zeros((n + 1, m + 1, 2), dtype=int)  # 2D array to store the path

    # Set the initial value to 0
    dtw_matrix[0, 0] = 0

    for i in range(1, n + 1):
        for j in range(1, m + 1):
            # Compute the cost between elements s[i-1] and t[j-1]
            cost = abs(s[i - 1] - t[j - 1])

            # Update the DTW matrix and path matrix
            candidates = [
                (dtw_matrix[i - 1, j], i - 1, j),  # insertion
                (dtw_matrix[i, j - 1], i, j - 1),  # deletion
                (dtw_matrix[i - 1, j - 1], i - 1, j - 1),  # match
            ]
            min_candidate = min(candidates, key=lambda x: x[0])

            dtw_matrix[i, j] = cost + min_candidate[0]
            path_matrix[i, j] = [min_candidate[1], min_candidate[2]]

    # Backtrack to find the optimal alignment path
    i, j = n, m
    path = [(i, j)]
    while i > 0 or j > 0:
        i, j = path_matrix[i, j]
        path.append((i, j))

    # Reverse the path to get the correct order
    path.reverse()

    return dtw_matrix, np.array(path)
