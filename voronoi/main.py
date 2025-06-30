import sys
import os
import time
import numpy as np
import yaml
import cv2
from tqdm import tqdm
from utils import VoronoiGenerator
from splitters import VoronoiSplitter
from validation import VoronoiConfigValidator

def validate_config_file(config):
    """設定ファイルのバリデーションを実行する"""
    validator = VoronoiConfigValidator()
    if not validator.validate_config(config):
        validator.print_validation_results()
        sys.exit(1)
    if validator.get_warnings():
        validator.print_validation_results()
        print()

def check_directory(output_dir):
    """出力ディレクトリが存在するか確認し、上書きするか尋ねる。"""
    if os.path.exists(output_dir):
        answer = input(f"The directory '{output_dir}' already exists. Do you want to overwrite it? (y/n): ")
        if answer.lower() != "y":
            print("The process was interrupted.")
            sys.exit(0)

def create_directory(output_dir, datatype_info):
    """出力ディレクトリを作成する。"""
    for datatype, params in datatype_info.items():
        os.makedirs(f"{output_dir}/{datatype}/images", exist_ok=True)
        os.makedirs(f"{output_dir}/{datatype}/labels", exist_ok=True)

def save_images(output_dir, datatype, name, image, label):
    """画像とラベルを保存する。"""
    base_path = f"{output_dir}/{datatype}"
    cv2.imwrite(f"{base_path}/images/{name}.png", image)
    cv2.imwrite(f"{base_path}/labels/{name}.png", label)

def main(config_file):
    # configファイルの読み込み
    with open(config_file, 'r') as f:
        config = yaml.load(f, Loader=yaml.FullLoader)
    
    # バリデーション実行
    validate_config_file(config)
    
    voronoi_config = config["voronoi"]
    output_dir = voronoi_config["output_dir"]
    datatype_info = voronoi_config["datatype_info"]

    # 初期化
    voronoi_generator = VoronoiGenerator(voronoi_config)
    voronoi_splitter = VoronoiSplitter(voronoi_config)
    
    # 出力ディレクトリの作成
    check_directory(output_dir)
    create_directory(output_dir, datatype_info)

    # ボロノイ図の生成と保存
    for datatype, params in datatype_info.items():
        np.random.seed(params["seed"]) # 乱数シードの設定
        name_counter = 0
        for i in tqdm(range(params["diagram_num"]), desc=f"Generating {datatype} images"):
            # パラメータの取得
            point_params = voronoi_config["point_generation"]["params"]
            if voronoi_config["point_generation"]["method"] == "random":
                points_num_list = point_params["points_num"]
                points_num = points_num_list[i % len(points_num_list)]
                kwargs = {"points_num": points_num}
            else:  # poisson_disk
                min_distance_list = point_params["min_distance"]
                min_distance = min_distance_list[i % len(min_distance_list)]
                max_attempts = point_params.get("max_attempts", 100)
                kwargs = {"min_distance": min_distance, "max_attempts": max_attempts}
            
            voronoi_image, voronoi_label = voronoi_generator.generate(**kwargs) # ボロノイ図の生成
            image_list, label_list = voronoi_splitter(voronoi_image, voronoi_label) # 画像とラベルの分割

            # 保存
            for image, label in zip(image_list, label_list):
                save_images(output_dir, datatype, name_counter, image, label)
                name_counter += 1

if __name__ == "__main__":
    args = sys.argv
    try:
        # Validate the arguments
        if len(args) != 2:
            raise ValueError("ValueError: The number of arguments is invalid.")
        config_file = args[1]
        if not os.path.exists(config_file):
            raise FileNotFoundError(f"File not found: {config_file}")
        if not config_file.endswith('.yaml'):
            raise ValueError("ValueError: The configuration file must be in yaml format.")
        
        # Run the main function
        main(config_file)

    except Exception as e:
        print(e, file=sys.stderr)
        sys.exit(1)
