
# Réception des données sur les produits « champagne » via API et sauvegarde dans un fichier .csv

import requests
import pandas as pd
from io import BytesIO
from PIL import Image
import matplotlib.pyplot as plt

# App ID et App Key
from config import APP_ID, APP_KEY

# API Endpoint
url = "https://api.edamam.com/api/food-database/v2/parser"

# Demande à API(appliquer un filtre "champagne" au requête API)
querystring = {
    "ingr": "champagne",
    "app_id": APP_ID,
    "app_key": APP_KEY
}

response = requests.request("GET", url, params=querystring)
data = response.json()

# Extrayons les informations nécessaires
items = data['hints'][:10]
products = []

for item in items:
    food = item['food']
    product_info = {
        'foodId': food['foodId'],
        'label': food['label'],
        'category': food['category'],
        'foodContentsLabel': food.get('foodContentsLabel', 'N/A'), 
        'image': food.get('image', None) }
    products.append(product_info)

df = pd.DataFrame(products)
df.to_csv("champagne_products.csv", index=False)

valid_images = df.dropna(subset=['image'])
for idx, row in valid_images.iterrows():
    response = requests.get(row['image'])
    img = Image.open(BytesIO(response.content))
    img.save(f"image_{idx}.jpg", "JPEG")
    
df = pd.read_csv("champagne_products.csv", sep=',')
print(df)

for idx, row in valid_images.iterrows():
    response = requests.get(row['image'])
    img = Image.open(BytesIO(response.content))
    plt.imshow(img)
    plt.title(row['label'])
    plt.axis('off')  
    plt.show()

    '''
RGPD
Comment je me conforme au RGPD dans mon projet :
Légalité : j'utilise une API pour collecter des données qui dispose des autorisations nécessaires pour accéder aux données.

Finalité de la restriction : Je collecte des données uniquement à des fins de recherche et d'analyse des produits « champagne ».

Minimisation des données : je collecte uniquement les données nécessaires à mon projet (foodId, label,category, foodContentsLabel, image).

Précision : j'utilise un processus automatisé pour collecter des données 
qui garantissent l'exactitude des données.

Limites de stockage : je stocke les données dans un fichier CSV 
qui peut être facilement supprimé ou modifié selon les besoins.

De plus, je ne stocke pas de données sur des individus spécifiques ni sur leurs données personnelles, 
ce qui minimise le risque de violation de la confidentialité des données.
'''
