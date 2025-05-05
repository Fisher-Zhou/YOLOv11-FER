import json
from .image_recognition import img_recognition
from .video_recognition import vdo_recognition
from .camera_recognition import cmr_detection
import os
import shutil
import pprint
import re
def read_config(config_path):
    """
    读取config.json文件

    -------

    """
    try:
        with open(config_path, 'r', encoding='utf-8') as file:
            data = json.load(file)
    except FileNotFoundError:
        print("文件未找到，请检查文件路径是否正确。")
    except json.JSONDecodeError:
        print("文件内容不是有效的 JSON 格式。")
    return data

def get_next_filename(output_dir, base_name, extension):
    """
    检查output_dir中的文件，找到基于base_name排序的序号，并返回下一个序号所对应的地址
    Generate the next sequential filename that doesn't exist.
    Example: if 'output_1.jpg' exists, return 'output_2.jpg'.
    """
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)

    # Find all files in the directory matching the pattern
    pattern = re.compile(rf"{base_name}_(\d+)\.{extension}$")
    max_num = 0

    for filename in os.listdir(output_dir):
        match = pattern.match(filename)
        if match:
            num = int(match.group(1))
            max_num = max(max_num, num)

    # Return the next number
    next_num = max_num + 1
    return os.path.join(output_dir, f"{base_name}_{next_num}.{extension}")

class menu:
    def __init__(self,config):
        self.config = config
        self.options = {
            '1': ('上传', self.upload),
            '2': ('图像识别', self.image_recognition),
            '3': ('视频识别', self.video_recognition),
            '4': ('摄像头识别', self.cmr_recognition),
            '5': ('查看', self.check),
            '6': ('删除文件',self.clear_folder),
            '7': ('退出', self.exit_menu)
        }

    def display_menu(self):
        """
        展示菜单
        Returns
        -------

        """
        print("\n=== 识别系统菜单 ===")
        for key, (name, _) in self.options.items():
            print(f"{key}. {name}")
        print("==================")

    def upload(self):
        #选择图像还是视频
        options={
            '1':'images',
            '2':'videos'
        }
        pprint.pprint(options)
        choice=input("选择你要上传的类型")
        if choice=='1':
            try:
                os.startfile(self.config['input_image_path'])
            except FileNotFoundError:
                print("错误：文件夹不存在！")
            except OSError as e:
                print(f"打开文件夹失败：{e}")
        elif choice=='2':
            try:
                os.startfile(self.config['input_video_path'])
            except FileNotFoundError:
                print("错误：文件夹不存在！")
            except OSError as e:
                print(f"打开文件夹失败：{e}")
        else:
            print('输入错误')
            return

    def image_recognition(self):
        """
        识别
        Returns
        -------

        """
        print("正在执行图像识别功能...")
        img_recognition(self.config)
        return



    def video_recognition(self):
        """
        识别
        Returns
        -------

        """
        print("正在执行图像识别功能...")
        vdo_recognition(self.config)

        return


    def cmr_recognition(self):
        """
        识别
        Returns
        -------

        """
        print("正在执行图像识别功能...")
        cmr_detection(self.config)


    def check(self):
        # 选择图像还是视频
        options = {
            '1': 'images',
            '2': 'videos'
        }
        pprint.pprint(options)
        choice = input("选择你要打开的类型")
        if choice == '1':
            try:
                os.startfile(self.config['output_image_path'])
            except FileNotFoundError:
                print("错误：文件夹不存在！")
            except OSError as e:
                print(f"打开文件夹失败：{e}")
        elif choice == '2':
            try:
                os.startfile(self.config['output_video_path'])
            except FileNotFoundError:
                print("错误：文件夹不存在！")
            except OSError as e:
                print(f"打开文件夹失败：{e}")
        else:
            print('输入错误')
            return
    def clear_folder(self):
        """
        删除目标文件夹下的所有文件
        处理后的文件会放入output文件夹里，如果output中的文件已经使用完毕，可以使用此函数删除其下所有文件
        input文件也可以由此删除

        Args:
            folder_path (str): Path to the folder whose contents are to be deleted.
        """
        options={
            '1':"input_image",
            '2':"input_video",
            '3':"output_image",
            '4':"output_video",
            '5':'exit'
        }
        folder=None
        while True:
            pprint.pprint(options)
            choice = input("请选择要清空的文件夹 (1-5): ")
            if choice in options:
                if choice=='1':
                    folder = os.path.abspath(self.config["input_image_path"])
                elif choice == '2':
                    folder = os.path.abspath(self.config["input_video_path"])
                elif choice == '3':
                    folder = os.path.abspath(self.config["output_image_path"])
                elif choice == '4':
                    folder = os.path.abspath(self.config["output_video_path"])
                elif choice=='5':
                    break
            else:
                print("无效选择，请重试！")

            if 'folder' not in locals():
                return

            if not os.path.exists(folder):
                print(f"Folder '{folder}' does not exist.")
                return

            if not os.path.isdir(folder):
                print(f"'{folder}' is not a folder.")
                return

            for item in os.listdir(folder):
                item_path = os.path.join(folder, item)
                try:
                    if os.path.isfile(item_path) or os.path.islink(item_path):
                        os.unlink(item_path)  # Delete file or symbolic link
                    elif os.path.isdir(item_path):
                        shutil.rmtree(item_path)  # Delete folder and its contents
                except Exception as e:
                    print(f"Failed to delete {item_path}: {e}")

            print(f"All contents in '{folder}' have been deleted.")
    def exit_menu(self):
        """
        退出菜单
        Returns
        -------

        """
        print("退出系统...")
        return False

    def run(self):
        """
        菜单选择界面
        Returns
        -------

        """
        while True:
            self.display_menu()
            choice = input("请选择功能 (1-7): ")
            if choice in self.options:
                action = self.options[choice][1]
                if action() is False:
                    break
            else:
                print("无效选择，请重试！")

