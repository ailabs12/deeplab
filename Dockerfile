FROM ubuntu:16.04
MAINTAINER "Konstantin Bakhtin"

RUN apt-get update && apt-get install -y wget ca-certificates \
    git curl vim python-dev python-pip \
    libfreetype6-dev libpng12-dev libhdf5-dev

RUN pip install --upgrade pip
RUN pip install tensorflow
RUN pip install numpy pandas sklearn matplotlib seaborn jupyter pyyaml h5py
RUN pip install keras keras-applications keras-preprocessing --no-deps
RUN pip install matplotlib

#add
RUN pip2 install jupyter
RUN pip2 install pillow
RUN ipython2 kernelspec install-self

RUN ["mkdir", "notebooks"]
COPY jupyter_notebook_config.py /root/.jupyter/
COPY run_jupyter.sh /

# Jupyter and Tensorboard ports
EXPOSE 8888 6006

# Store notebooks in this mounted directory
VOLUME /notebooks

CMD ["/run_jupyter.sh"]

