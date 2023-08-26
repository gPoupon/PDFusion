FROM python:alpine

LABEL org.opencontainers.image.source=https://github.com/gPoupon/PDFusion
LABEL org.opencontainers.image.title=PDFusion
LABEL org.opencontainers.image.version=1
LABEL org.opencontainers.image.licenses=MIT

ENV DEBIAN_FRONTEND=noninteractive
ENV PYTHONUNBUFFERED=1

WORKDIR /PDFusion

COPY requirements.txt .

RUN pip install -r requirements.txt

#RUN apt-get update && apt-get install -y ghostscript inotify-tools && rm -rf /var/lib/apt/lists/*

RUN apk add --update-cache inotify-tools ghostscript && rm -rf /var/cache/apk/*

COPY ./src ./src

CMD ["python", "./src/fusionHA.py"]