FROM python:3.8-alpine
LABEL Maintainer="vergieet"
WORKDIR /usr/app/src
# RUN pkg install python
RUN apk add build-base
RUN pip install --upgrade pip setuptools wheel && \
    pip install --no-cache-dir numpy --no-binary :all: && \
    pip install --no-cache-dir Cython==0.29.32 && \
    pip install --no-cache-dir cvlib==0.2.2 && \
    pip install --no-cache-dir opencv-python==4.5.3.56  && \
    pip install --no-cache-dir tensorflow==1.14.0 && \
    pip install --no-cache-dir matplotlib==3.1.1 && \
    pip install --no-cache-dir Keras==2.2.5
    
COPY trafficlight.py ./usr/app/src
COPY jogja_cctv.jpg ./usr/app/src
CMD [ "python", "./trafficlight.py"]
