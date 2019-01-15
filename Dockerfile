FROM python:3.6

RUN pip3 install --no-cache-dir \
        datascience \
        nbconvert \
        jupyter_client \
        ipykernel \
        matplotlib \
        pandas \
        ipywidgets \
        scipy

RUN pip3 install --no-cache-dir gofer-grader==1.0.3

COPY . /srv/repo

WORKDIR /srv/repo
