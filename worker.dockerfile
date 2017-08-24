FROM ubuntu:xenial
MAINTAINER Dmitry Ukov

ENV DEBIAN_FRONTEND=noninteractive LC_ALL=C.UTF-8 LANG=C.UTF-8 PIP_INDEX_URL=${pip_index_url:-https://pypi.python.org/simple/}

RUN set -x \
  && apt-get update \
  && apt-get install -y --no-install-recommends \
    apt-transport-https \
    ca-certificates \
  && apt-get -o Dpkg::Options::="--force-confmiss" install -y --reinstall netbase \
  && apt-get clean \
  && apt-get autoremove --purge -y \
  && rm -r /var/lib/apt/lists/*

COPY .git            /project/.git

RUN set -x \
  && apt-get update \
  && apt-get install -y --no-install-recommends \
    python \
    python-dev \
    python-pip \
    git \
    wget \
  && wget --no-check-certificate https://github.com/Yelp/dumb-init/releases/download/v1.2.0/dumb-init_1.2.0_amd64.deb \
  && dpkg -i dumb-init_1.2.0_amd64.deb \
  && rm dumb-init_*.deb \
  && wget --no-check-certificate https://github.com/jwilder/dockerize/releases/download/v0.3.0/dockerize-linux-amd64-v0.3.0.tar.gz \
  && tar -C /usr/local/bin -xzf dockerize-linux-amd64-v0.3.0.tar.gz \
  && rm dockerize-linux-amd64-v0.3.0.tar.gz \
  && pip --no-cache-dir --disable-pip-version-check install 'setuptools==32.3.1' \
  && cd /project \
  && git reset --hard \
  && pip install --no-cache-dir --disable-pip-version-check -r /project/requirements.txt \
  && pip install --no-cache-dir --disable-pip-version-check /project \
  && apt-get purge -y git python-pip python-dev \
  && apt-get clean \
  && apt-get autoremove --purge -y \
  && cd / \
  && rm -r /project \
  && rm -r /var/lib/apt/lists/*

ENTRYPOINT ["/usr/bin/dumb-init", "-c", "--"]
CMD ["dockerize", "--", "scworker"]
