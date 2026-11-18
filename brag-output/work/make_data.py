# Données 100 % fictives pour la vidéo (style des modèles Excel de l'application).
import csv
stages = [
 # Typologie, Établissement, Service, Adresse, CP, Ville
 ('SPA','Clinique des Tilleuls','Chirurgie orthopédique','10 rue de Crosne','76000','Rouen'),
 ('SPA','Clinique des Tilleuls','Chirurgie orthopédique','10 rue de Crosne','76000','Rouen'),
 ('SPA','Clinique des Tilleuls','Médecine polyvalente','10 rue de Crosne','76000','Rouen'),
 ('SPA','Hôpital des Érables','Urgences','20 rue de la République','76500','Elbeuf'),
 ('SPA','Hôpital des Érables','Cardiologie','20 rue de la République','76500','Elbeuf'),
 ('SPA','Clinique des Mouettes','Réanimation','40 rue de Paris','76600','Le Havre'),
 ('SPA','Clinique des Mouettes','Pneumologie','40 rue de Paris','76600','Le Havre'),
 ('SPS','Centre de soins de suite Les Hêtres','Rééducation fonctionnelle','15 rue Jean Jaurès','76300','Sotteville-lès-Rouen'),
 ('SPS','Centre de soins de suite Les Hêtres','Soins de suite polyvalents','15 rue Jean Jaurès','76300','Sotteville-lès-Rouen'),
 ('SPS','Centre de santé mentale Les Peupliers','Hôpital de jour','8 rue de la Barre','76200','Dieppe'),
 ('SPS','Centre de dialyse des Ajoncs','Hémodialyse','5 rue Thiers','76400','Fécamp'),
 ('SPS','Centre de dialyse des Ajoncs','Hémodialyse','5 rue Thiers','76400','Fécamp'),
 ('SPR','Cabinet infirmier du Val Fleuri','Soins à domicile','3 rue Victor Hugo','76600','Le Havre'),
 ('SPR','Maison de santé des Saules','Consultations infirmières','9 rue des Victoires','76190','Yvetot'),
 ('SPR','Maison de santé de la Falaise','Éducation thérapeutique','12 place du Marché','76170','Lillebonne'),
 ('SPR','Cabinet infirmier des Quatre-Vents','Soins à domicile','2 rue de la République','76360','Barentin'),
 ('SPR','Cabinet infirmier des Quatre-Vents','Soins à domicile','2 rue de la République','76360','Barentin'),
 ('VDE','EHPAD Les Glycines','Unité de vie protégée','27 rue Carnot','76190','Yvetot'),
 ('VDE','EHPAD Les Glycines','Hébergement permanent','27 rue Carnot','76190','Yvetot'),
 ('VDE',"Centre d'hébergement Le Phare",'Accueil de jour','15 quai du Havre','76000','Rouen'),
 ('VDE',"Foyer d'accueil Les Mésanges",'Foyer de vie','6 rue Pasteur','76210','Bolbec'),
 ('VDE',"Foyer d'accueil Les Mésanges",'Foyer de vie','6 rue Pasteur','76210','Bolbec'),
 ('VDE','EHPAD Les Charmilles','Unité Alzheimer','30 rue de la République','76270','Neufchâtel-en-Bray'),
 ('SPA','Hôpital des Érables','Médecine gériatrique','20 rue de la République','76500','Elbeuf'),
]
with open('data/lieux-de-stage.csv','w',newline='',encoding='utf-8-sig') as f:
    w = csv.writer(f); w.writerow(['Typologie','Établissement','Service','Adresse','CP','Ville']); w.writerows(stages)

