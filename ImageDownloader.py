import os
import requests
import csv
import time
import random
from tqdm import tqdm
from utils.file_clean import clean_filename

class ImageDownloader:
    def __init__(self, csv_file, image_dir='./image'):
        self.csv_file = csv_file
        self.image_dir = image_dir

        # 确保图片目录存在
        if not os.path.exists(self.image_dir):
            os.makedirs(self.image_dir)

    def download_images(self):
        # 读取 CSV 文件
        with open(self.csv_file, 'r', encoding='utf-8') as f:
            csv_reader = csv.reader(f)
            next(csv_reader)  # 跳过第一行标题

            # 获取总行数，便于计算进度
            total_images = sum(1 for row in csv_reader)
            f.seek(0)  # 回到文件开头
            next(csv_reader)  # 跳过标题

            # 使用 tqdm 包装 csv_reader，显示进度
            for row in tqdm(csv_reader, total=total_images, desc='下载图片', unit='张', ncols=100):
                if len(row) == 2:
                    name, url = row
                    # 下载图片
                    self.download_image(name, url)
                    # 每下载一张图片后休眠 2-5 秒，防止被网站封 IP
                    time.sleep(random.uniform(2, 5))

    def download_image(self, name, url):
        try: 
            # 清理文件名，防止出现非法字符
            clean_name = clean_filename(name)
            #获取图片的响应
            response = requests.get(url, stream=True)
            # 确保请求成功
            if response.status_code == 200:
                # 设置文件的保存路径，并以名称作为文件名
                file_path = os.path.join(self.image_dir, f"{clean_name}.jpg")

                # 打开文件并将响应内容写入文件
                with open(file_path, 'wb') as f:
                    for chunk in response.iter_content(chunk_size=1024):
                        f.write(chunk)
                print(f"下载成功：{name}")
            else:
                print(f"无法下载图片：{url}")
        except Exception as e:
            print(f"下载图片失败：{name}，错误信息： {e}")


if __name__ == '__main__':
    csv_file = './starbucks.csv'
    image_downloader = ImageDownloader(csv_file)
    image_downloader.download_images()