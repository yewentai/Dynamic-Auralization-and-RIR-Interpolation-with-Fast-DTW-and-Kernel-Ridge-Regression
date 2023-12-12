import os

# Set the directory where you want to delete files
directory = "data\RIRs"

# Iterate over the files in the directory
for filename in os.listdir(directory):
    # Check if 'i' is in the filename
    if "i" in filename.lower():
        # Create the full file path
        file_path = os.path.join(directory, filename)
        # Delete the file
        os.remove(file_path)
        print(f"Deleted {filename}")
