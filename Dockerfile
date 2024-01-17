# 使用官方Python运行时作为父镜像
FROM python:3.11.7-slim

# 设置工作目录
WORKDIR /app

# 安装需要的包
COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt -i https://pypi.tuna.tsinghua.edu.cn/simple

# 将当前目录内容复制到容器的 /app 目录下
COPY . .

# 命令在容器运行时执行
ENTRYPOINT ["python"]
CMD ["start.py"]