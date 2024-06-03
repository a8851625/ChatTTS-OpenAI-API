FROM nvidia/cuda:12.2.2-cudnn8-runtime-ubuntu22.04 

# 安装 Python 和依赖项
RUN apt-get update && apt-get install -y \
    python3-pip \
    python3-setuptools \
    python3-dev \
    vim curl wget  git\
    && ln -s /usr/bin/python3 /usr/bin/python \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /app
RUN git clone https://github.com/2noise/ChatTTS /app 
# 设置工作目录

# 复制当前目录的内容到容器的工作目录
COPY . /app
RUN mkdir -p /app/ChatTTS/assest &&  wget -P /app/ChatTTS/assest https://huggingface.co/2Noise/ChatTTS/resolve/main/asset/spk_stat.pt
# 安装 Python 依赖
RUN pip install --no-cache-dir -r requirements.txt

# 暴露服务端口
EXPOSE 5001

# 启动 Flask 应用
CMD ["python", "app.py"]
