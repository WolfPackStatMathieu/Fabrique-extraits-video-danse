import csv
from moviepy.video.io.ffmpeg_tools import ffmpeg_extract_subclip
from moviepy.editor import VideoFileClip
import datetime
import re
import os
from tkinter import Tk
from tkinter.filedialog import askopenfilename
import re
from unidecode import unidecode

def clean_file_name(file_name):
    """Remove invalid characters from a file name."""
    file_name = unidecode(file_name)  # replace accented characters with non-accented equivalent
    return re.sub(r'[<>:"/\\|?*]', '_', file_name)  # replace invalid characters with underscore


def select_file(prompt, initial_dir):
    """Open a file dialog and return the path of the selected file."""
    Tk().withdraw()  # we don't want a full GUI, so keep the root window from appearing
    filename = askopenfilename(initialdir=initial_dir, title=prompt)  # show an "Open" dialog box and return the path to the selected file
    return filename


def convert_to_seconds(time_str):
    """Converts a string in format MM:SS into seconds."""
    m, s = re.split(':', time_str)
    return int(m) * 60 + int(s)

def lire_csv(fichier):
    """Read the lines from the CSV file and returns the title of the passage, start and end times."""
    with open(fichier, 'r') as f:
        reader = csv.DictReader(f)
        for row in reader:
            yield row['titre_passage'], row['debut'], row['fin']

# Specify default paths
default_video_path = "C:/Users/mathi/Videos/Fabrique à gif"
default_csv_path = "C:/Users/mathi/Videos/Fabrique à gif"

# Ask the user for the path of the video
chemin_video = select_file("Veuillez sélectionner le fichier vidéo"
                           , default_video_path)

# Ask the user for the name of the CSV file
nom_fichier_csv = select_file("Veuillez sélectionner le fichier CSV"
                              , default_csv_path)

# # Ask the user for the path of the video
# chemin_video = input("Veuillez entrer le chemin de la vidéo : ")

# # Ask the user for the name of the CSV file
# nom_fichier_csv = input("Veuillez entrer le nom du fichier CSV : ")

# List to store the names of temporary files
temp_files = []

# Initialize total size to 0
total_size = 0

for titre_passage, debut, fin in lire_csv(nom_fichier_csv):
    # Clean the passage title
    titre_passage = clean_file_name(titre_passage)

    start_time = convert_to_seconds(debut)
    end_time = convert_to_seconds(fin)

    # Extract the passage from the video
    temp_file_name = f"{titre_passage}_temp.mp4"
    ffmpeg_extract_subclip(chemin_video, start_time, end_time, targetname=temp_file_name)

    # Load the temporary clip and cut it again to the exact time range
    clip = VideoFileClip(temp_file_name).subclip(0, end_time - start_time)

    # Convert the passage to mp4 with reduced bitrate
    mp4_file_name = f"{titre_passage}.mp4"
    clip = clip.resize(width=1080)  # reduce resolution if necessary
    clip.write_videofile(mp4_file_name, codec='libx264', audio_codec='aac', bitrate="1200k")  # specify the codec and bitrate

    # Close the clip to free up resources
    clip.close()

    # Add the name of the temporary file to the list
    temp_files.append(temp_file_name)

    # Add the size of the mp4 to the total size
    total_size += os.path.getsize(mp4_file_name)

# Delete all temporary .mp4 files
for temp_file in temp_files:
    os.remove(temp_file)

# Convert total size to MB and display it
total_size_mb = total_size / (1024 * 1024)
print(f"La taille totale des .mp4 créés est de {total_size_mb:.2f} Mo.")
