# YOLOv11 目标检测系统

## 项目简介

本项目基于最新的 YOLOv11 算法，提供了高效、易用的目标检测解决方案，支持图像、视频和摄像头实时检测，适用于多种实际场景。项目结构清晰，便于二次开发和部署。

## 主要功能

- 支持图像目标检测
- 支持视频目标检测
- 支持摄像头实时检测
- 支持批量处理
- 结果可视化与输出
- 丰富的数据增强与训练策略

## 安装与环境配置

1. 克隆项目：
   ```bash
   git clone https://github.com/yourname/obj_recognition.git
   cd obj_recognition
   ```
2. 安装依赖：
   ```bash
   pip install -r requirements.txt
   ```
3. （可选）配置虚拟环境或conda环境，确保Python 3.8+。
4. 下载YOLOv11预训练权重，并放置到 `train/runs/train/exp32/weights/` 目录下。

## 快速上手

1. 运行主程序：
   ```bash
   python main.py
   ```
2. 按照菜单提示选择功能，如图像检测、视频检测、摄像头检测等。
3. 检测结果将保存在 `output/` 目录下。

## 目录结构

```
obj_recognition/
├── input/                 # 输入文件目录
│   ├── input_image/      # 输入图像
│   └── input_video/      # 输入视频
├── output/               # 输出文件目录
│   ├── output_image/     # 输出图像
│   └── output_video/     # 输出视频
├── train/                # 训练相关文件及权重
├── utils/                # 工具函数
├── config.json           # 配置文件
├── main.py               # 主程序
├── requirements.txt      # 依赖包列表
├── README.md             # 项目说明文档
└── 研究报告.md           # 训练与实验报告
```

## 常见问题（FAQ）

- **Q: 权重文件太大，如何获取？**
  A: 请参考README中的权重下载说明，或在Issues区留言获取。
- **Q: 运行报错缺少依赖？**
  A: 请确保已正确执行 `pip install -r requirements.txt`。
- **Q: 如何更换自己的数据集？**
  A: 修改 `config.json` 和 `datasets/data.yaml`，并将数据放入相应目录。

## 贡献方式

欢迎提交Issue、Pull Request或建议！如有意参与开发，请遵循以下流程：
1. Fork本仓库
2. 新建分支进行开发
3. 提交PR并详细描述修改内容

## 联系方式

- 作者邮箱：your_email@example.com
- 项目主页：https://github.com/yourname/obj_recognition

## 开源协议

本项目基于 MIT License 开源，您可以自由使用、修改和分发。详情见下：

---

MIT License

Copyright (c) 2024 yourname

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE. 