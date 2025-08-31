import os
import json
from datetime import datetime
from PIL import Image # 导入Pillow库中的Image模块

# --- 配置 ---
IMAGE_DIR = 'images'  # 图片存放的根目录
OUTPUT_DIR = 'data'   # JSON 输出目录
OUTPUT_FILE = 'image-data.json' # JSON 文件名

# --- 排序时间依据配置 ---
# 您可以在这里选择排序依据：
# 'modification' -> 按文件修改时间排序 (推荐, 能准确反映图片内容何时被最后编辑)
# 'creation'     -> 按文件创建时间排序 (Windows下准确,但在Linux/Mac下可能不符合直觉)
SORT_BY_TIME = 'modification' 

# --- 加载分类映射表 ---
CATEGORY_MAP_FILE = 'category_map.json'
category_map = {}
try:
    with open(CATEGORY_MAP_FILE, 'r', encoding='utf-8') as f:
        category_map = json.load(f)
    print(f"Successfully loaded category map from '{CATEGORY_MAP_FILE}'.")
except FileNotFoundError:
    print(f"Warning: Category map file '{CATEGORY_MAP_FILE}' not found. Using folder names as display names.")
except json.JSONDecodeError:
    print(f"Error: Could not decode JSON from '{CATEGORY_MAP_FILE}'. Please check its format.")


def generate_image_data():
    """扫描图片目录并生成包含图片信息的 JSON 文件（包含宽高和指定日期）。"""
    image_data = []
    
    if not os.path.isdir(IMAGE_DIR):
        print(f"Error: Image directory '{IMAGE_DIR}' not found.")
        return

    # 获取所有图片并按指定时间排序，最新的在前
    all_images = []
    print(f"Sorting by file '{SORT_BY_TIME}' time.") # 提示当前排序模式
    
    for category in os.listdir(IMAGE_DIR):
        category_path = os.path.join(IMAGE_DIR, category)
        if os.path.isdir(category_path):
            for filename in os.listdir(category_path):
                if filename.lower().endswith(('.png', '.jpg', '.jpeg', '.gif', '.webp')):
                    image_path_full = os.path.join(category_path, filename)
                    try:
                        # 根据配置选择获取哪种时间戳
                        if SORT_BY_TIME == 'creation':
                            timestamp = os.path.getctime(image_path_full)
                        else: # 默认为 modification
                            timestamp = os.path.getmtime(image_path_full)
                            
                        all_images.append((timestamp, image_path_full, category, filename))
                    except Exception as e:
                        print(f"Warning: Could not get stats for file {image_path_full}. Error: {e}")
                        
    # 按时间戳降序排序（最新的在前）
    all_images.sort(key=lambda x: x[0], reverse=True)

    # 处理排序后的图片
    for timestamp, image_path_full, category, filename in all_images:
        try:
            with Image.open(image_path_full) as img:
                width, height = img.size
            
            # ---【关键修改】---
            # 修改了日期格式，加入了时:分:秒，以保留完整的时间信息
            date_added = datetime.fromtimestamp(timestamp).strftime('%Y-%m-%d %H:%M:%S')

        except Exception as e:
            print(f"Warning: Could not process file {image_path_full}. Error: {e}")
            continue

        original_src = os.path.join(IMAGE_DIR, category, filename).replace('\\', '/')

        # 根据映射表获取中文分类名
        category_name = category_map.get(category, category)

        image_info = {
            'src': original_src,
            'category': category,           # 英文ID，用于筛选
            'categoryName': category_name,  # 中文名，用于显示
            'filename': filename,
            'width': width,
            'height': height,
            'dateAdded': date_added
        }
        image_data.append(image_info)
    
    if not os.path.exists(OUTPUT_DIR):
        os.makedirs(OUTPUT_DIR)
        
    output_path = os.path.join(OUTPUT_DIR, OUTPUT_FILE)

    with open(output_path, 'w', encoding='utf-8') as f:
        json.dump(image_data, f, indent=2, ensure_ascii=False)
        
    print(f"Successfully generated image data at '{output_path}' with {len(image_data)} images.")

if __name__ == '__main__':
    generate_image_data()
