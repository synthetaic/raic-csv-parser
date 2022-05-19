FROM python:3.8

WORKDIR /root

ADD raic_download_images.py /root/
ADD requirements.txt /root/

RUN pip install -r /root/requirements.txt

