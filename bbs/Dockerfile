# 使用基础的Python映像作为基础镜像
FROM python:3.8

# 设置工作目录
WORKDIR /project/bbs

# 复制项目文件到容器中
#COPY . /project/bbs

# 安装项目依赖
RUN pip install flask gunicorn

# 启动Gunicorn服务器
CMD ["gunicorn", "--bind", "0.0.0.0:8003", "app:app"]
