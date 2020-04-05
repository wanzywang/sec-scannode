FROM python:3.8-alpine
MAINTAINER yourname youremai@mail.com
RUN sed -i 's/dl-cdn.alpinelinux.org/mirrors.aliyun.com/g' /etc/apk/repositories
RUN apk add make gcc  musl-dev libffi-dev openssl-dev git vim
# 设置时区为上海
RUN apk add tzdata && cp /usr/share/zoneinfo/Asia/Shanghai /etc/localtime \
    && echo "Asia/Shanghai" > /etc/timezone
RUN mkdir /xn-secnode && mkdir /xn-secnode/logs && rm -rf /xn-secnode/*
WORKDIR /xn-secnode
LABEL ver=1.5.1
RUN git clone https://github.com/sec-scannode.git /xn-secnode/
RUN pip install -r requirements.txt -i https://pypi.tuna.tsinghua.edu.cn/simple
RUN echo "* * * * * root find /xn-secnode/logs -name 'xnsec.log*' -and -mtime +10 -type f |xargs rm -f" >>/etc/crontabs/root
RUN chmod a+x /xn-secnode/node_run.sh

ENV REDIS_ENV=0:pass811220@localhost:6379
ENV HEART_RATE=60

CMD ["sh","-c", "/xn-secnode/node_run.sh"]

