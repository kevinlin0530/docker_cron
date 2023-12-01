FROM python:3.10
ENV TZ=Asia/Taipei
WORKDIR /app
COPY . .

RUN apt-get update && apt-get -y install cron && apt-get -y install redis-server && \ 
    apt-get install nano && \
    pip install --upgrade pip && \
    pip install -r requirements.txt

COPY hello-cron /etc/cron.d/crontab
# 設置 cron 任務並在 crontab 末尾添加換行
RUN touch /var/log/cron.log && chmod 666 /var/log/cron.log
RUN chmod 0644 /etc/cron.d/crontab && chmod 711 /app/redis_test.py && crontab /etc/cron.d/crontab

RUN export EDITOR=nano && echo "export EDITOR=nano" >> ~/.bashrc

# 在前景運行 cron，創建日誌文件，然後 tail 日誌
CMD service redis-server start && cron && tail -f /var/log/cron.log