FROM python:alpine

LABEL org.opencontainers.image.source=https://github.com/gPoupon/PDFusion
LABEL org.opencontainers.image.title=PDFusion
LABEL org.opencontainers.image.version=1
LABEL org.opencontainers.image.licenses=MIT

ENV DEBIAN_FRONTEND=noninteractive

WORKDIR /PDFusion

COPY requirements.txt .

RUN pip install -r requirements.txt

RUN apk add --update-cache ghostscript && rm -rf /var/cache/apk/*

COPY ./src ./src

CMD ["python", "./src/fusionHA.py"]