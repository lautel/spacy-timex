###############################################################################
# File: Dockerfile
# Author: Laura Cabello
# Date: 20/12/2020
# Comments: Dockerfile to generate the NLP image with required libraries installed.
# Run the following command to build the image: "docker build --rm=true -t nlp:latest -f Dockerfile ."
###############################################################################

FROM python:3.7-stretch

# INSTALL NLP SOURCE-CODE
ADD requirements.txt /mnt/NLP/
WORKDIR /mnt/NLP
RUN pip install -r requirements.txt && \
    python -m spacy download en_core_web_sm

COPY . /mnt/NLP
#COPY ./kickstart.sh /mnt/NLP

# PYTONPATH ENV
ENV PYTHONPATH="$PYTHONPATH:/mnt/NLP"

RUN apt-get -y remove build-essential && \
    apt-get clean && \
    apt -y autoremove && \
    rm -rf /var/lib/apt/lists/*

#ENTRYPOINT ["/bin/bash", "-c", "/mnt/NLP/kickstart.sh"]
CMD ["/bin/bash"]