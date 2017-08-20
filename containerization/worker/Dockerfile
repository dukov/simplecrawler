FROM ubuntu:xenial
MAINTAINER Dmitry Ukov

RUN set -x \
  && apt-get update \
  && apt-get install -y --no-install-recommends \
    apt-transport-https \
    ca-certificates \
  && apt-get clean \
  && apt-get autoremove --purge -y \
  && rm -r /var/lib/apt/lists/*
