## I. 作業流れ	
1. JESONで環境準備
2. dockerfile実行
3. docker imageにtagをつける
4. ACRにプッシュ

## II. JESONで環境準備
- OS: UBUNTU 18.04
- [/home/nvidia/aml_workdir]パスを作成しておく。
- Dogcatイメージが[/home/nvidia/aml_workdir/dog_cat_images]に保存されることを仮定する
- [score.py]、[dockerfile]、[.bashrc]を作成しておきます。
- [/home/nvidia/aml_workdir/outputs]にAMLモジュール(keras_simple.h5)を保存しておく。(前のステップのモジュール)

## III. DOCKERFILE実行
### 1. build dockerfile
- dockerfile内容:
    ```
    FROM ubuntu:18.04

    RUN apt-get update && \
        apt-get install libhdf5-serial-dev hdf5-tools libhdf5-dev zlib1g-dev zip libjpeg8-dev liblapack-dev libblas-dev gfortran -y && \
        apt-get install python3.6 -y && \
        apt-get install -y python3-pip && \
        apt-get install python3-h5py -y && \
        pip3 install --upgrade pip && \
        pip3 install -U pip testresources setuptools && \
        pip3 install -U numpy==1.18.2 keras_preprocessing==1.1.0 keras_applications==1.0.8 gast==0.2.2 protobuf && \
        apt-get install wget -y && \
        wget https://developer.download.nvidia.com/compute/redist/jp/v43/tensorflow-gpu/tensorflow_gpu-2.0.0+nv19.12-cp36-cp36m-linux_aarch64.whl && \
        pip3 install tensorflow_gpu-2.0.0+nv19.12-cp36-cp36m-linux_aarch64.whl && \
        rm tensorflow_gpu-2.0.0+nv19.12-cp36-cp36m-linux_aarch64.whl && \
        export PYTHONPATH="/usr/lib/python3.6/dist-packages"

    RUN pip3 install pillow

    COPY /.bashrc /root/.bashrc
    RUN /bin/bash -c "source /root/.bashrc"
    COPY /outputs/. /home/aml_workdir/outputs/
    COPY /score.py /home/aml_workdir/score.py
    ```
- build dockerfile:
    ```
    cd /home/nvidia/aml_workdir/
    docker build -t myimage:v1 --force-rm -f dockerfile .
    ```
### 2. Dockerイメージの動き確認
- 環境準備:
    - JETSONのtensorflow使えるように、Cudaを設定する必要
    - Cuda設定はJETSONのホームページにより手順通り
    - Docker ImageでCuda使えるように、イメージにJETSON HostのCudaパスを共有させる必要
- run docker:
    ```
    docker run -it --name aml \            
        -v /home/nvidia/aml_workdir/dog_cat_images:/home/aml_workdir/dog_cat_images \           
        -v /usr/local/cuda:/usr/local/cuda \           
        -v /usr/local/cuda-10.0:/usr/local/cuda-10.0 \
        myimage:v1
    ```
- docker imageにtagをつける
    - `docker tag myimage:v1 [azure container registry name].azurecr.io/myimage:v1`
- ACRにプッシュ
    - `docker push [azure container registry name].azurecr.io/myimage:v1`