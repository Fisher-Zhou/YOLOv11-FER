#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
目标识别系统主程序
支持图像、视频和摄像头实时识别功能
"""

import utils
import os
import logging
import sys
from typing import Dict, Any

# 配置日志
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('app.log'),
        logging.StreamHandler(sys.stdout)
    ]
)
logger = logging.getLogger(__name__)

def setup_directories(config: Dict[str, Any]) -> None:
    """
    创建必要的目录结构
    
    Args:
        config: 配置字典，包含所需的路径信息
    """
    try:
        # 创建输出目录
        if not os.path.exists(config["output_path"]):
            os.makedirs(config["output_path"])
            logger.info(f"创建输出目录: {config['output_path']}")
        
        # 创建输入目录
        if not os.path.exists(config["input_image_path"]):
            os.makedirs(config["input_image_path"])
            logger.info(f"创建输入图像目录: {config['input_image_path']}")
        
        if not os.path.exists(config["input_video_path"]):
            os.makedirs(config["input_video_path"])
            logger.info(f"创建输入视频目录: {config['input_video_path']}")
            
    except Exception as e:
        logger.error(f"创建目录时发生错误: {str(e)}")
        raise

def main() -> None:
    """
    主程序入口函数
    负责初始化配置、创建目录并启动菜单系统
    """
    try:
        # 读取配置文件
        logger.info("正在读取配置文件...")
        config = utils.util.read_config('config.json')
        
        # 创建必要的目录
        setup_directories(config)
        
        # 初始化并运行菜单系统
        logger.info("正在启动菜单系统...")
        menu = utils.util.menu(config)
        menu.run()
        
    except FileNotFoundError:
        logger.error("配置文件不存在")
        print("错误：找不到配置文件 config.json")
        sys.exit(1)
    except Exception as e:
        logger.error(f"程序运行出错: {str(e)}")
        print(f"程序发生错误: {str(e)}")
        sys.exit(1)

if __name__ == '__main__':
    main()