apt-get install -y nginx redis.server supervisor
mkdir /var/log/ovftool
mkdir /var/tmp/torrents

touch /var/log/ovftool/info.log
touch /var/log/ovftool/debug.log
touch /var/log/ovftool/error.log
touch /var/log/ovftool/method_time.log

mv /root/ovftool-agent/ovf.conf /etc/supervisor/conf.d/