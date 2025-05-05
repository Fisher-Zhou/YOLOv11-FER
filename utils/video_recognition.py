from ultralytics import YOLO
import cv2
import os
from pathlib import Path
def detect_objects_in_video(model_path, video_path, output_dir=None,base_name="output",extension='mp4'):
    # 加载 YOLOv11 模型
    model = YOLO(model_path)
    # 打开视频文件
    cap = cv2.VideoCapture(video_path)
    if cap is None:
        print(f'Could not load video at {video_path}')
    # 获取视频属性
    fps = cap.get(cv2.CAP_PROP_FPS)
    width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
    height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))

    # 设置输出目录，默认为当前目录
    if output_dir is None:
        raise ValueError(f"{output_dir} does not exist")
    else:
        # 确保输出目录存在
        os.makedirs(output_dir, exist_ok=True)

    # 生成唯一的输出文件名（base_name + 序号 + extension）
    from .util import get_next_filename
    output_path=get_next_filename(output_dir=output_dir,base_name=base_name,extension=extension)

    # 定义编解码器并创建 VideoWriter 对象
    fourcc = cv2.VideoWriter_fourcc(*'mp4v')
    out = None
    if output_path:
        out = cv2.VideoWriter(output_path, fourcc, fps, (width, height))

    # 逐帧处理视频
    while cap.isOpened():
        ret, frame = cap.read()
        if not ret:
            break

        # 在帧上运行 YOLOv11 检测
        results = model(frame)

        # 在帧上可视化检测结果
        annotated_frame = results[0].plot()

        # 如果有输出路径，将带注释的帧写入输出视频
        if out is not None:
            out.write(annotated_frame)
        else:
            # 否则，实时显示带注释的帧
            cv2.imshow('YOLOv11 Detection', annotated_frame)
            if cv2.waitKey(1) & 0xFF == ord('q'):
                break

    # 释放资源
    cap.release()
    if out is not None:
        out.release()
    cv2.destroyAllWindows()
def process_video_or_folder(model_path, video_path, output_dir=None,base_name="output",extension='mp4'):
    video_extension = {'.mp4'}
    if not output_dir.exists():
        os.makedirs(output_dir)
    if video_path.is_file():
        if video_path.suffix.lower() in video_extension:
            print(f'Processing single video:{video_path}')
            detect_objects_in_video(model_path, video_path, output_dir=None,base_name=base_name,extension=extension)
        else:
            print(f'Error:{video_path} is not a supported image format.')
    elif video_path.is_dir():
        print(f"Processing images in folder: {video_path}")
        for file_path in video_path.iterdir():
            if file_path.is_file() and file_path.suffix.lower() in video_extension:
                print(f'Processing video:{file_path}')
                detect_objects_in_video(model_path, file_path, output_dir=None,base_name=base_name,extension=extension)
        print("folder processing completed")

    else:
        print(f"Error: '{video_path}' is neither a file nor a folder.")

def vdo_recognition(config):
    model_path = Path(config["model_path"])
    video_path = Path(config["input_video_path"])
    output_dir = Path(config["output_video_path"])

    process_video_or_folder(model_path,video_path,output_dir)
