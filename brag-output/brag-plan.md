# /brag — Place2b2026 (« The place to be 2026 ») · v2

## Ce que c'est
Un seul fichier HTML qui aide les formateurs d'IFSI à placer les étudiants infirmiers en stage : tous les lieux de stage et toutes les adresses d'étudiants sur une carte, avec le temps de trajet en voiture entre chaque étudiant et chaque lieu. Rien à installer.

## Angle (v2, d'après les retours)
- **Mis en avant :** la vue d'ensemble (toute la promo sur une carte) et la facilité à voir la distance entre l'adresse d'un étudiant et les lieux de stage.
- **Retiré :** le placement automatique (et la vue Parcours), pour garder un seul message.
- **Légendes :** une seule à la fois, jamais collées l'une à l'autre.
- **Son :** vraie musique produite à la place de la synthèse.

Accroche : « Étudiants infirmiers. Lieux de stage. À combien de minutes ? » L'app répond : on voit tout le monde sur la carte ; un clic sur une étudiante affiche ses places libres triées par temps de trajet ; le survol d'une place trace le trajet avec « 19 min · 20 km ».

## Matériel réel utilisé
- Instantanés DOM de la vraie application (CSS, balisage, icônes, logo, polices), pris dans Chromium : vue d'ensemble, étudiante sélectionnée, puis deux aperçus de trajet obtenus en survolant réellement les lignes de la liste. Animés image par image, sans les scripts de l'app.
- Le zoom de la vue d'ensemble (niveau 10) vers le secteur de l'étudiante (niveau 11) est un vrai changement de niveau de carte : agrandissement des tuiles puis fondu court vers l'instantané au niveau 11.
- Temps affichés = calcul réel de l'app (OSRM) sur les adresses fictives : BONNET Manon (Pavilly, sans voiture, limite 20 min) → 19 min · 20 km (Rouen, vert), 22 min · 18,2 km (Yvetot, orange).

## Données
100 % fictives, dans le style des modèles Excel de l'app : 24 étudiants, 24 places dans 14 lieux aux noms inventés. Les adresses sont des rues génériques de communes de Seine-Maritime et de l'Eure, choisies pour que le géocodage tombe juste.

## Son
- Musique : « Happy Beats / Business Moves Vol. 12 » de Sascha Ende (ende.app), licence CC BY 4.0. Crédit dans la vidéo (écran final) et dans le texte de partage. Extrait de 5,42 s à 24,92 s du morceau, à 110 BPM : l'intro sans basse porte l'accroche, et la basse et la batterie entrent pile quand l'app apparaît (3,27 s).
- Bruitages : Kenney (CC0), discrets, choisis parmi les sons les moins agressifs (chocs sourds, clic, survol, cloche finale).
- Mixage normalisé à -14 LUFS, crête -1,7 dBFS.

## Storyboard (19,5 s, 30 i/s, 1920×1080, un temps = 0,5454 s)

| # | Temps | Scène | À l'écran |
|---|---|---|---|
| 1 | 0–3,27 | **Accroche** | Fond jaune, cartes `etudiants.xlsx` et `lieux-de-stage.xlsx`. « Étudiants infirmiers. » (0), « Lieux de stage. » (0,82), « À combien de minutes ? » (1,64) |
| 2 | 3,27–7,09 | **Vue d'ensemble** | Vraie app. Les épingles tombent, les points des étudiants apparaissent. Légende unique : « Toute la promo, d'un coup d'œil. » avec le code couleur (lieux de stage / étudiants) |
| 3 | 7,09–9,82 | **Un clic** | Le curseur clique sur BONNET Manon, sa fiche glisse, la carte zoome sur Pavilly, la colonne défile jusqu'à « Places libres les plus proches » (5, 19, 21, 22 min…). Légende : « Un clic : ses stages les plus proches. » |
| 4 | 9,82–14,18 | **Les distances** | Survol de « Accueil de jour » : trajet tracé, « 19 min · 20 km », bulles étudiante et lieu. Puis survol de « Unité de vie protégée » : « 22 min · 18,2 km » vers Yvetot. Légende : « Chaque trajet, en minutes et en km. » |
| 5 | 14,18–19,5 | **Final** | Logo, « The place to be 2026 », « Un seul fichier HTML. Rien à installer. », « Logiciel libre · github.com/lcssrd/Place2b2026 », crédit musique |

Affiche (image 0) : 11,3 s, le trajet de 19 min affiché avec la légende.

## Rendu
Composition `work/comp2.html` (fonction pure du temps), capturée image par image par Playwright, encodée en H.264 (CRF 16) ; mixage `work/mix.py`. Instantanés : `work/snap2.js`.
