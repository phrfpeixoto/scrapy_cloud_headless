FROM scrapinghub/scrapinghub-stack-scrapy:1.3-py3
RUN apt-get -y --no-install-recommends install zip unzip jq
RUN printf "deb http://archive.debian.org/debian/ jessie main\ndeb-src http://archive.debian.org/debian/ jessie main\ndeb http://security.debian.org jessie/updates main\ndeb-src http://security.debian.org jessie/updates main" > /etc/apt/sources.list

#============================================
# Firefox and geckodriver
#============================================
RUN apt-get update                             \
 && apt-get install -y --no-install-recommends \
    ca-certificates curl firefox-esr           \
 && rm -fr /var/lib/apt/lists/*                \
 && curl -L https://github.com/mozilla/geckodriver/releases/download/v0.24.0/geckodriver-v0.24.0-linux64.tar.gz | tar xz -C /usr/local/bin

#============================================
# crawlera-headless-proxy
#============================================

RUN curl -L https://github.com/scrapinghub/crawlera-headless-proxy/releases/download/1.1.1/crawlera-headless-proxy-linux-amd64 -o /usr/local/bin/crawlera-headless-proxy \
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
