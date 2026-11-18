# Place2b2026 (« The place to be », programme 2026)

**Version 1.0** · Licence [GNU GPL v3](LICENSE) · © 2026 Lucas Seraudie · Dépôt : <https://github.com/lcssrd/Place2b2026>

Place2b2026 sert à placer les étudiants infirmiers en stage selon le **programme de formation 2026** et ses **4 typologies de stage** (SPA, SPS, SPR, VDE). Tout tient dans un seul fichier HTML (`Place2b2026.html`) qui s'ouvre dans le navigateur. Il n'y a rien à installer, ni serveur, ni compte à créer. L'interface adopte un style « Brutalist » : contours francs, ombres dures, aplats de couleur.

> Pour les promotions qui suivent encore l'ancien programme (disciplines SCD, SLD SSR, SP SM, SLV), utilisez [Place2Be](https://github.com/lcssrd/Place2Be), dont Place2b2026 est dérivé. Les deux outils gardent leurs données à part et peuvent être utilisés dans le même navigateur.

L'outil a été pensé pour les formateurs d'IFSI qui répartissent une promotion entre les lieux de stage :

- il **affiche sur une carte** les lieux de stage et les adresses des étudiants ;
- il **calcule le temps de trajet en voiture** entre chaque étudiant et chaque lieu ;
- il **propose un placement automatique** qui réduit au maximum les trajets, en tenant compte de qui a une voiture ;
- il **suit le parcours de stage** de chaque étudiant, typologie par typologie ;
- il **signale les problèmes** dans un tableau de bord : adresses introuvables, doublons, trajets trop longs, typologies qui risquent de manquer avant la fin de la formation ;
- il **exporte** les placements et les parcours en Excel, prêts à imprimer.

---

## Sommaire

