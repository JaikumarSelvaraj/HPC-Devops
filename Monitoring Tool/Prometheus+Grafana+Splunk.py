					Grafanna and Prometheus
					
Devops what are things, it will automate -> Build , Test and Deploy.

Splunk -> Mainly used to monitor log.

Prometheus  -> Metrics  (CPU,Memory,Disk) -> TSDB -> Time Series Database -> 600 to 700 Metrics can be able to measure

SCRAPEINTRAVEL -> 

Node Exporter ->

CloudWatch -> We can use only AWS. Observer only few metrics.

Grafanna -> Mainly used for creating Dashboard



--------------------------------------------------------------------------------------------------------------------
				Prometheus - 2 (Time Series database)
				
Create Two Instances

Prometheus & Node_Exporter

Prometheus.io

Dashboard + Metrics

Query + PromQL

Download and extract file

./prometheus --config.file=prometheus.yml (Configuration file specified below)

host:9090/query -> Splunk(port no : 8000)

nodeexported -> 9100

clienetnode:9100/metrics

Change the parrent Configuration file .yml with new node


nohup ./node_exporter &

node_cpu_seconds_total (Collecting node_exporter file data)

Status -> Target Health -> we can able to see list of host are added

Prometheus  -> able to visualize lower standard + collect metrics
Node Exporter -> Only collect the metrics.


--------------------------------------------------------------------------------------------------------------------
Configuration file

scrape_configs:
  # The job name is added as a label `job=<job_name>` to any timeseries scraped from this config.
  - job_name: "prometheus"

    # metrics_path defaults to '/metrics'
    # scheme defaults to 'http'.

    static_configs:
      - targets: ["localhost:9090"]
       # The label name is added as a label `label_name=<label_value>` to any timeseries scraped from this config.
        labels:
          app: "prometheus"
    scrape_native_histograms: true

  # The job name is added as a label `job=<job_name>` to any timeseries scraped from this config.
  - job_name: "HDFC"

    # metrics_path defaults to '/metrics'
    # scheme defaults to 'http'.

    static_configs:
      - targets: ["47.131.248.237:9100"]
       # The label name is added as a label `label_name=<label_value>` to any timeseries scraped from this config.
        labels:
          app: "HDFC"
    #scrape_native_histograms: true


--------------------------------------------------------------------------------------------------------------------
			Grafana
			
12.4.3 - Version

Install the package

Port number 3000

Default password -> admin/admin -> set new password

Data Source  -> Prometheus -> Connection : Promethesus server URL 

Create Dashboard -> New Dashboard -> Visualiation -> Promethues 

	Metrics : go_gc_duration_seconds Job :2 (localhost & HDFC(node exporter)) -> Run Quries -> Save
	
All the metrics doesn't show the two app, some metrics specific to the hosts.
	
if CPU is >60 how will you generate alert


--------------------------------------------------------------------------------------------------------------------
SPLUNK

SDLC -> Software Development Life Cycle

Project
Dev env
Test/QA env
SIT Env
UAT env
Prod env
For all the project we need to have CICD

Cloudwatch -> Metrics (CPU,Memory,Disk,Network)
cloudtrail -> Logs -> Event Mangement

splunk -> SIEM -> security Information & Event management
-----------------------------------------------------------------------------------------------------------------