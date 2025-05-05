# 首先进行monkey-patching
from gevent import monkey

monkey.patch_all()

from flask import Flask, request, jsonify, send_from_directory
from flask_socketio import SocketIO, emit
import os
from flask_cors import CORS
from werkzeug.utils import secure_filename
from threading import Thread
import cv2
import numpy as np
import base64
from io import BytesIO
from PIL import Image
import utils
import sys
import subprocess

app = Flask(__name__)
# 配置CORS和WebSocket
CORS(app, resources={r"/*": {"origins": "*"}})
socketio = SocketIO(app, cors_allowed_origins="*", async_mode='gevent')

# 设置上传图片文件夹
UPLOAD_IMAGE_FOLDER = 'input/input_image/'
app.config['UPLOAD_IMAGE_FOLDER'] = UPLOAD_IMAGE_FOLDER

# 设置上传视频文件夹
UPLOAD_VIDEO_FOLDER = 'input/input_video/'
app.config['UPLOAD_VIDEO_FOLDER'] = UPLOAD_VIDEO_FOLDER

# 确保上传文件夹存在
os.makedirs(app.config['UPLOAD_IMAGE_FOLDER'], exist_ok=True)
os.makedirs(app.config['UPLOAD_VIDEO_FOLDER'], exist_ok=True)

# 允许的文件扩展名
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'mp4', 'avi', 'mov', 'mkv'}

config=utils.util.read_config('config.json')
menu=utils.util.menu(config)
def allowed_file(filename):
    """检查文件扩展名是否允许"""
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


@app.route('/')
def home():
    return 'Welcome to the homepage!'


@app.route('/favicon.ico')
def favicon():
    return send_from_directory(os.path.join(app.root_path, 'static'), 'favicon.ico')


@app.route('/upload_image', methods=['POST'])
def upload_file():
    if 'file' not in request.files:
        return jsonify({'error': '没有文件部分'}), 400
    file = request.files['file']
    if file.filename == '':
        return jsonify({'error': '没有选择文件'}), 400
    if file and allowed_file(file.filename):
        filename = secure_filename(file.filename)
        file_path = os.path.join(app.config['UPLOAD_IMAGE_FOLDER'], filename)
        file.save(file_path)
        # 发送WebSocket消息
        socketio.emit('image_uploaded', {'filename': filename})
        # socketio.emit('start_image_recognition',{'filename': filename})
        print('图片上传成功')
        return jsonify({'message': '文件上传成功', 'filename': filename}), 200
    return jsonify({'error': '不支持的文件类型'}), 400


@app.route('/upload_video', methods=['POST'])
def upload_video():
    if 'file' not in request.files:
        return jsonify({'error': '没有文件部分'}), 400

    file = request.files['file']
    if file.filename == '':
        return jsonify({'error': '没有选择文件'}), 400

    if file and allowed_file(file.filename):
        filename = secure_filename(file.filename)
        file_path = os.path.join(app.config['UPLOAD_VIDEO_FOLDER'], filename)
        file.save(file_path)
        # 发送WebSocket消息
        socketio.emit('video_uploaded', {'filename': filename})
        return jsonify({'message': '视频上传成功'}), 200
    return jsonify({'error': '不支持的文件类型'}), 400

# 启动摄像头识别
@app.route('/start_camera_recognition', methods=['POST'])
def start_camera_recognition():
    menu.cmr_recognition()
    # 返回成功响应
    return jsonify({
            'success': True,
            'message': '摄像头识别启动成功',
        }), 200


@app.route('/open_directory', methods=['POST'])
def open_directory():
    try:
        data = request.get_json()
        directory_path = data.get('path')

        if not directory_path:
            return jsonify({'error': '未提供目录路径'}), 400

        # 转换为绝对路径
        absolute_path = os.path.abspath(directory_path)

        # 检查目录是否存在
        if not os.path.exists(absolute_path):
            return jsonify({'error': '目录不存在'}), 404

        # 检查路径是否是目录
        if not os.path.isdir(absolute_path):
            return jsonify({'error': '提供的路径不是目录'}), 400

        # 尝试打开目录
        try:
            if sys.platform == 'win32':
                os.startfile(absolute_path)
            elif sys.platform == 'darwin':  # macOS
                subprocess.run(['open', absolute_path])
            else:  # Linux
                subprocess.run(['xdg-open', absolute_path])
            return jsonify({'message': '目录已打开'}), 200
        except Exception as e:
            return jsonify({'error': f'打开目录失败: {str(e)}'}), 500

    except Exception as e:
        # 记录异常信息
        print(f"后端错误: {str(e)}")
        return jsonify({'error': '服务器内部错误'}), 500
@socketio.on('connect')
def handle_connect():
    print('客户端已连接')
    emit('connection_response', {'data': '连接成功'})


@socketio.on('disconnect')
def handle_disconnect():
    print('客户端已断开连接')


@socketio.on('start_image_recognition')
def handle_image_recognition(data):
    """处理图片识别请求"""
    try:
        filename = data.get('filename')
        print(f'收到图片识别请求: {filename}')

        # 检查文件是否存在
        file_path = os.path.join(app.config['UPLOAD_IMAGE_FOLDER'], filename)
        if not os.path.exists(file_path):
            raise FileNotFoundError(f'文件不存在: {filename}')

        # 开始处理图片
        print(f'开始识别图片: {filename}')
        menu.image_recognition()
        print(f'图片识别完成: {filename}')

        # 发送完成消息
        socketio.emit('recognition_complete', {
            'filename': filename,
            'type': 'image',
            'message': '图片识别完成'
        })

    except Exception as e:
        print(f'图片识别错误: {str(e)}')
        socketio.emit('recognition_error', {'error': str(e)})


@socketio.on('start_video_recognition')
def handle_video_recognition(data):
    """处理视频识别请求"""
    try:
        filename = data.get('filename')
        print(f'收到视频识别请求: {filename}')

        # 检查文件是否存在
        file_path = os.path.join(app.config['UPLOAD_VIDEO_FOLDER'], filename)
        if not os.path.exists(file_path):
            raise FileNotFoundError(f'文件不存在: {filename}')

        # 开始处理视频
        print(f'开始识别视频: {filename}')
        menu.video_recognition()
        print(f'视频识别完成: {filename}')

        # 发送完成消息
        socketio.emit('recognition_complete', {
            'filename': filename,
            'type': 'video',
            'message': '视频识别完成'
        })

    except Exception as e:
        print(f'视频识别错误: {str(e)}')
        socketio.emit('recognition_error', {'error': str(e)})

if __name__ == '__main__':
    print('启动服务器...')
    print('服务器运行在 http://localhost:5000')

    # 使用socketio.run启动应用，同时支持HTTP和WebSocket
    socketio.run(app, host='0.0.0.0', port=5000, debug=False)