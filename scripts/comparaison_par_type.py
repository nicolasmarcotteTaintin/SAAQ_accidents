import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from tqdm import tqdm

# Charger les données des accidents
accidents = pd.read_csv('./data/raw/accidents_2012-2022.csv')

# Définir les années pour lesquelles nous avons les données des véhicules en circulation
years = range(2011, 2023)

# Colonnes à utiliser
cols_to_use_2011_2016 = ["AN", "TYP_VEH_CATEG_USA"]
cols_to_use_2017_onwards = ["AN", "TYP_VEH_CATEG_USA"]

# Fonction pour charger les données par chunks et filtrer les colonnes nécessaires
def load_filtered_data(file, cols_to_use):
    chunk_size = 100000  # Taille des chunks
    chunks = []
    for chunk in pd.read_csv(file, chunksize=chunk_size, usecols=cols_to_use, dtype=str):
        chunks.append(chunk)
    return pd.concat(chunks, ignore_index=True)

# Charger les données des véhicules en circulation pour toutes les années
vehicules = pd.DataFrame()
for year in tqdm(years, desc="Chargement des données des véhicules en circulation"):
    file_path = f'./data/raw/Vehicule_En_Circulation_{year}.csv'
    if year < 2017:
        data = load_filtered_data(file_path, cols_to_use_2011_2016)
    else:
        data = load_filtered_data(file_path, cols_to_use_2017_onwards)
    vehicules = pd.concat([vehicules, data], ignore_index=True)

# Créer une colonne 'Type_de_vehicule' dans les données des accidents pour correspondre aux catégories dans les données des véhicules
def categorize_vehicle(row):
    if row['Type de véhicule'] in ['VUS', 'Fourgonnette']:
        return 'SUV'
    elif row['Type de véhicule'] == 'Automobile':
        return 'Car'
    else:
        return 'Other'

accidents['Type_de_vehicule'] = accidents.apply(categorize_vehicle, axis=1)

# Filtrer les accidents graves
accidents_graves = accidents[accidents['Nature des dommages'] == 'Graves']

# Calculer la proportion de chaque type de véhicule impliqué dans les accidents graves
accidents_count = accidents_graves['Type_de_vehicule'].value_counts(normalize=True)

# Créer une colonne 'Type_de_vehicule' dans les données des véhicules pour correspondre aux catégories dans les données des accidents
def categorize_vehicle_vehicules(row):
    if row['TYP_VEH_CATEG_USA'] in ['MC', 'AU']:  # Catégories ajustées pour correspondre aux types de véhicules
        return 'SUV'
    elif row['TYP_VEH_CATEG_USA'] == 'AU':
        return 'Car'
    else:
        return 'Other'

vehicules['Type_de_vehicule'] = vehicules.apply(categorize_vehicle_vehicules, axis=1)

# Calculer la proportion de chaque type de véhicule en circulation
vehicules_count = vehicules['Type_de_vehicule'].value_counts(normalize=True)

# Comparer les proportions
comparison = pd.DataFrame({
    'Proportion_accidents': accidents_count,
    'Proportion_circulation': vehicules_count
})

# Calculer le ratio de représentation
comparison['Ratio_représentation'] = comparison['Proportion_accidents'] / comparison['Proportion_circulation']

# Afficher les résultats
print(comparison)

# Générer des graphiques
sns.set(style="whitegrid")

# Graphique des proportions des véhicules dans les accidents graves
plt.figure(figsize=(10, 6))
sns.barplot(x=comparison.index, y=comparison['Proportion_accidents'], palette='viridis')
plt.title('Proportion des types de véhicules dans les accidents graves')
plt.ylabel('Proportion')
plt.xlabel('Type de véhicule')
plt.show()

# Graphique des proportions des véhicules en circulation
plt.figure(figsize=(10, 6))
sns.barplot(x=comparison.index, y=comparison['Proportion_circulation'], palette='viridis')
plt.title('Proportion des types de véhicules en circulation')
plt.ylabel('Proportion')
plt.xlabel('Type de véhicule')
plt.show()

# Graphique du ratio de représentation des types de véhicules dans les accidents graves
plt.figure(figsize=(10, 6))
sns.barplot(x=comparison.index, y=comparison['Ratio_représentation'], palette='viridis')
plt.title('Ratio de représentation des types de véhicules dans les accidents graves')
plt.ylabel('Ratio de représentation')
plt.xlabel('Type de véhicule')
plt.axhline(1, color='red', linestyle='--')
plt.show()
