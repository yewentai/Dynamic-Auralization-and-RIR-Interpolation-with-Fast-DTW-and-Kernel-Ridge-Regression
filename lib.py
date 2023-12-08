import matplotlib.pyplot as plt
import numpy as np


def edc_analyze(signal, sampling_rate, threshold=10e-2, plot=True):
    # Compute the energy decay curve (EDC)
    edc = np.cumsum(signal[::-1] ** 2)[::-1]

    # Normalize EDC to values between 0 and 1
    edc /= np.max(edc)

    # Find the index where EDC drops below the threshold
    early_echo_index = np.argmax(edc < threshold)

    time = np.arange(0, len(edc)) / sampling_rate
    # Plot the EDC and the signal if requested
    if plot:
        fig, axs = plt.subplots(2, 1, figsize=(12, 8))

        # Plot the Energy Decay Curve
        axs[0].plot(time, edc, label="Energy Decay Curve")
        axs[0].axvline(
            x=time[early_echo_index],
            color="r",
            linestyle="--",
            label="Early Echoes Threshold",
        )
        axs[0].set_title("Energy Decay Curve and Early Echoes Detection")
        axs[0].set_xlabel("Time (s)")
        axs[0].set_ylabel("Normalized Energy")
        axs[0].legend()

        # Plot the Signal
        axs[1].plot(time, signal)
        axs[1].axvline(
            x=time[early_echo_index],
            color="r",
            linestyle="--",
            label="Early Echoes Threshold",
        )
        axs[1].set_title("Signal and Early Echoes Detection")
        axs[1].set_xlabel("Time (s)")
        axs[1].set_ylabel("Amplitude")
        axs[1].legend()

        plt.tight_layout()
        plt.show()

    return early_echo_index, time[early_echo_index]


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


def plot_dtw_matrix(dtw_matrix, path):
    """
    Plots the DTW matrix and the path.

    Args:
    dtw_matrix (array-like): The DTW matrix.
    path (array-like): The path through the DTW matrix.
    """

    # Print the shape of the dtw_matrix
    print("Shape of DTW Matrix:", dtw_matrix.shape)

    # Plot the DTW matrix
    plt.figure(figsize=(10, 10))
    plt.imshow(dtw_matrix, origin="lower", cmap="gray")  # Gray colormap for visibility
    plt.colorbar()
    plt.title("DTW Matrix with Path")

    # Highlight the path on the plot
    plt.plot(path[:, 1], path[:, 0], color="r", marker="o", markersize=5)

    plt.show()
