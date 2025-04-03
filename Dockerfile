FROM python:3.11.9-slim

RUN apt update
RUN python --version

RUN mkdir "/SkyLink-Project"

WORKDIR /SkyLink-Project

COPY ./src ./src
COPY ./requirements.txt ./requirements.txt

COPY ./commands ./commands

RUN python -m pip install --upgrade & pip install -r ./requirements.txt

CMD ["bash"]