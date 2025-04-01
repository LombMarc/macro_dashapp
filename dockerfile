FROM python:3.10-slim 

WORKDIR /macro_dashapp

COPY . /macro_dashapp

RUN pip install -r requirements.txt

RUN apt-get update && apt-get install -y \
    chromium \
    chromium-driver \
    && rm -rf /var/lib/apt/lists/*

ENV PATH="/usr/lib/chromium-browser:/usr/bin:${PATH}"

EXPOSE 8050

CMD ["python", "app.py"]