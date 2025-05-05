import cv2
from ultralytics import YOLO


def cmr_detection(config):
    # 加载YOLOv11模型
    model = YOLO(config['model_path'])

    # 打开摄像头（0表示默认摄像头）
    cap = cv2.VideoCapture(0)

    if not cap.isOpened():
        print("Error: Unable to open camera")
        return

    try:
        while True:
            # 读取摄像头帧
            ret, frame = cap.read()
            if not ret:
                print("Error: Failed to capture frame")
                break

            # 进行推理
            results = model(frame)

            # 获取检测结果并绘制到帧上
            annotated_frame = results[0].plot()

            # 显示结果
            cv2.imshow('YOLOv11 Camera Detection', annotated_frame)

            # 按'q'键退出
            if cv2.waitKey(1) & 0xFF == ord('q'):
                break

    except Exception as e:
        print(f"An error occurred: {str(e)}")

    finally:
        # 释放资源
        cap.release()
        cv2.destroyAllWindows()


