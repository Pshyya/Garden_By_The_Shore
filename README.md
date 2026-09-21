# Garden By The Shore

## Lancer le jeu

Depuis ce dossier :

```bash
pip install pygame opencv-python
python Main.py
```

Le menu propose `Entrer dans le jeu` et `Quitter`. Pour afficher une cinematique,
ajoutez un fichier `.mp4`, `.mov`, `.avi`, `.mkv` ou `.webm` dans le dossier
`Videos/`. Le premier fichier trouve sera lu apres l'entree dans le jeu.

La touche `Echap` ferme le menu ou la scene de jeu. Pendant la cinematique,
`Echap` et `Espace` permettent de la passer.

## Images du personnage

Les images du MC se placent dans `Pictures/`. Utilisez des sous-dossiers nommes
`tete`, `cheveux`, `yeux`, `nez` et `bouche`. Les images transparentes de chaque
dossier deviennent automatiquement des choix dans l'interface Custom. Une image
nommee `MC.png`, `personnage.png` ou `base.png` sert de personnage de base.

Les fichiers `.png`, `.jpg`, `.jpeg` et `.webp` sont pris en charge. Les noms des
fichiers deviennent les libelles des choix.
