FROM alpine:3

RUN apk update && apk upgrade && apk add --no-cache curl 

WORKDIR /home

COPY cronjob.sh /home/cronjob.sh

RUN chmod +x /home/cronjob.sh

# Copy cron file to the container
COPY cron /etc/cron.d/cron

# Give the permission
RUN chmod 0644 /etc/cron.d/cron
 
# Add the cron job
RUN crontab /etc/cron.d/cron
 
# Link cron log file to stdout
RUN ln -s /dev/stdout /var/log/cron
 
# Run the cron service in the foreground
CMD [ "crond", "-l", "2", "-f" ]