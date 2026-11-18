# /brag — Place2b2026 (« The place to be 2026 »)

## Ce que c'est
Un seul fichier HTML qui place les étudiants infirmiers en stage : carte des lieux et des étudiants, temps de trajet en voiture, placement automatique optimal, parcours par typologie (programme 2026 : SPA, SPS, SPR, VDE). Pour les formateurs d'IFSI. Rien à installer.

- **Pour qui :** les formateurs d'IFSI qui répartissent une promotion entre les lieux de stage.
- **Ce qui le distingue :** l'algorithme hongrois répartit tout le monde d'un coup, en tenant compte de qui a une voiture ; un seul fichier, aucun serveur, aucun compte ; les noms ne quittent jamais l'ordinateur.
- **La réplique la plus forte (tirée du README) :** « deux trajets de 25 minutes valent mieux qu'un de 10 et un de 40 ».
- **Accroche visuelle :** la carte qui se remplit d'épingles, puis 24 liaisons qui se tracent d'un coup au clic sur « Placement automatique ».
- **Légende à partager :** « Placer toute une promo en stage, en un fichier HTML. »

## Angle
Entrée → action clé → résultat, avec la vraie interface : deux fichiers Excel → la carte → *Placement automatique* → « Tous les étudiants sont placés » → les parcours en couleurs. Ton : `default`, dynamique et propre, avec la touche brutaliste de l'app (contours francs, ombres dures, jaune #f59e0b, rouge #e11d48, Space Grotesk + Inter).

## Matériel réel utilisé
- Instantanés DOM de la vraie application (CSS, balisage, icônes, logo, polices Inter intégrée + Space Grotesk), pris dans Chromium après import, après placement automatique et dans la vue Parcours. Animés image par image (aucun script de l'app dans la vidéo).
- Fond de carte Plan IGN mis en cache localement.
- Chiffres affichés = vrai résultat de l'app sur les données de démo : 24/24 placés, trajet moyen 17 min, trajet max 34 min.

## Données
**100 % fictives**, dans le style des modèles Excel de l'app (Réglages › Modèles) : 24 étudiants (MARTIN Alice, BERNARD Lucas…) et 24 places dans 14 lieux aux noms inventés (Clinique des Tilleuls, EHPAD Les Glycines…). Les adresses sont des rues génériques de communes de Seine-Maritime/Eure, choisies pour que le géocodage tombe juste. Aucune donnée réelle d'étudiant.

## Musique
120 BPM (1 temps = 0,5 s = 15 images, 1 mesure = 2 s), do majeur, C–G–Am–F. Synthétisée (kick, clap, charleston, basse, accords, mélodie) ; effets (whoosh, pops, clics) dans la même tonalité et sur la même grille. Lever de 2 temps, drop à 3,0 s. Tous les plans coupent sur un temps.

## Storyboard (22 s, 30 i/s, 1920×1080)

| # | Temps | Scène | À l'écran | Son |
|---|---|---|---|---|
| 1 | 0,0–3,0 | **Accroche** | Fond jaune. « Étudiants infirmiers. » + carte `etudiants.xlsx` (t=0) ; « Lieux de stage. » + carte `lieux-de-stage.xlsx` (t=1,0) ; « Qui va où ? » en rouge (t=2,0) | Accords filtrés, claps, montée |
| 2 | 3,0–7,0 | **Révélation** | Coupe franche sur la vraie app (fenêtre brutaliste). Les épingles tombent, les points bleus apparaissent. Légende « Stages en rouge. Étudiants en bleu. » (texte de l'app). La caméra glisse vers le bouton jaune | Drop, pops sur les doubles-croches |
| 3 | 7,0–11,0 | **Action** | Curseur, clic sur *Placement automatique* (7,5), vraie boîte de dialogue (35 min / 20 min), clic sur *Lancer le placement* (8,5). Les 24 liaisons se tracent, les points passent au vert, les badges d'épingles décomptent jusqu'à ✓, les compteurs passent à 24/24. Légende « Placement automatique. » | Clics, arpège montant |
| 4 | 11,0–13,0 | **Résultat** | Vraie fenêtre « Tous les étudiants sont placés » : 24/24 · 17 min · 34 min | Impact |
| 5 | 13,0–15,0 | **Le malin** | Fond encre. « Des trajets raisonnables pour tous. » 10 + 40 min ✗ contre 25 + 25 min ✓ | Break, sans kick |
| 6 | 15,0–16,94 | **Parcours** | Vraie vue Parcours : les cartes SPA/SPS/SPR/VDE tombent colonne par colonne, la colonne « Stage 3A » (prévu) en dernier. Légende « Chaque parcours, typologie par typologie. » | Retour du groove |
| 7 | 16,94–22,0 | **Final** | Balayage jaune, logo + « The place to be 2026 », « Un seul fichier HTML. Rien à installer. », « Logiciel libre · github.com/lcssrd/Place2b2026 » | Accord final à 21,0 s |

## Rendu
- Composition HTML (`work/comp.html`) animée par une fonction pure du temps, capturée image par image dans Chromium (Playwright), encodée en H.264 (CRF 16) ; bande-son synthétisée en Python/numpy (`work/music.py`), normalisée à -14 LUFS (crête -2,3 dBFS).
- Récupéré pendant la fabrication : la police Space Grotesk (Google Fonts) et les tuiles du Plan IGN (mises en cache dans `work/`) ; le géocodage et les temps de trajet ont été calculés par l'application elle-même (IGN, BAN, OSRM) sur les adresses fictives.
- Affiche : image à 10,75 s (carte avec les 24 liaisons et « Toute la promo, d'un coup. »), intégrée comme image 0.

## Contrôles prévus
Images fixes de chaque scène et à chaque fin/début de transition (2,85 / 3,0 / 6,9 / 8,5 / 10,9 / 12,9 / 13,1 / 14,9 / 15,1 / 16,9 / 17,1), nombre d'images = 22 × 30 = 660, image 0 = affiche.
