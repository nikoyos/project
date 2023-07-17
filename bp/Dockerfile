# 使用基础的Python映像作为基础镜像
FROM python:3.8

# 设置工作目录
WORKDIR /project/bp

# 复制项目文件到容器中
#COPY . /project/bp

# 安装项目依赖
# gevent gevent-websocket Flask-Session
RUN apt update
Run pip install --upgrade pip
RUN pip install flask flask-socketio 
RUN pip uninstall gunicorn
RUN pip uninstall eventlet
RUN pip install gunicorn==20.1.0
RUN pip install eventlet==0.30.2


# 启动Gunicorn服务器
CMD ["gunicorn", "--worker-class", "eventlet", "-w", "1", "-b", "0.0.0.0:8002", "app:app"]