def st(d,e,s,v): return '\n'.join([d,e,s,v])
A = st('SPA','Clinique des Tilleuls','Médecine polyvalente','Rouen')
A2 = st('SPA','Hôpital des Érables','Urgences','Elbeuf')
A3 = st('SPA','Clinique des Mouettes','Pneumologie','Le Havre')
S1 = st('SPS','Centre de soins de suite Les Hêtres','Rééducation fonctionnelle','Sotteville-lès-Rouen')
S2 = st('SPS','Centre de santé mentale Les Peupliers','Hôpital de jour','Dieppe')
S3 = st('SPS','Centre de dialyse des Ajoncs','Hémodialyse','Fécamp')
R1 = st('SPR','Cabinet infirmier du Val Fleuri','Soins à domicile','Le Havre')
R2 = st('SPR','Maison de santé des Saules','Consultations infirmières','Yvetot')
R3 = st('SPR','Cabinet infirmier des Quatre-Vents','Soins à domicile','Barentin')
V1 = st('VDE','EHPAD Les Glycines','Unité de vie protégée','Yvetot')
V2 = st('VDE',"Centre d'hébergement Le Phare",'Accueil de jour','Rouen')
V3 = st('VDE',"Foyer d'accueil Les Mésanges",'Foyer de vie','Bolbec')
students = [
 # NOM, Voiture, Adresse 1, Adresse 2, Stage 1, 2A, 2B
 ('MARTIN Alice','oui','4 rue de la République, 76290 Montivilliers','12 rue de la République, 76000 Rouen', A, V1, S1),
 ('BERNARD Lucas','non','4 rue de la République, 76160 Darnétal','', R2, A, ''),
 ('DUBOIS Camille','oui','8 rue Jean Jaurès, 76550 Offranville','12 rue de la République, 76230 Bois-Guillaume', S2, V2, R1),
 ('LEROY Inès','non','4 rue de la République, 76700 Harfleur','', R1, A3, ''),
 ('MOREAU Hugo','oui','10 Grande Rue, 27310 Bourg-Achard','', A2, S1, V2),
 ('PETIT Léa','oui','6 rue du Général de Gaulle, 76450 Cany-Barville','', S3, R2, A),
 ('ROUX Nathan','non','4 rue de la République, 76530 Grand-Couronne','', V2, S1, ''),
 ('FOURNIER Chloé','oui','6 rue du Général de Gaulle, 76560 Doudeville','', V1, A, R3),
 ('GIRARD Adam','oui','4 rue de la République, 76430 Saint-Romain-de-Colbosc','', A3, V3, S3),
 ('BONNET Manon','non','6 rue du Général de Gaulle, 76570 Pavilly','', R3, V1, ''),
 ('LAMBERT Théo','oui','6 rue du Général de Gaulle, 76630 Envermeu','', S2, A2, V3),
 ('FONTAINE Sarah','non','4 rue de la République, 76130 Mont-Saint-Aignan','', A, S1, ''),
 ('ROUSSEAU Jules','oui','4 rue de la République, 76110 Goderville','', R1, V3, A3),
 ('VINCENT Emma','oui','6 rue du Général de Gaulle, 76790 Étretat','', V3, S3, R2),
 ('MULLER Louis','non','4 rue de la République, 76150 Maromme','', S1, V2, A2),
 ('LEFEBVRE Jade','oui','4 rue de la République, 76440 Forges-les-Eaux','', V1, R3, ''),
 ('MERCIER Raphaël','oui','4 rue de la République, 27400 Louviers','', A2, R2, S1),
 ('DUPONT Lina','non','4 rue de la République, 76600 Le Havre','', A3, R1, ''),
 ('BLANC Noah','oui','6 rue du Général de Gaulle, 76750 Buchy','12 rue de la République, 76000 Rouen', R3, S2, V1),
 ('GUERIN Zoé','oui','4 rue de la République, 76460 Saint-Valery-en-Caux','', S3, A3, ''),
 ('BOYER Gabriel','oui','6 rue du Général de Gaulle, 76890 Tôtes','', R2, V1, A),
 ('GARNIER Louise','oui','6 rue du Général de Gaulle, 76480 Duclair','', V2, A, S2),
 ('CHEVALIER Tom','oui','4 rue de la République, 76690 Clères','', A, R3, V2),
 ('FRANÇOIS Lola','oui','4 rue de la République, 27500 Pont-Audemer','', S1, ''  , ''),
]
with open('data/etudiants.csv','w',newline='',encoding='utf-8-sig') as f:
    w = csv.writer(f); w.writerow(['NOM','Voiture','Adresse 1','Adresse 2','Stage 1','Stage 2A','Stage 2B','Stage 3A','Stage 3B'])
    for r in students: w.writerow(list(r)+['',''])
print(len(stages),'places;',len(students),'étudiants')
