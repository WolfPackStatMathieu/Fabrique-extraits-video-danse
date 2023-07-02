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
    """Converts a string in format HH:MM:SS, MM:SS or MM:SS.SS into seconds.
    Cette version de la fonction vérifie d'abord combien de parties il y a dans
    la chaîne de caractères. Si elle a trois parties, elle les traite comme
    des heures, des minutes et des secondes. Si elle a deux parties, elle les
    traite comme des minutes et des secondes. Si elle n'a pas deux ou trois parties
    , elle déclenche une exception ValueError, indiquant que le format de la chaîne
    de caractères n'est pas correct.
    Lorsque vous convertissez une chaîne de caractères en un entier avec int()
    ou un flottant avec float(), Python ignore les zéros non significatifs."""
    parts = time_str.split(':')
    if len(parts) == 3:
        hours = int(parts[0])
        minutes = int(parts[1])
        seconds = float(parts[2])
        return hours * 3600 + minutes * 60 + seconds
    elif len(parts) == 2:
        minutes = int(parts[0])
        seconds = float(parts[1])
        return minutes * 60 + seconds
    else:
        raise ValueError("Invalid time format, please use HH:MM:SS, MM:SS or MM:SS.SS")

def is_valid_time_format(time_str):
    """Check if the time format is valid (HH:MM:SS, MM:SS or MM:SS.SS).
    Voici ce que fait chaque partie de l'expression régulière :

    ^ et $ : Ces métacaractères correspondent respectivement au début et à la fin de la chaîne.
    Ils garantissent que toute la chaîne doit correspondre au motif, et pas seulement une partie de celle-ci.

    ([0-9]{1,2}:[0-5][0-9]:[0-5][0-9]) : Cette partie du motif correspond à une heure au format HH:MM:SS.
        [0-9]{1,2} correspond à un nombre d'un ou deux chiffres (de 0 à 99), représentant les heures.
        :[0-5][0-9] correspond à un deux-points suivi d'un nombre à deux chiffres compris entre 00 et 59,
        représentant les minutes et les secondes.

    | : C'est l'opérateur "OU" en expressions régulières. Il signifie que le motif peut correspondre à la
    partie précédente OU à la partie suivante.

    ([0-5]?[0-9]:[0-5][0-9](\.[0-9]{1,2})?) : Cette partie du motif correspond à un temps au format MM:SS
    ou MM:SS.SS.
        [0-5]?[0-9] correspond à un nombre à deux chiffres compris entre 00 et 59, avec le premier chiffre
        optionnel, représentant les minutes.
        :[0-5][0-9] correspond de nouveau à un deux-points suivi d'un nombre à deux chiffres compris entre
        00 et 59, représentant les secondes.
        (\.[0-9]{1,2})? correspond à une option de fractions de seconde, où un point est suivi d'un ou deux
        chiffres. Le point d'interrogation à la fin signifie que cette partie est optionnelle.

    En combinant tout cela, cette fonction vérifie si une chaîne donnée correspond à l'un de ces formats de
    temps valides : HH:MM:SS, MM:SS, ou MM:SS.SS, avec des heures, des minutes et des secondes facultativement
    fractionnaires.
    """
    # Define the regular expression (regex) pattern to match
    regex = "^(([0-9]{1,2}:[0-5][0-9]:[0-5][0-9])|([0-5]?[0-9]:[0-5][0-9](\.[0-9]{1,2})?))$"

    # Try to match the input string (time_str) with the regex pattern
    # If the input string matches the pattern, the match() function will return a Match object
    # Otherwise, it will return None
    # The "is not None" at the end translates this into a boolean, so the function returns True for a match and False otherwise
    return re.match(regex, time_str) is not None



def is_valid_row(row):
    """Check if a row from the CSV is valid."""
    titre_passage = row.get('titre_passage')
    debut = row.get('debut')
    fin = row.get('fin')

    if titre_passage is None or debut is None or fin is None:
        return False

    if not isinstance(titre_passage, str) or not is_valid_time_format(debut) or not is_valid_time_format(fin):
        return False
    else:
        return True


def check_csv_format(fichier):
    """Check the format of each row in the CSV file and that there are no duplicate passage titles."""
    problematic_rows = []  # stores problematic rows
    seen_titles = set()  # stores titles we've already seen
    with open(fichier, 'r') as f:
        reader = csv.DictReader(f)
        for row in reader:
            # Validate the format of each line
            if not is_valid_row(row):
                problematic_rows.append(row)
            else:
                # Check if we've seen this title before
                titre_passage = row['titre_passage']
                if titre_passage in seen_titles:
                    problematic_rows.append(row)
                else:
                    seen_titles.add(titre_passage)

    # If there were problematic rows, stop the program
    if problematic_rows:
        print("The following rows have invalid formats or duplicate titles:")
        for row in problematic_rows:
            print(row)
        raise ValueError("Invalid data found in CSV.")


def lire_csv(fichier):
    """Read the lines from the CSV file and returns the title of the passage, start and end times."""
    with open(fichier, 'r') as f:
        reader = csv.DictReader(f)
        for row in reader:
            yield row['titre_passage'], row['debut'], row['fin']



############ DEBUT ############
# Specify default paths
default_video_path = "C:/Users/mathi/Videos/Fabrique extraits video danse"
default_csv_path = "C:/Users/mathi/Videos/Fabrique extraits video danse"

# Ask the user for the path of the video
chemin_video = select_file("Veuillez sélectionner le fichier vidéo"
                           , default_video_path)

# Ask the user for the name of the CSV file
nom_fichier_csv = select_file("Veuillez sélectionner le fichier CSV"
                              , default_csv_path)

# Check the format of the CSV file
check_csv_format(nom_fichier_csv)

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
    try:
        ffmpeg_extract_subclip(chemin_video, start_time, end_time, targetname=temp_file_name)

        # Load the temporary clip and cut it again to the exact time range
        clip = VideoFileClip(temp_file_name).subclip(0, end_time - start_time)

        # Convert the passage to mp4 with reduced bitrate
        mp4_file_name = f"{titre_passage}.mp4"
        clip = clip.resize(width=1080)  # reduce resolution if necessary
        # clip.write_videofile(mp4_file_name, codec='libx264', audio_codec='aac', bitrate="1200k")  # specify the codec and bitrate
        clip.write_videofile(mp4_file_name, codec='mpeg4', audio_codec='aac', bitrate="1200k")

    except Exception as e:
        print(f"Error occurred while processing passage: {titre_passage}")
        print(f"Error message: {str(e)}")
    finally:
        # Close the clip to free up resources
        if 'clip' in locals():
            clip.close()


    # Add the name of the temporary file to the list
    temp_files.append(temp_file_name)

    # Add the size of the mp4 to the total size
    total_size += os.path.getsize(temp_file_name)

# Delete all temporary .mp4 files
for temp_file in temp_files:
    os.remove(temp_file)

# Convert total size to MB and display it
total_size_mb = total_size / (1024 * 1024)
print(f"La taille totale des .mp4 créés est de {total_size_mb:.2f} Mo.")
