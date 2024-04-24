
FROM python:3.10-slim


ENV DEBIAN_FRONTEND noninteractive


RUN apt-get update && apt-get install -y \
    tk \
    python3-tk \
    wget \
    firefox-esr \
    xvfb \
    && rm -rf /var/lib/apt/lists/*


RUN wget https://github.com/mozilla/geckodriver/releases/download/v0.30.0/geckodriver-v0.30.0-linux64.tar.gz \
    && tar -xzf geckodriver-v0.30.0-linux64.tar.gz \
    && mv geckodriver /usr/local/bin/ \
    && chmod +x /usr/local/bin/geckodriver \
    && rm geckodriver-v0.30.0-linux64.tar.gz


WORKDIR /app

COPY . /app


RUN pip install --no-cache-dir -r requirements.txt


EXPOSE 5000

ENV NAME World
ENV DISPLAY=:99

CMD Xvfb :99 -screen 0 1280x720x24 & python app.py

