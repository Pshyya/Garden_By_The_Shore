# Garden By The Shore

## Lancer le jeu

Depuis ce dossier :

```bash
pip install pygame opencv-python
python Main.py
```

Le menu propose `Entrer dans le jeu` et `Quitter`. Apres `Entrer`, choisissez une
des cinq histoires de Lily Himo. Les cinq emplacements sont respectivement rouge,
bleu, vert, jaune et violet.

La touche `Echap` ferme le menu ou la scene de jeu. Pendant la cinematique,
`Echap` et `Espace` permettent de la passer.

## Images du personnage

Les images du MC se placent dans `Pictures/`. L'image de Lily Himo peut rester
directement dans ce dossier. Pour ajouter des variantes, utilisez des sous-dossiers nommes
`tete`, `cheveux`, `yeux`, `nez` et `bouche`. Les images transparentes de chaque
dossier deviennent automatiquement des choix dans l'interface Custom. Une image
nommee `MC.png`, `personnage.png` ou `base.png` sert de personnage de base.

Les fichiers `.png`, `.jpg`, `.jpeg` et `.webp` sont pris en charge. Les noms des
fichiers deviennent les libelles des choix.
