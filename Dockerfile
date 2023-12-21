FROM python:3.10
ENV TZ=Asia/Taipei
WORKDIR /app
COPY . .

RUN apt-get update && apt-get -y install cron && apt-get -y install redis-server && \ 
    apt-get install nano && \
    pip install --upgrade pip && \
    pip install -r requirements.txt
# 先將hello-cron複製到指定的檔案路徑
COPY hello-cron /etc/cron.d/crontab
# 創建cron.log 檔案
RUN touch /var/log/cron.log && chmod 666 /var/log/cron.log
# 第一步先開啟 crontab 檔案權限，第二步 開啟 redis_test 檔案權限，第三步 執行crontab 指令
RUN chmod 0644 /etc/cron.d/crontab && chmod 711 /app/redis_test.py && crontab /etc/cron.d/crontab
# 設定nano 為設定指令並設置路徑
RUN export EDITOR=nano && echo "export EDITOR=nano" >> ~/.bashrc

# 在前景運行 cron，創建日誌文件，然後 tail 日誌
CMD service redis-server start && cron && tail -f /var/log/cron.log