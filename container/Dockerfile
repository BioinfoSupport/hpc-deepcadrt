FROM nvidia/cuda:11.1.1-cudnn8-devel-ubuntu20.04

ARG DEBIAN_FRONTEND=noninteractive
RUN apt-get update && apt-get install -y \
  python3 \
  python3-pip \
  git \
  ffmpeg \
  libsm6 \
  libxext6 \
  && rm -rf /var/lib/apt/lists/*

RUN pip3 install \
  torch \
  torchvision \
  torchaudio

RUN pip3 install deepcad onnx
#RUN git clone https://github.com/cabooster/DeepCAD-RT

#RUN pip3 install \
#  jupyterlab

ADD deepcadrt_train.py /usr/bin/
ADD deepcadrt_test.py /usr/bin/

VOLUME /DeepCAD-RT/DeepCAD_RT_pytorch/notebooks/datasets/
WORKDIR /DeepCAD-RT/DeepCAD_RT_pytorch/notebooks/
#EXPOSE 8888  
#CMD ["jupyter","lab","--port=8888","--ip=0.0.0.0","--allow-root"]

