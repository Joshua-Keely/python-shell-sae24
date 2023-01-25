#!/bin/bash
sudo dnf install figlet -y --quiet
clear
# menu
function menu {
    figlet sae24
    echo "Bonjour, choisissez une action:

1) Installation complete                                    
2) Installation des paquets                                
3) Configuration de la BDD
4) Install Prometheus     
5) Installation node_exporter
6) Installation Grafana
7) Configuration du reverse proxy
8) Exit
"
    read -p "Votre choix: " n1
}

# Packages 
function lamp_install {
    sudo dnf install httpd -y --quiet
    sudo dnf install php-curl php-gd php-intl php-json php-mbstring php-xml php-zip -y --quiet
    sudo dnf install mariadb-server -y --quiet
    sudo dnf install python -y --quiet

    # Main
    sudo systemctl start mariadb
    sudo systemctl enable mariadb
    sudo systemctl start httpd
    sudo systemctl enable httpd
    # Firewall 
    firewall-cmd --add-service=http --permanent
    firewall-cmd --add-port=80/tcp --permanent
    firewall-cmd --reload
}
function config_database {
   mysql -Bse "CREATE DATABASE sae24; USE sae24; CREATE USER 'sae24user'@'localhost' IDENTIFIED BY 'sae24'; GRANT ALL PRIVILEGES ON sae24.* TO 'sae24user'@'localhost'; CREATE TABLE temperatures (timestamp BIGINT PRIMARY KEY, value FLOAT); CREATE TABLE test (timestamp BIGINT PRIMARY KEY, value FLOAT); QUIT;"
echo "Database configured"
}

function install_prometheus {
   # User & Group creation for Prometheus
   useradd -m -s /bin/false prometheus
   # Ceating config dir for Prometheus
   mkdir /etc/prometheus
   mkdir /var/lib/prometheus
   chown prometheus /var/lib/prometheus
   # Downloading Prometheus tar file
   dnf install wget -y
   wget https://github.com/prometheus/releases/download/v2.14.0/prometheus-2.14.0.linux-amd64.tar.gz -P /tmp
   cd /tmp
   tar -zxpvf prometheus-2.14.0.linux-amd64.tar.gz
   cd prometheus-2.14.0.linux-amd64.tar.gz
   cp prometheus /usr/local/bin
   cp promtool /usr/local/bin
   cd
   # Creating config file for Prometheus
   touch /etc/prometheus/prometheus.yml
   echo "
#Global config

global:
  scrape_interval:     15s
  evaluation_interval: 15s
  scrape_timeout: 15s
scrape_configs:
  - job_name: 'prometheus'
    static_configs:

    - targets: ['localhost:9090']
  - job_name: 'node_exporter'
    static_configs:
    - targets: ['localhost:9100']" > /etc/prometheus/prometheus.yml
   firewall-cmd --add-port=9090/tcp --permanent
   firewall-cmd --reload
   #Creating systemd service file for Prometheus
   touch /etc/systemd/system/prometheus.service
   echo "
[Unit]
Description=Prometheus Time Series Collection and Processing Server
Wants=network-online.target
After=network-online.target
   
[Service]
User=prometheus
Group=prometheus
Type=simple
ExecStart=/usr/local/bin/prometheus \
    --config.file /etc/prometheus/prometheus.yml \
    --storage.tsdb.path /var/lib/prometheus/ \
    --web.console.templates=/etc/prometheus/consoles \
    --web.console.libraries=/etc/prometheus/console_libraries

[Install]
   
WantedBy=multi-user.target" > /etc/systemd/system/prometheus.service
   systemctl daemon-reload
   # Start & Enable Prometheus
   systemctl start prometheus
   systemctl enable prometheus
   # Check
   systemctl status prometheus
   netstat -tunlp
   echo "Check prometheus is running in your browser: http://localhost:9090"
  }

function install_node {
   useradd -m -s /bin/false node_exporter
   wget https://github.com/prometheus/node_exporter/releases/download/v0.18.1.linux-amd64.tar.gz
   tar -zxpvf node_exporter-0.18.1.linux-amd64.tar.gz
   cp node_exporter-0.18.1.linux-amd64/node_exporter /usr/local/bin
   chown node_exporter:node_exporter /usr/local/bin/node_exporter
   touch /etc/systemd/system/node_exporter.service
   echo "
[Unit]
Description=Prometheus Node Exporter
Wants=network-online.target
After=network-online.target

[Service]
User=node_exporter
Group=node_exporter
Type=simple
ExecStart=/usr/local/bin/node_exporter

[Install]
WantedBy=multi-user.target" > /etc/systemd/system/node_exporter.service
   systemctl daemon-reload
   systemctl start node_exporter
   systemctl enable node_exporter
   firewall-cmd --add-port=9100/tcp --permanent
   firewall-cmd --reload
   systemctl restart prometheus
}

function install_grafana {
   dnf install grafana -y --quiet
   systemctl daemon-reload
   systemctl start grafana-server
   systemctl enable grafana-server
   firewall-cmd --add-port=3000/tcp --permanent
   firewall-cmd --reload
   echo "Access Grafana dashboard: http://localhost:3000 Login: admin Pass: admin"
}

function config_reverse {
   touch /etc/httpd/conf.d/grafana.conf
   cp /etc/httpd/conf.d /etc/httpd/conf.d.ori
   rm -f /etc/httpd/conf.d/autoindex.conf
   echo "
ProxyPass /grafana http://localhost:3000
ProxyPassReverse /grafana http://localhost:3000
ProxyPreserveHost On" > /etc/httpd/conf.d/grafana.conf
   replace "root_url = %(protocol)s://%(domain)s:%(http_port)s" "root_url = %(protocol)s://%(domain)s:%(http_port)s/grafana" -- /etc/grafana/grafana.ini
}

for (( ; ;))
do
       	clear 
	menu
	if [ $n1 == 1 ]
	then
	   lamp_install
	   config_database
	   install_grafana
	   config_reverse
	   sleep 2s
	   clear
	fi

	if [ $n1 == 2 ]
	then 
	   lamp_install
	   sleep 2s
	   clear
	fi

	if [ $n1 == 3 ]
	then
	   config_database
	   sleep 2s
	   clear
	fi

	if [ $n1 == 4 ]
	then 
	   install_prometheus
	   sleep 2s
	   clear
	fi 

	if [ $n1 == 5 ]
	then
	   install_node
	   sleep 2s 
	   clear 
	fi 

	if [ $n1 == 6 ]
	then
	   install_grafana
	   sleep 2s
	   clear
	fi

	if [ $n1 == 7 ]
	then
	   config_reverse
	   sleep 2s
	   clear
	fi
	if [ $n1 == 8 ]
	then
   	   clear
   	   echo "goodbye"
	   exit
	fi
done

