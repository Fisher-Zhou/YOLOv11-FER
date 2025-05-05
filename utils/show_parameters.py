def show_param(model_path):
    from ultralytics import YOLO

    model=YOLO('runs/train/exp14/weights/best.pt')

    for name, param in model.named_parameters():
        print(f"Name: {name}")
        print(f"Type: {type(param)}")
        print(f"Size: {param.size()}")
        print(f"Values: {param}")
        print("------------------------")