```markdown
# Script de découpe vidéo avec réduction de la résolution et nettoyage des noms de fichiers

Ce script Python permet de découper une vidéo en utilisant un fichier CSV contenant les informations sur les passages à extraire. Il réduit également la résolution des clips vidéo générés et nettoie les noms de fichiers en remplaçant les caractères invalides et accentués.

## Prérequis

- Python 3.x
- MoviePy (installé avec `pip install moviepy`)
- Unidecode (installé avec `pip install unidecode`)

## Utilisation

1. Assurez-vous que vous avez installé les prérequis mentionnés ci-dessus.

2. Placez votre fichier vidéo dans le répertoire spécifié par `default_video_path` dans le script. Vous pouvez également spécifier un autre chemin lors de l'exécution du script.

3. Créez un fichier CSV avec les informations sur les passages à extraire. Le fichier CSV doit contenir les colonnes suivantes : `titre_passage`, `debut`, `fin`. Assurez-vous que le fichier CSV est bien formaté.

4. Exécutez le script en utilisant la commande suivante :

   ```bash
   python decoupe_avec_son.py
   ```

   Le script vous guidera pour sélectionner le fichier vidéo et le fichier CSV.

5. Le script découpera la vidéo en utilisant les informations du fichier CSV, réduira la résolution des clips vidéo générés si nécessaire, et nettoiera les noms de fichiers en remplaçant les caractères invalides et accentués.

6. Les clips vidéo générés seront enregistrés dans le même répertoire que le script.

## Remarques

- Assurez-vous d'avoir suffisamment d'espace disque disponible pour stocker les clips vidéo générés.

- Vérifiez que les chemins spécifiés dans le script correspondent à votre configuration.

- Assurez-vous que les dépendances requises sont correctement installées.

- Ce script utilise la bibliothèque MoviePy pour la manipulation vidéo et la bibliothèque Unidecode pour la gestion des caractères accentués. Assurez-vous d'avoir installé ces bibliothèques avant d'exécuter le script.

---

*Ce script a été développé pour répondre à un besoin spécifique et peut nécessiter des adaptations pour fonctionner avec d'autres configurations ou besoins particuliers.*
```
