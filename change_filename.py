import os

mapping_dict_1 = {
    "001": "_s1_p00",
    "004": "_s1_p01",
    "005": "_s1_p02",
    "006": "_s1_p03",
    "007": "_s1_p04",
    "008": "_s1_p05",
    "009": "_s1_p06",
    "010": "_s1_p07",
    "011": "_s1_p08",
    "012": "_s1_p09",
    "013": "_s1_p10",
    "014": "_s1_p11",
    "015": "_s1_p12",
    "016": "_s1_p13",
    "018": "_s1_p14",
    "019": "_s1_p15",
    "020": "_s1_p16",
    "021": "_s1_p17",
    "022": "_s1_p18",
    "023": "_s1_p19",
    "024": "_s1_p20",
    "025": "_s1_p21",
    "026": "_s1_p22",
    "027": "_s1_p23",
}

mapping_dict_2 = {
    "030": "_s2_p00",
    "031": "_s2_p01",
    "032": "_s2_p02",
    "033": "_s2_p03",
    "034": "_s2_p04",
    "035": "_s2_p05",
    "036": "_s2_p06",
    "037": "_s2_p07",
    "038": "_s2_p08",
    "039": "_s2_p09",
    "040": "_s2_p10",
    "041": "_s2_p11",
    "042": "_s2_p12",
    "043": "_s2_p13",
    "044": "_s2_p14",
    "045": "_s2_p15",
    "046": "_s2_p16",
    "047": "_s2_p17",
    "048": "_s2_p18",
    "049": "_s2_p19",
    "050": "_s2_p20",
}

dict_mic = {
    "micA": "m1",
    "micB": "m2",
    "micC": "m3",
    "micD": "m4",
    "micE": "m5",
    "micF": "m6",
}

# Folder path
folder_path = "RIRs"

# # Iterate over files in the folder
# for file in os.listdir(folder_path):
#     # Split the file name and the extension
#     file_name, file_extension = os.path.splitext(file)
#     os.path.join(folder_path, file)
#     # Construct the file path
#     file_path = os.path.join(folder_path, file)
#     # Check if the file is a wav file
#     if file_extension != ".wav":
#         os.remove(file_path)
#     # Split the file name by underscore
#     file_name = file_name.split("_")
#     # Get the last element of the list
#     postfix = file_name[-1]
#     # Check if the file name is in the dictionary
#     if postfix in mapping_dict_1:
#         # Construct the new file name
#         new_file_name = file_name[0] + mapping_dict_1[postfix] + file_extension
#         # Construct the new file path
#         new_file_path = os.path.join(folder_path, new_file_name)
#         # Rename the file
#         os.rename(file_path, new_file_path)
#     elif postfix in mapping_dict_2:
#         # Construct the new file name
#         new_file_name = file_name[0] + mapping_dict_2[postfix] + file_extension
#         # Construct the new file path
#         new_file_path = os.path.join(folder_path, new_file_name)
#         # Rename the file
#         os.rename(file_path, new_file_path)
#     else:
#         os.remove(file_path)

# change file name from micA_s1_p00.wav to p00_s1_m1.wav
# Iterate over files in the folder
for file in os.listdir(folder_path):
    # Split the file name and the extension
    file_name, file_extension = os.path.splitext(file)
    os.path.join(folder_path, file)
    # Construct the file path
    file_path = os.path.join(folder_path, file)
    # Split the file name by underscore
    file_name = file_name.split("_")
    # Get the first element of the list
    prefix = file_name[0]
    # Get the second element of the list
    mid = file_name[1]
    # Get the last element of the list
    postfix = file_name[2]
    # Check if the file name is in the dictionary
    if prefix in dict_mic:
        # Construct the new file name
        new_file_name = mid + "_" + postfix + "_" + dict_mic[prefix] + file_extension
        # Construct the new file path
        new_file_path = os.path.join(folder_path, new_file_name)
        # Rename the file
        os.rename(file_path, new_file_path)
    else:
        os.remove(file_path)
