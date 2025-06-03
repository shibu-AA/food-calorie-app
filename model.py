# 以下を「model.py」に書き込み
import torch
import torch.nn as nn
import torch.nn.functional as F
from torchvision import models, transforms
from PIL import Image

import sqlite3

def get_calorie_from_db(food_name: str, db_path="Food101_Calorie.db") -> int:
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    cursor.execute("SELECT Calorie FROM Calorietable WHERE name=?", (food_name,))
    result = cursor.fetchone()
    conn.close()
    return result[0] if result else None


food_101_classes = [
    "apple_pie", "baby_back_ribs", "baklava", "beef_carpaccio", "beef_tartare", "beet_salad",
    "beignets", "bibimbap", "bread_pudding", "breakfast_burrito", "bruschetta", "caesar_salad",
    "cannoli", "caprese_salad", "carrot_cake", "ceviche", "cheese_plate", "cheesecake",
    "chicken_curry", "chicken_quesadilla", "chicken_wings", "chocolate_cake", "chocolate_mousse", "churros",
    "clam_chowder", "club_sandwich", "creme_brulee", "croque_madame", "cup_cakes", "crab_cakes", "deviled_eggs",
    "donuts", "dumplings", "edamame", "eggs_benedict", "escargots", "falafel", "filet_mignon",
    "fish_and_chips", "foie_gras", "french_fries", "french_onion_soup", "french_toast",
    "fried_calamari", "fried_rice", "frozen_yogurt", "garlic_bread", "gnocchi",
    "grilled_cheese_sandwich", "grilled_salmon", "greek_salad", "guacamole", "gyoza", "hamburger",
    "hot_and_sour_soup", "hot_dog", "huevos_rancheros", "hummus", "ice_cream", "lasagna",
    "lobster_bisque", "lobster_roll_sandwich", "macaroni_and_cheese", "macarons", "miso_soup",
    "mussels", "nachos", "omelette", "onion_rings", "oysters", "pad_thai", "paella", "pancakes",
    "panna_cotta", "peking_duck", "pho", "pizza", "pork_chop", "poutine", "prime_rib",
    "pulled_pork_sandwich", "ramen", "ravioli", "red_velvet_cake", "risotto", "samosa",
    "sashimi", "scallops", "seaweed_salad", "shrimp_and_grits", "spaghetti_bolognese",
    "spaghetti_carbonara", "spring_rolls", "steak", "strawberry_shortcake", "sushi", "tacos",
    "takoyaki", "tiramisu", "tuna_tartare", "waffles"
]


n_class = len(food_101_classes)
img_size = 224

from torchvision.models import resnet18

# モデル構築
def load_model(weight_path="model_food101.pth", device="cpu"):
    net = models.resnet18(pretrained=True)
    net.fc = nn.Linear(net.fc.in_features, n_class)
    net.load_state_dict(torch.load(weight_path, map_location=torch.device(device)))
    net = net.to(device)
    net.eval()
    return net

# 推論関数
def predict(img: Image.Image, net, device="cpu"):
    if img.mode != "RGB":  #入力画像がRGBAのとき
        img = img.convert("RGB")
    transform = transforms.Compose([
        transforms.Resize((img_size, img_size)),
        transforms.ToTensor(),
        transforms.Normalize(mean=[0.485, 0.456, 0.406],
                             std=[0.229, 0.224, 0.225])
    ])

    x = transform(img).unsqueeze(0).to(device)  # shape: [1, 3, 224, 224]

    with torch.no_grad():
        y = net(x)
        y_prob = torch.softmax(y[0], dim=0)

    sorted_prob, sorted_indices = torch.sort(y_prob, descending=True)
    results = [(food_101_classes[idx], float(prob)) for idx, prob in zip(sorted_indices, sorted_prob)]

    return results
