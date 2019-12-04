FROM python:3.6
ADD . /app

RUN cd /app && \
python setup.py install && \
rm -rf /app

ENTRYPOINT ["mfutil"]
