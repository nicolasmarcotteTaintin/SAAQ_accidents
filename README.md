# Analyse des accidents de la SAAQ
Ce repository sert à dupliquer les informations et les scripts associés à la demande d'accès à l'information 03.06.33404 auprès de la SAAQ.
Structure actuelle:
- Scripts: Les fichiers python
- Docs: Demandes d'accès à l'information
- Data: Données RAW ou PROCESSED
- Output: Résultats des scripts, images (PNG), etc.

## 1er analyse: Comparaison de la gravité des accidents par type de véhicules
![alt text](https://github.com/nicolasmarcotteTaintin/SAAQ_accidents/blob/main/output/graph_type_vehicule.png)

Explication : La catégorisation des incidents dans le fichier 'accidents_2012-2022.csv' correspond implicitement à une évaluation de leur gravité. Le ratio mortalité/incident grave est ainsi un indicateur de gravité, calculé pour chaque type de véhicule.

Fichiers Associés:
-  output/graph_type_vehicule.png
-  scripts/comparaison_par_type.py