1. [Les 4 typologies de stage du programme 2026](#1-les-4-typologies-de-stage-du-programme-2026)
2. [Démarrage rapide](#2-démarrage-rapide)
3. [Ce qu'il faut pour l'utiliser](#3-ce-quil-faut-pour-lutiliser)
4. [Préparer les fichiers Excel](#4-préparer-les-fichiers-excel)
5. [Comment l'outil localise les adresses](#5-comment-loutil-localise-les-adresses)
6. [Comment les temps de trajet sont calculés](#6-comment-les-temps-de-trajet-sont-calculés)
7. [Le placement automatique](#7-le-placement-automatique)
8. [Le placement à la main](#8-le-placement-à-la-main)
9. [Les trois vues : Carte, Parcours, Tableau de bord](#9-les-trois-vues--carte-parcours-tableau-de-bord)
10. [Les périodes de stage](#10-les-périodes-de-stage)
11. [Corriger les adresses](#11-corriger-les-adresses)
12. [Sauvegarde, annulation et reprise du travail](#12-sauvegarde-annulation-et-reprise-du-travail)
13. [Exports Excel](#13-exports-excel)
14. [Réglages](#14-réglages)
15. [Raccourcis clavier](#15-raccourcis-clavier)
16. [Données personnelles et services externes](#16-données-personnelles-et-services-externes)
17. [Limites connues](#17-limites-connues)
18. [Adapter l'outil et contribuer](#18-adapter-loutil-et-contribuer)
19. [Historique des versions](#19-historique-des-versions)
20. [Licence et crédits](#20-licence-et-crédits)

---

## 1. Les 4 typologies de stage du programme 2026

Le programme de formation infirmière 2026 classe les stages en 4 typologies. Place2b2026 les reconnaît et leur attribue une couleur dans toute l'application et dans les exports Excel.

| Sigle | Typologie officielle | Intitulé court | Couleur |
|---|---|---|---|
| **SPA** | Prise en soins d'une altération de l'état de santé en phase aiguë | Soins en phase aiguë / Soins aigus | Jaune |
| **SPS** | Prise en soins d'une altération de l'état de santé stabilisée | Soins stabilisés / Phase stabilisée | Bleu |
| **SPR** | Accompagnement dans le cadre d'une équipe de soins primaires | Soins de premier recours / Soins primaires | Rouge |
| **VDE** | Accompagnement en situation de vulnérabilité, dépendance ou exclusion | Vulnérabilité / Dépendance / Exclusion | Vert |

**Ce que vous pouvez écrire dans vos fichiers.** Le sigle (`SPA`), l'intitulé court (`Soins aigus`, `Soins primaires`…) ou l'intitulé officiel complet sont tous reconnus. Majuscules, accents et ponctuation ne comptent pas. À l'import, la valeur est ramenée à son sigle : c'est lui qui s'affiche dans l'application, et l'intitulé officiel apparaît au survol de la pastille.

**Valeurs non reconnues.** Toute autre valeur est conservée telle quelle et classée dans « Autres » (en gris). C'est le cas des anciennes disciplines (SCD, SLD SSR, SP SM, SLV).

**Partout dans l'application**, les typologies servent à :

- filtrer les places proposées à un étudiant, et les épingles de la carte ;
- repérer les typologies qu'un étudiant n'a pas encore faites ;
- compter les places libres par typologie ;
- alerter quand une typologie risque de manquer avant la fin du cursus.

---

## 2. Démarrage rapide

1. **Téléchargez** [`Place2b2026.html`](Place2b2026.html) (bouton « Download raw file » sur GitHub) et rangez-le dans un dossier de travail.
2. **Ouvrez-le** d'un double-clic dans **Google Chrome** ou **Microsoft Edge**.
3. Cliquez sur **Importer les stages** et choisissez la liste des places de stage (Excel).
4. Cliquez sur **Importer les étudiants** et choisissez la liste des étudiants (Excel, avec leur parcours si vous l'avez).
5. Attendez la fin de la barre de progression : l'outil localise les adresses, puis calcule les trajets.
6. Cliquez sur **Placement automatique**, vérifiez les limites de trajet, puis **Lancer le placement**.
7. Ajustez à la main si besoin, puis faites **Ctrl+S** pour choisir un fichier de sauvegarde `.json`. Ensuite, chaque modification y est enregistrée automatiquement.

> Vous n'avez pas encore de fichiers ? Ouvrez **Réglages** (icône des curseurs, en haut à droite) › **Modèles de fichiers Excel**. Vous y trouverez deux modèles déjà rédigés avec les 4 typologies 2026 et des données fictives, chacun avec une feuille « Mode d'emploi ».

---

## 3. Ce qu'il faut pour l'utiliser

| Besoin | Détail |
|---|---|
| **Navigateur** | Chrome ou Edge (recommandé). Firefox et Safari fonctionnent aussi, mais sans la sauvegarde automatique dans un fichier (voir [§ 12](#12-sauvegarde-annulation-et-reprise-du-travail)). |
| **Connexion internet** | Nécessaire pour le fond de carte, la localisation des adresses et le calcul des trajets. Les bibliothèques (Leaflet, SheetJS) et la police Inter sont intégrées au fichier : l'interface s'ouvre même hors ligne. Seule la police des titres (Space Grotesk) vient de Google Fonts ; hors ligne, Inter la remplace. |
| **Installation** | Aucune. Le fichier peut être copié sur une clé USB, envoyé par e-mail ou déposé sur un serveur web (GitHub Pages, intranet…). |
| **Fichiers acceptés** | `.xlsx`, `.xls`, `.ods` et `.csv` pour les imports, `.json` pour les sauvegardes. |

---

## 4. Préparer les fichiers Excel

Règles communes à tous les imports :

- **Seule la première feuille** du classeur est lue.
- La **ligne d'en-têtes** peut se trouver dans les 15 premières lignes : l'outil la repère seul. L'ordre des colonnes n'a pas d'importance, mais gardez les intitulés indiqués.
- Majuscules, accents et ponctuation des en-têtes ne comptent pas (`Établissement`, `ETABLISSEMENT` et `etablissement` sont équivalents).
- Un **« ! » en début de cellule** (fréquent dans les exports de certains logiciels d'IFSI) est retiré à l'affichage.
- Vous pouvez aussi **glisser-déposer** un fichier n'importe où sur la page. L'outil devine s'il s'agit d'étudiants (colonnes « Nom » et « Adresse ») ou de stages. Un `.json` est ouvert comme une sauvegarde.

### 4.1 Liste des stages (« Importer les stages »)

**Une ligne = une place.** Un service qui accueille deux étudiants s'écrit sur deux lignes identiques.

| Colonne | Intitulés reconnus | Obligatoire | Contenu |
|---|---|---|---|
| Établissement | `Établissement`, `Structure` | **Oui** | Nom du lieu de stage. Il sert à regrouper les places sur une même épingle. |
| Typologie | `Typologie`, ou `Discipline` (anciens fichiers) | Conseillée | `SPA`, `SPS`, `SPR` ou `VDE`, ou leur intitulé ([§ 1](#1-les-4-typologies-de-stage-du-programme-2026)). |
| Service | `Service…`, `Unité` | Conseillée | Service ou unité d'accueil. |
| Adresse | `Adresse…` | Facultative, mais conseillée | Numéro et rue. Elle donne une position exacte et passe avant toute autre source. |
| CP | `CP`, `C.P.`, `Code postal` | Conseillée | Un code à 4 chiffres est complété par un 0 (`7600` → `07600`). |
| Ville | `Ville`, `Commune` | Conseillée | Commune du lieu de stage. |

Si aucune ligne d'en-têtes n'est trouvée, les colonnes sont lues dans cet ordre : Typologie, Service, CP, Ville, Établissement.

**Réimporter une liste** remplace la précédente. Les placements des places identiques (même typologie, service, CP, ville et établissement) sont conservés.

### 4.2 Liste des étudiants et parcours (« Importer les étudiants »)

**Une ligne = un étudiant.**

| Colonne | Intitulés reconnus | Obligatoire | Contenu |
|---|---|---|---|
| Nom | `NOM`, `Nom…`, `Étudiant` | **Oui** | Nom et prénom. Une colonne `Prénom` séparée est aussi acceptée. |
| Adresse 1 | `Adresse 1`, `Adresse`, `Adresse principale` | **Oui** | Adresse complète (rue, code postal, ville). Elle sert au calcul des trajets. |
| Adresse 2 | `Adresse 2`, `Adresse secondaire` | Non | Deuxième point de départ possible (logement de stage, famille…). Le trajet le plus court des deux est retenu. |
| Voiture | `Voiture`, `Véhicule` | Non | `oui`, `o`, `yes`, `x`, `1`, `vrai`, `ok`… Toute autre valeur veut dire « non ». |
| Parcours | `Stage 1`, `Stage 2A`, `Stage 2B`… `Rattrapage…`, `Ratt…` | Non | Une colonne par période de stage, dans l'ordre chronologique. |

**Remplir une cellule de parcours.** Passez à la ligne dans la cellule avec **Alt+Entrée** :

```
06/07/2026 au 02/08/2026     ← facultatif : une ligne de dates
SPS                          ← la typologie (sigle ou intitulé)
Centre de soins de suite     ← l'établissement
Rééducation fonctionnelle    ← le service (une ou plusieurs lignes)
Elbeuf                       ← la ville, sur la dernière ligne
```

La ligne de typologie n'est reconnue que si elle contient exactement un sigle ou un intitulé de la [§ 1](#1-les-4-typologies-de-stage-du-programme-2026). Ainsi, un établissement nommé « EHPAD Dépendance » n'est pas pris pour une typologie. Laissez la cellule vide pour un stage pas encore fait.

**Réimporter la liste** remplace la précédente. Pour chaque étudiant retrouvé sous le même nom, son placement est conservé, et sa localisation aussi si l'adresse n'a pas changé. Si le nouveau fichier n'a pas de colonnes de parcours, le parcours déjà chargé est gardé.

### 4.3 Liste d'adresses des lieux de stage (facultative)

C'est un répertoire des établissements de votre secteur (`Établissement`, `Adresse`, `CP`, `Ville`). L'outil y cherche l'adresse des lieux dont la liste des stages ne donne pas d'adresse. Importez-la dans **Réglages › Liste d'adresses des lieux de stage › Mettre à jour**. Elle est gardée dans votre sauvegarde.

> Place2b2026 **n'intègre aucune liste d'adresses** : chaque utilisateur importe la sienne. Sans liste, les lieux sont cherchés par leur nom, puis par leur commune ([§ 5](#5-comment-loutil-localise-les-adresses)).

### 4.4 Modèles téléchargeables

**Réglages › Modèles de fichiers Excel** propose deux modèles :

- `modele-lieux-de-stage.xlsx` : la liste des stages, avec les colonnes Typologie et Adresse ;
- `modele-etudiants.xlsx` : les étudiants et leur parcours.

Les deux modèles utilisent les 4 typologies 2026, sur des données fictives. Chacun contient une feuille « Mode d'emploi ». Remplacez les lignes d'exemple par vos données.

---

## 5. Comment l'outil localise les adresses

Pour chaque adresse, l'outil cherche une position (latitude, longitude). Une barre de progression s'affiche en bas de la carte pendant ce temps.

### Les étudiants

L'adresse est envoyée à la **Géoplateforme de l'IGN**. Si elle ne répond pas, l'outil se rabat sur la **Base adresse nationale** (`api-adresse.data.gouv.fr`). Le résultat est marqué **« Position approximative »** quand la correspondance est faible ou que seule la commune a été reconnue.

### Les lieux de stage

L'outil essaie ces sources dans l'ordre et garde la première qui donne une position :

1. **L'adresse saisie à la main** dans la fiche du lieu ([§ 11](#11-corriger-les-adresses)). Elle est retenue pour cet établissement lors des imports suivants.
2. **L'adresse de la colonne « Adresse »** de la liste des stages.
3. **La liste d'adresses importée** dans les Réglages, en cherchant l'établissement :
   - d'abord sous le même nom ;
   - puis sous un nom tronqué (les exports Excel coupent parfois les noms longs) ;
   - enfin d'après les mots en commun, au même code postal ou dans la même ville. Les mots rares pèsent plus lourd que les mots courants, et les abréviations sont comprises (« CH » = « Centre hospitalier », « St » = « Saint »…).
4. **Le nom de l'établissement**, cherché parmi les lieux connus de l'IGN, puis dans **OpenStreetMap** (Nominatim). Seul un résultat à moins de 12 km de la commune est accepté.
5. **Le centre de la commune**, en dernier recours. L'épingle est alors pâle, contour en pointillés, et marquée « Position approximative ».

Si l'adresse trouvée dans la liste d'adresses est dans une autre ville que celle de la liste des stages, l'outil le signale : il s'agit peut-être d'une antenne de l'établissement.

Vous pouvez toujours **placer une épingle à la main** : vous cliquez sur la carte, et cette position passe avant tout le reste.

---

## 6. Comment les temps de trajet sont calculés

- Les trajets sont calculés **en voiture**, avec le service de calcul d'itinéraire public **OSRM** (`router.project-osrm.org`), qui s'appuie sur les routes d'OpenStreetMap. Le trafic n'est pas pris en compte.
- Pour chaque étudiant et chaque lieu, l'outil calcule le trajet depuis l'adresse 1 et depuis l'adresse 2, puis **garde le plus court**. La fiche indique de quelle adresse il part.
- Les calculs sont regroupés par paquets (25 adresses de départ × 75 lieux par requête) et retentés jusqu'à 3 fois.
- **Si le service ne répond pas**, le temps est **estimé** : distance à vol d'oiseau × 1,3, à 50 km/h, plus 3 minutes. Un temps estimé est précédé de « ≈ ». Pour relancer le calcul exact plus tard : **Réglages › Recalculer les trajets estimés**.
- Les temps déjà calculés sont gardés dans la sauvegarde : ils ne sont pas recalculés à chaque ouverture.

**Couleur des temps** (selon les limites des Réglages) :

| Couleur | Signification |
|---|---|
| Vert | Dans la limite de l'étudiant. |
| Orange | Étudiant sans voiture : au-delà de sa limite, mais dans la limite « avec voiture ». |
| Rouge | Au-delà de la limite. |

Chaque trajet a un bouton **Itinéraire**, qui ouvre le trajet en voiture dans Google Maps pour vérifier.

---

## 7. Le placement automatique

Le bouton **Placement automatique** ouvre une fenêtre où vous réglez :

- **Avec voiture · trajet maximum** : 35 minutes par défaut ;
- **Sans voiture · stage considéré comme « proche »** : 20 minutes par défaut ;
- **Conserver les placements manuels** : coché par défaut. Les places marquées d'un cadenas ne bougent pas.

### Ce que fait l'algorithme

1. Il met de côté :
   - les placements manuels (si l'option est cochée) ;
   - les étudiants qui ont **déjà un stage renseigné dans leur parcours** pour la période en cours.
2. Il construit un tableau « étudiants × places libres ». Le coût d'un couple vaut **t² + t**, où t est le temps de trajet en minutes. Un trajet au-delà de la limite de l'étudiant est interdit.
3. Il résout ce tableau avec l'**algorithme hongrois**, qui trouve la répartition optimale (et non une suite de choix « au plus proche »). Grâce au carré, deux trajets de 25 minutes valent mieux qu'un de 10 et un de 40 : l'outil préfère des trajets raisonnables pour tous à un excellent trajet pour quelques-uns.
4. Il place le plus d'étudiants possible. Les lieux éloignés reviennent naturellement aux étudiants qui ont une voiture, puisqu'eux seuls peuvent y aller.

Le placement automatique ne tient compte **que des trajets**, pas des typologies. Pour orienter un étudiant vers une typologie qu'il n'a pas encore faite, placez-le à la main ([§ 8](#8-le-placement-à-la-main)) et verrouillez sa place avant de lancer le placement automatique pour les autres.

### Le résultat

Une fenêtre résume le nombre d'étudiants placés, le trajet moyen et le trajet le plus long. Elle donne aussi la raison de chaque étudiant non placé :

- *Adresse introuvable* ;
- *Aucun stage à moins de X min* (avec ou sans voiture) ;
- *Plus aucune place libre* ;
- *Places proches déjà attribuées*.

Un bouton **Annuler** dans la notification remet les placements d'avant.

Les placements automatiques ont un cadenas ouvert : un nouveau placement automatique peut les changer. Cliquez sur le cadenas pour en verrouiller un.

---

## 8. Le placement à la main

Il y a trois façons de placer un étudiant :

1. **Depuis la fiche de l'étudiant** (cliquez sur son nom). La section « Places libres les plus proches » liste les 15 places libres les plus proches, triées par temps de trajet. Les filtres par typologie aident à choisir :
   - « Pas encore faites » ne garde que les typologies absentes de son parcours ;
   - un point jaune signale une typologie qu'il n'a pas encore faite.

   Ces filtres s'appliquent aussi aux épingles de la carte.
2. **Depuis la carte**. Sélectionnez un étudiant, puis cliquez sur une épingle : une fenêtre montre le trajet et les places du lieu, chacune avec un bouton **Placer**.
3. **Depuis la fiche du lieu**. Pour chaque place libre, « Choisir un étudiant… » liste les étudiants non placés, du plus proche au plus éloigné, avec leurs derniers stages en couleur. Les trajets hors limite sont signalés.

Un placement fait à la main est **verrouillé** (cadenas fermé). Si la place est déjà prise, l'outil demande confirmation avant de remplacer l'étudiant. **Retirer** libère la place.

Survoler un étudiant ou une place dans les listes trace le trajet sur la carte.

---

## 9. Les trois vues : Carte, Parcours, Tableau de bord

### 9.1 Carte

**Colonne de gauche**

- **Stage en cours de placement** : choix de la période ([§ 10](#10-les-périodes-de-stage)), avec les boutons **Enregistrer dans le parcours** et **Purger la liste**.
- **Chiffres clés** : étudiants placés, places libres, trajet moyen.
- **Onglets Étudiants / Stages**, avec une recherche (touche `/`) et deux filtres :
  - Étudiants : tous, non placés, placés, adresse à vérifier ; avec ou sans voiture.
  - Stages : tous, places libres, complets, position à vérifier, sans adresse précise ; par typologie.

  Les filtres s'appliquent aussi à la carte.
- **Bandeau d'alerte** quand des adresses sont à corriger ([§ 11](#11-corriger-les-adresses)).
- **Fiche détaillée** de l'étudiant ou du lieu sélectionné.

**Sur la carte**

| Symbole | Signification |
|---|---|
| Épingle rouge | Lieu de stage. Le chiffre indique le nombre de places libres. |
| Épingle rose avec ✓ | Lieu complet. |
| Épingle pâle, contour en pointillés | Position approximative (centre de la commune). |
| Point bleu foncé / bleu clair | Adresse 1 / adresse 2 d'un étudiant. |
| Point vert | Étudiant placé. |
| Pointillés | Liaison étudiant ↔ lieu de stage (calque « Liaisons »). |

La légende en bas à gauche permet d'afficher ou de masquer chaque calque. Le fond de carte est le **Plan IGN**. S'il ne charge pas, l'outil bascule sur un fond Esri.

### 9.2 Parcours

C'est un tableau avec une ligne par étudiant et une colonne par période de stage. Chaque stage y apparaît comme une carte colorée selon sa typologie.

- **« Prévu »** : le placement de la période en cours, pas encore enregistré dans le parcours.
- **« À placer »** : l'étudiant n'a pas encore de stage pour la période en cours.
- **« Enregistré »** : le stage a été inscrit depuis l'application ([§ 10](#10-les-périodes-de-stage)).
- Sous chaque nom, les 4 typologies (SPA, SPS, SPR, VDE) s'affichent en couleur quand elles sont faites, en gris quand elles restent à faire.

Ce que vous pouvez y faire :

- **Cliquer sur une carte** pour modifier le stage (typologie, dates, établissement, service, ville), ou sur **+ Ajouter** dans une case vide. La liste des typologies du formulaire propose les 4 sigles avec leur intitulé court.
- **Glisser une carte** dans une autre colonne du même étudiant, pour corriger une période. Les deux stages s'échangent si la case était occupée.
- **Ajouter une colonne de rattrapage** avec le **+** d'un en-tête. Le **×** supprime une colonne de rattrapage vide.
- **Filtrer** : recherche, typologie « pas encore faite », placés ou non placés, avec ou sans voiture.
- **Ajouter, modifier ou supprimer un étudiant**. Ces changements valent aussi pour la liste des étudiants à placer.
- **Exporter en Excel** un tableau en couleurs, prêt à imprimer ([§ 13](#13-exports-excel)).

### 9.3 Tableau de bord

C'est l'état de la promotion pour la période en cours. Le nombre d'alertes s'affiche sur l'onglet.

- **Chiffres clés** : étudiants placés, places libres, non placés, trajets au-delà de la limite, typologies qui vont manquer, alertes.
- **Alertes**, de la plus grave à la moins grave :

  | Niveau | Alerte |
  |---|---|
  | À corriger | Adresses d'étudiants introuvables |
  | À corriger | Étudiants sans adresse |
  | À corriger | Lieux de stage sans coordonnées |
  | À corriger | Noms d'étudiants en double |
  | À vérifier | Établissements en double (même nom, code postal ou ville écrits différemment) |
  | À vérifier | Étudiants localisés approximativement |
  | À vérifier | Positions de lieux de stage à vérifier |

  Chaque alerte donne la liste des éléments concernés, cliquables, et un raccourci **Corriger sur la carte**.
- **Places restantes par typologie** : places, pourvues, libres et taux de remplissage pour SPA, SPS, SPR et VDE. La colonne « À faire » compte les étudiants non placés qui n'ont pas encore fait la typologie.
- **Étudiants non placés**, les plus difficiles à placer en premier : nombre de lieux possibles dans la limite, trajet le plus proche et typologies manquantes.
- **Trajets au-delà de la limite** : les étudiants placés trop loin, avec le dépassement en minutes.
- **Typologies qui manqueront en fin de cursus** : pour chaque étudiant, les typologies pas encore faites, comparées au nombre de stages restants (hors rattrapages, en comptant le placement en cours). L'étudiant est marqué « Manquera N typologies » s'il n'a plus assez de stages, « Aucune marge » s'il n'en a plus aucun de trop.
- **Places restantes par lieu** : les places libres de chaque lieu, par typologie.

---

## 10. Les périodes de stage

En haut de la colonne de gauche, **Stage en cours de placement** indique la période que vous préparez (Stage 1, Stage 2A…).

- La liste des périodes reprend les colonnes de parcours de votre fichier d'étudiants : nommez-les comme dans votre planning de formation. Sans parcours importé, une liste par défaut est proposée (Stage 1, 2A, 2B, 3A, 4, 5A, 5B, 6A, 6B).
- À l'import du parcours, l'outil **devine la période en cours** : c'est la première colonne vide (hors rattrapages) pour la majorité des étudiants.
- **Chaque période garde sa propre liste de stages et ses propres placements.** Changer de période range ceux de la période quittée et recharge ceux de la nouvelle.
- **Enregistrer dans le parcours** inscrit les placements de la période dans la colonne correspondante du parcours (stages marqués « Enregistré ») et sauvegarde. L'outil propose ensuite de passer à la période suivante, dont la liste de stages repart à zéro. Une période enregistrée est marquée ✓ dans la liste.
- **Purger la liste** vide les places et les placements de la période affichée. Le parcours et les autres périodes ne sont pas touchés, et l'opération peut être annulée.

---

## 11. Corriger les adresses

Quand des adresses posent problème, un bandeau apparaît au-dessus de la liste. Par exemple : « 2 adresses d'étudiants introuvables · 3 positions approximatives ». Cliquez sur **Corriger** pour ouvrir la liste. Pour chaque élément :

- **Placer** : cliquez ensuite sur la carte à l'endroit exact ;
- **✎ (corriger)** : saisissez l'adresse corrigée. Elle est relocalisée aussitôt ;
- **Ignorer** : l'élément ne compte plus dans les alertes. Il reste rétablissable en bas de la liste ;
- **Plus de détails** : affiche l'adresse retenue, sa source et la cause du problème.

**Tout placer à la suite** enchaîne les éléments un par un sur la carte (bouton « Passer » pour sauter un élément, Échap pour arrêter).

Dans la **fiche d'un lieu**, vous pouvez aussi :

- **Modifier l'adresse** : elle sera retenue pour cet établissement à chaque import ;
- **Placer sur la carte** : positionner l'épingle à la main.

Dans la **fiche d'un étudiant**, le bouton ⌖ à côté de chaque adresse repositionne le point à la main. **Modifier la fiche** change le nom, les adresses ou la voiture.

---

## 12. Sauvegarde, annulation et reprise du travail

### Où sont les données ?

Toutes les données restent **sur votre ordinateur** :

1. **Une copie automatique dans le navigateur.** Vous retrouvez votre travail en rouvrant le fichier dans le même navigateur, sur le même poste. Cette copie est propre à Place2b2026 : elle ne se mélange pas avec celle de Place2Be.
2. **Un fichier de sauvegarde `.json`**, à garder à côté de l'application (nom proposé : `placements-stages-2026.json`) :
   - **Avec Chrome ou Edge** : la première fois, **Ctrl+S** (ou l'icône disquette) vous fait choisir l'emplacement du fichier. Ensuite, **chaque modification y est écrite automatiquement**. À la réouverture, l'outil se souvient du fichier : cliquez sur « Reprendre … » ou sur l'indicateur sous le titre pour le reconnecter. Le navigateur demande alors votre accord.
   - **Avec Firefox ou Safari** : Ctrl+S télécharge le fichier `.json`. Pensez à enregistrer régulièrement.

L'indicateur sous le titre donne l'état de la sauvegarde : « Enregistré · nom du fichier », « Enregistrement… », « Non enregistré dans un fichier » ou « Reconnecter … ».

### Rouvrir une sauvegarde

Utilisez l'icône dossier (Ouvrir une sauvegarde), le lien « Ouvrir le fichier .json » de l'écran d'accueil, ou glissez le fichier `.json` sur la page. Le fichier de sauvegarde se partage facilement avec un collègue.

Une sauvegarde de Place2Be (ancien programme) peut être ouverte, mais ses disciplines (SCD, SLD SSR…) apparaîtront dans « Autres ». Pour ces promotions, continuez avec Place2Be.

### Annuler / rétablir

- **Ctrl+Z** annule la dernière modification, **Ctrl+Y** (ou Ctrl+Maj+Z) la rétablit, jusqu'à 60 étapes.
- La plupart des actions affichent aussi une notification avec un bouton **Annuler**.

### Repartir de zéro

**Réglages › Nouvelle session** efface les données de la page. Le fichier de sauvegarde existant n'est pas modifié.

### Contenu du fichier `.json`

C'est un objet JSON lisible qui contient :

- les places de stage (`stages`, avec leur typologie dans `disc`) et les étudiants (`students`, avec adresses, voiture et parcours) ;
- les lieux localisés (`locations`) et les temps de trajet calculés (`times`) ;
- les placements (`assign`) et les verrous (`locks`) ;
- les réglages (`settings`) et les périodes (`period`, `periods`, `parcoursCols`) ;
- vos corrections d'adresses (`refEdits`), la liste d'adresses importée (`refCustom`) et les éléments ignorés (`ignored`).

---

## 13. Exports Excel

| Export | Où | Contenu |
|---|---|---|
| **Placements** `placements-<période>.xlsx` | Icône téléchargement, barre du haut | Feuille **Par stage** : typologie, service, CP, ville, établissement, étudiant, voiture, temps, distance, adresse de départ, placement manuel ou automatique. Feuille **Par étudiant** : la même chose, triée par nom. |
| **Parcours** `parcours-stages-<date>.xlsx` | Vue Parcours › Exporter en Excel | Tableau en couleurs par typologie, avec légende SPA / SPS / SPR / VDE, stages « Prévu » et « À placer » et colonne « Typologies manquantes ». Mise en page prête à imprimer : paysage, une page en largeur, noms et en-têtes répétés sur chaque page, volets figés, filtres, pied de page. |
| **Modèles** | Réglages › Modèles de fichiers Excel | Liste des stages et liste des étudiants avec les typologies 2026, exemples fictifs et mode d'emploi. |

---

## 14. Réglages

Ouvrez les Réglages avec l'icône des curseurs, en haut à droite.

| Réglage | Rôle |
|---|---|
| **Avec voiture · trajet maximum** | Limite de trajet des étudiants véhiculés (35 min par défaut, de 5 à 180). |
| **Sans voiture · stage « proche »** | Limite de trajet des étudiants sans voiture (20 min par défaut). |
| **Liste d'adresses des lieux de stage** | Importer (« Mettre à jour ») ou retirer une liste d'adresses ([§ 4.3](#43-liste-dadresses-des-lieux-de-stage-facultative)). |
| **Modèles de fichiers Excel** | Télécharger les modèles. |
| **Recalculer les trajets estimés** | Relancer le calcul des temps marqués « ≈ » et des adresses introuvables. |
| **Vider les placements** | Retirer tous les placements de la période, en gardant les listes. |
| **Nouvelle session** | Tout effacer de la page. |

Le bas de la fenêtre rappelle la version, l'auteur et la licence.

---

## 15. Raccourcis clavier

| Touche | Action |
|---|---|
| `/` | Aller à la recherche (vues Carte et Parcours). |
| `Échap` | Fermer la fiche ouverte, annuler un placement d'épingle ou fermer une liste. |
| `Ctrl+Z` | Annuler. |
| `Ctrl+Y` ou `Ctrl+Maj+Z` | Rétablir. |
| `Ctrl+S` | Enregistrer. |
| `Entrée` / `Espace` | Modifier la carte de stage sélectionnée (vue Parcours). |

---

## 16. Données personnelles et services externes

Place2b2026 n'a **pas de serveur** : les noms des étudiants, leurs parcours et vos placements ne quittent pas votre ordinateur. Ils restent dans le navigateur et dans votre fichier `.json`.

Pour fonctionner, l'outil fait tout de même appel à des services en ligne :

| Service | Ce qui lui est envoyé | Pourquoi |
|---|---|---|
| Géoplateforme IGN (`data.geopf.fr`) | Adresses des étudiants, noms et communes des lieux de stage | Localisation des adresses, fond de carte |
| Base adresse nationale (`api-adresse.data.gouv.fr`) | Adresses, si l'IGN ne répond pas | Localisation (secours) |
| OpenStreetMap Nominatim (`nominatim.openstreetmap.org`) | Nom, code postal et ville des **établissements** | Localisation des lieux introuvables à l'IGN |
| OSRM (`router.project-osrm.org`) | Coordonnées GPS (sans nom) | Temps et distances en voiture |
| Esri (`server.arcgisonline.com`) | Zone de carte affichée | Fond de carte, si l'IGN ne répond pas |
| Google Fonts (`fonts.googleapis.com`) | Rien de plus que la requête du navigateur (adresse IP) | Police des titres Space Grotesk |
| Google Maps | Adresse de départ et lieu de stage | Seulement si vous cliquez sur « Itinéraire » |

**Les noms des étudiants ne sont jamais envoyés.** Les adresses personnelles, en revanche, passent par les services de localisation. Assurez-vous que cet usage respecte les règles de votre établissement et le RGPD : information des étudiants, durée de conservation du fichier `.json`, etc.

---

## 17. Limites connues

- **Programme 2026 uniquement.** Les anciennes disciplines (SCD, SLD SSR, SP SM, SLV) sont classées dans « Autres » : pour les promotions de l'ancien programme, utilisez [Place2Be](https://github.com/lcssrd/Place2Be).
- **Le placement automatique ne choisit pas la typologie** : il ne regarde que les trajets ([§ 7](#7-le-placement-automatique)).
- **Trajets en voiture uniquement.** Les transports en commun ne sont pas calculés : la limite « sans voiture » est une approximation de la proximité.
- **Service OSRM de démonstration.** Il est gratuit mais sans garantie de disponibilité. En cas de panne, les temps sont estimés (« ≈ ») et peuvent être recalculés plus tard.
- **Nominatim** limite le nombre de requêtes à une par seconde : l'outil en tient compte, mais la recherche des établissements introuvables peut être lente.
- **France uniquement** pour la localisation des adresses (IGN et Base adresse nationale).
- La carte s'ouvre **centrée sur Rouen** ; elle se recadre automatiquement dès que des données sont chargées.
- Deux étudiants portant exactement le même nom sont signalés comme doublon possible.
- La sauvegarde automatique dans un fichier n'existe que sous **Chrome et Edge**.

---

## 18. Adapter l'outil et contribuer

Tout le code se trouve dans `Place2b2026.html`, organisé ainsi :

1. **Bibliothèques intégrées** (en haut du fichier) : la police Inter, Leaflet 1.9.4 pour la carte, xlsx-js-style 1.2.0 (SheetJS) pour Excel. Elles sont intégrées pour que l'outil marche sans CDN.
2. **Styles** (CSS) : une base avec les couleurs définies en variables dans `:root`, puis la surcouche « Brutalist » (`<style id="theme-brutalist">`), qui ne change que l'apparence, et les styles du tableau de bord. Les couleurs des typologies sont portées par les classes `d-spa`, `d-sps`, `d-spr`, `d-vde` (pastilles) et `c-spa`… (cartes du parcours).
3. **Interface** (HTML) : barre du haut, colonne, carte, vues Parcours et Tableau de bord, fenêtres de dialogue.
4. **`REF_DATA`** : liste d'adresses intégrée, vide. Elle a le format `[["Établissement", "Adresse", "CP", "Ville"], …]`. Si vous la remplissez, changez aussi `REF_BUILTIN_STAMP` pour que les sauvegardes existantes en tiennent compte.
5. **Application** (JavaScript, sans dépendance supplémentaire).

**Les typologies dans le code :**

| Élément | Rôle |
|---|---|
| `DISC_ALIAS` | Sigles et intitulés reconnus pour chaque typologie (sans accents, en minuscules). |
| `DISC_NAMES` | Intitulés officiels, affichés au survol des pastilles. |
| `DISC_SIGLE`, `DISC_KEYS` | Sigle affiché et ordre des typologies (SPA, SPS, SPR, VDE). |
| `discKey()`, `discClass()`, `discNorm()` | Reconnaissance d'une valeur, classe de couleur, conversion en sigle à l'import. |
| `DISC_XLS` | Couleurs des typologies dans les exports Excel. |

**Autres réglages faciles à modifier :**

| Élément | Où |
|---|---|
| Limites de trajet par défaut | `DEFAULT_SETTINGS` |
| Centre et zoom de départ de la carte | `L.map('map', …).setView([49.44, 1.09], 10)` |
| Périodes par défaut | `DEFAULT_PERIODS` |
| Version affichée | `APP_VERSION` et le commentaire d'en-tête |

**Publier une nouvelle version :**

1. Changez `APP_VERSION` et le numéro dans le commentaire d'en-tête.
2. Ajoutez une entrée dans l'[historique des versions](#19-historique-des-versions).
3. Créez un tag git `vX.Y`.

**Contribuer :** signalez un problème ou proposez une amélioration dans les *Issues* du dépôt, ou ouvrez une *Pull Request*. Toute contribution est publiée sous la même licence (GPL v3).

---

## 19. Historique des versions

### 1.0 — 18 novembre 2026

Première version, adaptée au programme de formation infirmière 2026. Elle est dérivée de Place2Be 1.0.

- Les 4 typologies de stage du programme 2026 (SPA, SPS, SPR, VDE) remplacent les anciennes disciplines, partout dans l'application :
  - import : sigle, intitulé court ou intitulé officiel reconnus et ramenés au sigle ; en-tête « Typologie » ou « Discipline » accepté ;
  - filtres, fiche étudiant, formulaire de stage, vue Parcours, tableau de bord ;
  - exports Excel et modèles téléchargeables.
- Intitulé officiel de chaque typologie affiché au survol.
- Données du navigateur et fichier de sauvegarde (`placements-stages-2026.json`) séparés de Place2Be.
- Toutes les fonctions de Place2Be 1.0 : carte, localisation des adresses, trajets en voiture, placement automatique optimal et à la main, parcours, périodes, tableau de bord, sauvegarde, annuler / rétablir.

---

## 20. Licence et crédits

**Place2b2026** — © 2026 **Lucas Seraudie** — dérivé de [Place2Be](https://github.com/lcssrd/Place2Be), du même auteur.

Ce programme est un logiciel libre : vous pouvez le redistribuer et le modifier selon les termes de la **Licence publique générale GNU, version 3** ou (à votre choix) toute version ultérieure, publiée par la Free Software Foundation. Le texte complet est dans le fichier [LICENSE](LICENSE).

Concrètement, vous pouvez utiliser, copier, modifier et redistribuer Place2b2026, y compris dans votre établissement, à condition :

- de **garder le nom de l'auteur, la mention de copyright et la licence**, dans le fichier comme dans l'application (crédit des Réglages et du bas de la carte) ;
- de **publier sous la même licence GPL v3** toute version modifiée que vous redistribuez, avec son code source ;
- d'**indiquer vos modifications**.

Le programme est fourni **sans aucune garantie**.

**Bibliothèques intégrées**, chacune sous sa propre licence :

| Bibliothèque | Licence |
|---|---|
| [Leaflet](https://leafletjs.com) 1.9.4 | BSD-2-Clause |
| [xlsx-js-style](https://github.com/gitbrent/xlsx-js-style) 1.2.0, basée sur [SheetJS](https://sheetjs.com) | Apache-2.0 |
| [Inter](https://rsms.me/inter/) | SIL Open Font License 1.1 |
| [Space Grotesk](https://fonts.google.com/specimen/Space+Grotesk) (chargée depuis Google Fonts) | SIL Open Font License 1.1 |

**Données et services :** fond de carte et géocodage © IGN – Géoplateforme · Base adresse nationale · © les contributeurs d'OpenStreetMap (Nominatim, OSRM) · Esri.
