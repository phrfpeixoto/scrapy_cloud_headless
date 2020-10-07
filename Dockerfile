FROM scrapinghub/scrapinghub-stack-scrapy:2.3
RUN apt-get update \
 && apt-get -y --no-install-recommends install zip unzip jq
RUN printf "deb http://ftp.debian.org/debian/ buster main\ndeb-src http://ftp.debian.org/debian/ buster main\ndeb http://security.debian.org buster/updates main\ndeb-src http://security.debian.org buster/updates main" > /etc/apt/sources.list

#============================================
# Firefox and geckodriver
#============================================
RUN apt-get update \
 && apt-get install -y --force-yes --no-install-recommends \
    ca-certificates curl firefox-esr procps \
 && rm -fr /var/lib/apt/lists/* \
 && curl -L https://github.com/mozilla/geckodriver/releases/download/v0.26.0/geckodriver-v0.26.0-linux64.tar.gz | tar xz -C /usr/local/bin

#============================================
# crawlera-headless-proxy
#============================================

RUN curl -L https://github.com/scrapinghub/crawlera-headless-proxy/releases/download/1.2.1/crawlera-headless-proxy-linux-amd64 -o /usr/local/bin/crawlera-headless-proxy \
 && chmod +x /usr/local/bin/crawlera-headless-proxy

COPY ./start-crawl /usr/local/bin/start-crawl

ENV TERM xterm
ENV SCRAPY_SETTINGS_MODULE scrapy_selenium.settings
RUN mkdir -p /app
WORKDIR /app
COPY ./requirements.txt /app/requirements.txt
RUN pip install --no-cache-dir -r requirements.txt
COPY . /app
RUN python setup.py install
