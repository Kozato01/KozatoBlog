FROM python:3.13-slim

WORKDIR /app

ENV PORT=3000
ENV PYTHONUNBUFFERED=1

COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt

# Só os arquivos que o site precisa — nada de .env ou currículo
COPY app.py index.html ./
COPY utils ./utils
COPY templates ./templates
COPY content ./content
COPY assets ./assets

# Volume de dados (posts, recados e contador de visitas)
RUN useradd --create-home --uid 1000 kozato \
    && mkdir -p /app/data \
    && chown -R kozato:kozato /app/data
USER kozato

EXPOSE 3000

HEALTHCHECK --interval=30s --timeout=3s --start-period=5s \
  CMD python -c "import os,sys,urllib.request; sys.exit(0 if urllib.request.urlopen('http://localhost:'+os.environ['PORT']+'/api/health').status == 200 else 1)"

# Um worker só com threads: o site só lê arquivo, dá e sobra.
CMD ["gunicorn", "--workers", "1", "--threads", "4", "--bind", "0.0.0.0:3000", "app:app"]
