
# Générateur de Grilles de Bingo

Ce script Python génère des grilles de bingo personnalisées à partir d'un dossier d'images.

## Installation

1. Assurez-vous d'avoir Python installé sur votre système. 
Sur windows télécharger le programme d'installation sur https://www.python.org/ et cocher la case "Add Python x.x to PATH" lors de l'installation.
2. Clonez ce dépôt ou télécharger le zip (bouton **<> Code**).

## Dépendances

Ce script nécessite les bibliothèques Python suivantes :
- `PIL` (Pillow)
- `reportlab`
- `PyPDF2`
- `tqdm`
- `tkinter`

Vous pouvez les installer via les étapes suivantes : 
1. Ouvrez un terminal ou une invite de commande et naviguez jusqu'au répertoire **gridGenerator**. 
(Par exemple : ```cd Bureau/gridGenerator```)

2. Exécutez la commande suivante : ``pip install Pillow reportlab PyPDF2 tqdm``


## Utilisation

1. Ouvrez un terminal ou une invite de commande.

2. Naviguez jusqu'au répertoire où se trouve le fichier `bingo_generator.py`. 
(Par exemple : ```cd Bureau/gridGenerator```)

3. Exécutez le script en utilisant la commande suivante : `python bingo_generator.py`


4. Une interface graphique s'ouvrira, vous permettant de spécifier les paramètres de génération des grilles de bingo.

## Paramètres

- **Dossier d'images**: Chemin vers le dossier contenant les images à utiliser dans les grilles. (Pour l'instant, il est préférable de déplacer vos images dans le dossier **images** présent dans le projet. Assurez vous d'avoir autant d'images que de cases à remplir.)
- **Nombre de lignes**: Nombre de lignes dans chaque grille de bingo.
- **Nombre de colonnes**: Nombre de colonnes dans chaque grille de bingo.
- **Taille de la bordure**: Taille de la bordure autour de chaque image dans la grille.
- **Nombre d'images à remplir**: Nombre d'images à placer dans chaque grille.
- **Nombre de grilles à générer**: Nombre total de grilles de bingo à générer.
- **Nom du fichier de sortie**: Nom du fichier PDF combiné contenant toutes les grilles générées. Le fichier sera créé dans le dossier **gridGenerator**.


