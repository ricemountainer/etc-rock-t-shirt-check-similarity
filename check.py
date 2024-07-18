import os
import numpy as np
from PIL import Image
from torchvision import models, transforms
import torch
import sys
import csv
import shutil
# 特徴量抽出のための変換
transform = transforms.Compose([
    transforms.Resize((224, 224)),
    transforms.ToTensor(),
    transforms.Normalize(mean=[0.485, 0.456, 0.406], std=[0.229, 0.224, 0.225]),
])

# 事前学習モデルのロード
model = models.resnet50(pretrained=True)
model = model.eval()

# 類似性の閾値
THRESHOLD=0.8

# 履歴CSV
HISTORY_CSV_FILE="history.csv"

# 画像から特徴量を抽出する関数
def extract_features(img):
    img_t = transform(img)
    batch_t = torch.unsqueeze(img_t, 0)
    with torch.no_grad():
        features = model(batch_t)
    return features.numpy().flatten()

# 類似度を計算する関数（ここではコサイン類似度を使用）
def cosine_similarity(features1, features2):
    return np.dot(features1, features2) / (np.linalg.norm(features1) * np.linalg.norm(features2))

# 新しい画像の特徴量と過去の画像の特徴量を比較する関数
def check_similarity(new_image_features, existing_images_features, threshold=THRESHOLD):
    similar_images = []
    for file_path, features in existing_images_features.items():
        similarity = cosine_similarity(new_image_features, features)
        if similarity > threshold:
            similar_images.append((file_path, similarity))
    return similar_images

# ローカルディレクトリ内の全画像ファイルのパスを取得する関数
def get_all_image_files(directory):
    supported_extensions = ['.jpg', '.jpeg', '.png', '.bmp', '.gif']
    image_files = []
    for root, _, files in os.walk(directory):
        for file in files:
            if any(file.lower().endswith(ext) for ext in supported_extensions):
                image_files.append(os.path.join(root, file))
    return image_files


def remove_prefix_suffix(input_str):
    # 先頭の"./all/"を取り除く
    if input_str.startswith("./all/"):
        input_str = input_str[len("./all/"):]
    
    # 末尾の".jpg"を取り除く
    if input_str.endswith(".jpg"):
        input_str = input_str[:-len(".jpg")]
    
    return input_str

def read_histiry_csv():
    result_dict = {}

    # CSVファイルを読み込む
    with open(HISTORY_CSV_FILE, mode='r', encoding='utf-8') as csvfile:
        csv_reader = csv.reader(csvfile)
    
        # 各行を処理
        for row in csv_reader:
            if len(row) >= 4:
                key = row[0]
                values = row[1:4]
                result_dict[key] = values
    
    return result_dict

def print_check_result(similar_images):
    history_dic=read_histiry_csv()
    if similar_images:
        print("類似した画像が見つかりました。")
        for file_path, similarity_score in similar_images:
            #print(f"ファイル名: {file_path}, 類似度スコア: {similarity_score}")
            key=remove_prefix_suffix(file_path)
            val=history_dic.get(key)
            print(f"ファイル名: {file_path}, 詳細:{val}, 類似度スコア: {similarity_score}")
    else:
        print("類似した画像は見つかりませんでした。")

def main():
    # 使用例
    directory_path = './all/'  # 画像ファイルが含まれるディレクトリのパス
    file_name=sys.argv[1]
    new_image_path = file_name  # 新しい画像ファイルのパス

    # 新しい画像の読み込みと特徴量抽出
    new_image = Image.open(new_image_path)
    new_image_features = extract_features(new_image)

    # ディレクトリ内のすべての画像ファイルのパスを取得
    existing_image_files = get_all_image_files(directory_path)

    # 過去の画像の特徴量を取得
    existing_images_features = {}
    for image_file in existing_image_files:
        if image_file != new_image_path:  # 新しい画像と既存の画像を区別
            img = Image.open(image_file)
            features = extract_features(img)
            existing_images_features[image_file] = features

    # 類似性の判定
    similar_images = check_similarity(new_image_features, existing_images_features)
    print_check_result(similar_images)

    # ファイル移動
    destination_path = directory_path + file_name
    shutil.move(new_image_path, destination_path)

if __name__ == "__main__":
    main()
