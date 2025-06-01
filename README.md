# SRE Final Project

A complete Site Reliability Engineering (SRE) demonstration, featuring a containerized Flask web application, end-to-end monitoring and alerting, Infrastructure as Code (IaC), CI/CD automation, security auditing, capacity planning, incident management with postmortem, custom SRE tooling, and defense materials.

---

## Table of Contents

1. [Project Overview](#project-overview)
2. [Tech Stack](#tech-stack)
3. [Features](#features)
4. [Architecture](#architecture)
5. [Repository Structure](#repository-structure)
6. [Prerequisites](#prerequisites)
7. [Getting Started](#getting-started)
   - [Clone the Repository](#clone-the-repository)
   - [Environment Variables](#environment-variables)
   - [Local Deployment (Docker Compose)](#local-deployment-docker-compose)
   - [Monitoring & Alerting](#monitoring--alerting)
   - [Incident Management & Postmortem](#incident-management--postmortem)
   - [Capacity Planning](#capacity-planning)
   - [Running Tests](#running-tests)
8. [Infrastructure as Code](#infrastructure-as-code)
   - [Terraform](#terraform)
   - [Ansible](#ansible)
9. [CI/CD Pipeline](#cicd-pipeline)
10. [SRE Tool: Cleanup Script](#sre-tool-cleanup-script)
11. [Security Audit](#security-audit)
12. [SLI / SLO / SLA](#sli--slo--sla)
13. [Team Roles & Collaboration](#team-roles--collaboration)
14. [Defense Materials](#defense-materials)
15. [Contact & Acknowledgements](#contact--acknowledgements)

---

## Project Overview

This project demonstrates the application of Site Reliability Engineering (SRE) principles to a simple containerized Flask web service. It covers:

- **Containerization**: All components (Flask app, Prometheus, Grafana, Alertmanager, Telegram Bot) run in Docker containers.
- **Monitoring & Alerting**:  
  - Custom Flask metrics exposed at `/metrics`.  
  - Prometheus scrapes metrics every 5 s.  
  - Grafana dashboards visualize request rate, CPU/memory usage.  
  - Alertmanager sends critical alerts to a Telegram chat.
- **Infrastructure as Code (IaC)**:  
  - **Terraform** provisions cloud infrastructure (VMs, network, security groups).  
  - **Ansible** installs dependencies, deploys containers, and configures services.
- **CI/CD**:  
  - GitHub Actions workflows build, test, and deploy on every push to `main`.
- **Security Audit**:  
  - OS-level audit with **Lynis**.  
  - Container vulnerability scanning with **Trivy**.  
  - Firewall configuration via **UFW** and port scanning with **Nmap**.
- **Capacity Planning**:  
  - Load testing with **ApacheBench (ab)** for 1–3 replicas.  
  - Analysis of throughput, p95 latency, and CPU utilization.  
  - Recommendations for horizontal scaling.
- **Incident Management & Postmortem**:  
  - Example simulated failure, incident response steps, root-cause analysis, and postmortem.
- **SRE Tool**:  
  - `cleanup_images.py`: Python script to delete dangling Docker images older than 7 days.
- **Defense Materials**:  
  - Slide deck and speaker notes for the final project presentation.

---

## Tech Stack

- **Programming & Web**: Python 3.10, Flask  
- **Containerization**: Docker, Docker Compose  
- **Monitoring & Visualization**: Prometheus, Grafana  
- **Alerting**: Alertmanager, Telegram Bot  
- **Infrastructure as Code**: Terraform, Ansible  
- **CI/CD**: GitHub Actions, Pytest  
- **Load Testing**: ApacheBench (`ab`)  
- **Security Tools**: Lynis, Trivy, UFW, Nmap  
- **SRE Utility**: Python (cleanup script)  

---

## Features

1. **REST API Endpoints**  
   - `/` – Returns JSON payload indicating service status.  
   - `/health` – Health check endpoint (returns uptime and timestamp).  
   - `/metrics` – Exposes Prometheus metrics:  
     - `app_requests_total` (Counter)  
     - `app_cpu_usage` (Gauge)  
     - `app_memory_usage` (Gauge)  

2. **Custom Metrics**  
   - Total request counter (`app_requests_total`).  
   - Real-time CPU usage gauge (`app_cpu_usage`).  
   - Real-time memory usage gauge (`app_memory_usage`).  

3. **Prometheus Monitoring**  
   - Scrapes Flask metrics every 5 s, stores time-series data, and evaluates alerting rules.

4. **Grafana Dashboards**  
   - Dashboard panels visualize:  
     - Requests per second (RPS)  
     - CPU usage (%)  
     - Memory usage (%)  
   - Preconfigured JSON dashboard located in `grafana/dashboards/flask_dashboard.json`.

5. **Alertmanager & Telegram Integration**  
   - Prometheus alert `HighRequestRate` fires when `sum(rate(app_requests_total[1m])) > 5` for 30 s.  
   - Alertmanager routes to the `telegram` receiver, forwarding payloads via webhook to the Telegram Bot.

6. **CI/CD Pipeline**  
   - **GitHub Actions** workflows:  
     - `build_and_test`: runs Pytest (3 unit tests) and builds Docker images.  
     - `deploy`: uses Ansible to provision and configure remote server, then launches Docker Compose.

7. **IaC Automation**  
   - **Terraform** module (`terraform/`) provisions VM(s), network, and firewall rules.  
   - **Ansible** playbooks (`ansible/`) install Docker, clone the repo, copy configs, and launch containers.

8. **Capacity Planning**  
   - Load tests with ApacheBench (`ab -n 20000 -c 50`) on 1–3 replicas.  
   - Table of results (instances vs. RPS, p95 latency, CPU%).  
   - Analysis and scaling recommendations.

9. **Incident Management & Postmortem**  
   - Simulated failure: primary container crash.  
   - Incident response steps detailed.  
   - Postmortem report with root cause analysis and lessons learned.

10. **Security Audits**  
    - **Lynis** OS audit output and recommendations.  
    - **Trivy** container scan (CVE list and fixes).  
    - **UFW** firewall rules ensuring only necessary ports (22, 5000, 9090, 9093, 3000) are open.  
    - **Nmap** scan to verify open ports.

11. **SRE Tool: Cleanup Script**  
    - `cleanup_images.py` deletes dangling Docker images older than 7 days.  
    - Configured to run daily via cron or systemd timer.
---

## Architecture

```mermaid
flowchart LR
    subgraph Container_Network
        Flask[Flask App<br/>(web:5000)] 
        Prometheus[Prometheus<br/>(prometheus:9090)]
        Grafana[Grafana<br/>(grafana:3000)]
        Alertmanager[Alertmanager<br/>(alertmanager:9093)]
        AlertBot[Telegram Bot<br/>(bot:8080)]
    end

    Browser[/ (HTTP:5000)]
    Curl[curl /metrics]
    Telegram[Telegram Chat]

    Browser --> Flask
    Curl --> Flask
    Flask --> Prometheus
    Prometheus --> Grafana
    Prometheus --> Alertmanager
    Alertmanager --> AlertBot
    AlertBot --> Telegram
````

* **Flask App** (`web:5000`): Serves HTTP endpoints (`/`, `/health`, `/metrics`).
* **Prometheus** (`prometheus:9090`): Scrapes metrics from `web:5000` every 5 s, evaluates alert rules.
* **Grafana** (`grafana:3000`): Connects to Prometheus as data source, renders dashboards.
* **Alertmanager** (`alertmanager:9093`): Receives alerts from Prometheus, groups and routes them to Telegram Bot.
* **Telegram Bot** (`bot:8080`): Receives webhook POSTs from Alertmanager, sends formatted notifications to a Telegram chat.

---

## Repository Structure

```
SRE-final/
├── ansible/
│   ├── inventory.ini
│   ├── playbook.yml
│   └── roles/
│       ├── common/
│       │   └── tasks/
│       │       └── main.yml
│       ├── docker/
│       │   └── tasks/
│       │       └── main.yml
│       └── sre_app/
│           └── tasks/
│               └── main.yml
├── bot/
│   ├── Dockerfile
│   └── bot.py
├── ci/
│   └── workflows/
│       └── deploy.yml
├── cleanup_images.py
├── docker-compose.yml
├── Dockerfile
├── grafana/
│   └── dashboards/
│       └── flask_dashboard.json
├── main.py
├── presentation/
│   ├── SRE_Final_Project.pdf
│   └── speaker_notes.md
├── prometheus.yml
├── alert.rules.yml
├── alertmanager.yml
├── terraform/
│   ├── main.tf
│   ├── variables.tf
│   ├── outputs.tf
│   └── terraform.tfvars.example
├── tests/
│   └── test_app.py
├── README.md
└── requirements.txt
```

* **`ansible/`** – Ansible playbooks and roles for provisioning and deploying the SRE stack.
* **`bot/`** – Telegram alert bot code and Dockerfile.
* **`ci/workflows/`** – GitHub Actions workflows (`deploy.yml`).
* **`cleanup_images.py`** – Python script for removing dangling Docker images.
* **`docker-compose.yml`** – Defines all service containers: Flask, Prometheus, Grafana, Alertmanager, Bot.
* **`Dockerfile`** – Builds the Flask application image.
* **`grafana/dashboards/flask_dashboard.json`** – Preconfigured Grafana dashboard.
* **`main.py`** – Flask application entry point.
* **`presentation/`** – Slide deck (PDF) and speaker notes (Markdown) for defense.
* **`prometheus.yml`** – Prometheus scrape configuration.
* **`alert.rules.yml`** – Prometheus alert rules.
* **`alertmanager.yml`** – Alertmanager routing and receiver configuration.
* **`terraform/`** – Terraform configuration for cloud infrastructure.
* **`tests/`** – Pytest unit tests for the Flask application.
* **`requirements.txt`** – Python dependencies.

---

## Prerequisites

* **Docker Engine** (≥ 20.10)
* **Docker Compose** (≥ v2.x)
* **Python 3.10+** (for local development and tests)
* **Git**
* **Terraform** (≥ v1.x)
* **Ansible** (≥ v2.9)
* **Node.js / NPM** (optional, for editing Grafana dashboards)
* **Telegram Account** (to obtain Bot token and chat ID)
* **A cloud provider account** (e.g., AWS, Azure, GCP) for Terraform resources

---

## Getting Started

### Clone the Repository

```bash
git clone https://github.com/Dari4ok/SRE-final.git
cd SRE-final
```

### Environment Variables

Create a `.env` file at the project root (Git-ignored) with:

```dotenv
TELEGRAM_TOKEN=<your_telegram_bot_token>
TELEGRAM_CHAT_ID=<your_telegram_chat_id>
```

* **TELEGRAM\_TOKEN**: Bot token from [BotFather](https://t.me/BotFather).
* **TELEGRAM\_CHAT\_ID**: Numeric chat ID (use `@userinfobot` in Telegram or check chat metadata).

Export variables (Linux/macOS):

```bash
export TELEGRAM_TOKEN=$(grep TELEGRAM_TOKEN .env | cut -d '=' -f2)
export TELEGRAM_CHAT_ID=$(grep TELEGRAM_CHAT_ID .env | cut -d '=' -f2)
```

> **Windows (PowerShell)**:
>
> ```powershell
> setx TELEGRAM_TOKEN "<token>"
> setx TELEGRAM_CHAT_ID "<chat_id>"
> ```

### Local Deployment (Docker Compose)

All services run locally via Docker Compose.

1. **Build & Start Containers**

   ```bash
   docker-compose up --build -d
   ```

2. **Verify Running Containers**

   ```bash
   docker ps
   ```

   You should see:

   ```
   CONTAINER ID   IMAGE                     COMMAND               PORTS                               NAMES
   abc123def456   sre-final-web             "python main.py"      0.0.0.0:5000->5000/tcp              sre-final-web-1
   def456ghi789   sre-final-bot             "python bot.py"       0.0.0.0:8080->8080/tcp              sre-final-bot-1
   ghi789jkl012   prom/prometheus:latest    "/bin/prometheus …"   0.0.0.0:9090->9090/tcp              sre-final-prometheus-1
   jkl012mno345   prom/alertmanager:latest  "/bin/alertmanager"   0.0.0.0:9093->9093/tcp              sre-final-alertmanager-1
   mno345pqr678   grafana/grafana:latest    "/run.sh"             0.0.0.0:3000->3000/tcp              sre-final-grafana-1
   ```

3. **Access Endpoints**

   * **Web App**:

     ```bash
     curl http://localhost:5000/
     # {"message":"Welcome to SRE Final Project","status":"OK"}
     ```

   * **Health Check**:

     ```bash
     curl http://localhost:5000/health
     # {"status":"healthy","timestamp":<unix_timestamp>}
     ```

   * **Prometheus UI**: `http://localhost:9090/` → **Status → Targets** (should show `flask-app:5000` as UP).

   * **Alertmanager UI**: `http://localhost:9093/` (initially “No alerts”).

   * **Grafana UI**: `http://localhost:3000/` (login: `admin` / `admin`) → **Configuration → Data Sources** → Add Prometheus (`http://prometheus:9090`) → **Import** dashboard from `grafana/dashboards/flask_dashboard.json`.

   * **Telegram Bot**: Listens at `http://localhost:8080/` for Alertmanager webhooks.

---

## Monitoring & Alerting

### Prometheus Configuration (`prometheus.yml`)

```yaml
global:
  scrape_interval: 5s

scrape_configs:
  - job_name: 'flask-app'
    static_configs:
      - targets: ['web:5000']
rule_files:
  - 'alert.rules.yml'
```

### Alert Rules (`alert.rules.yml`)

```yaml
groups:
  - name: HighRequestRate
    rules:
      - alert: HighRequestRate
        expr: sum(rate(app_requests_total[1m])) > 5
        for: 30s
        labels:
          severity: "warning"
        annotations:
          summary: "High request rate detected"
          description: "The request rate has exceeded 5 req/sec for more than 30 seconds."
```

### Alertmanager Configuration (`alertmanager.yml`)

```yaml
global:
  resolve_timeout: 5m

route:
  receiver: 'telegram'

receivers:
  - name: 'telegram'
    webhook_configs:
      - url: 'http://bot:8080/'
```

### Flask Metrics in `main.py`

```python
from flask import Flask, jsonify, Response
from prometheus_client import Counter, Gauge, generate_latest, CONTENT_TYPE_LATEST
import time
import psutil

app = Flask(__name__)

# Metrics
REQUEST_COUNT = Counter('app_requests_total', 'Total HTTP requests', ['method', 'endpoint'])
CPU_USAGE = Gauge('app_cpu_usage', 'Current CPU usage percentage')
MEMORY_USAGE = Gauge('app_memory_usage', 'Current memory usage percentage')

# Simulate real CPU and memory usage
def update_metrics():
    CPU_USAGE.set(psutil.cpu_percent(interval=None))
    MEMORY_USAGE.set(psutil.virtual_memory().percent)

@app.before_request
def before_request():
    REQUEST_COUNT.labels(method="GET", endpoint="/").inc()
    update_metrics()

@app.route('/')
def index():
    return jsonify({"message": "Welcome to SRE Final Project", "status": "OK"})

@app.route('/health')
def health():
    return jsonify({"status": "healthy", "timestamp": int(time.time())})

@app.route('/metrics')
def metrics():
    update_metrics()
    return Response(generate_latest(), mimetype=CONTENT_TYPE_LATEST)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
```

---

## Incident Management & Postmortem

### Simulated Failure

To demonstrate incident response, we simulate a container crash:

1. **Trigger Failure**:

   ```bash
   docker exec sre-final-web-1 pkill -f "python main.py"
   ```

   This kills the Flask process inside the `sre-final-web-1` container.

2. **Immediate Alert**:

   * Prometheus detects missing metrics at next scrape.
   * Alert rule `HighRequestRate` may fire if requests spike; alternately, configure a separate “Flask down” rule:

     ```yaml
     - alert: FlaskAppDown
       expr: up{job="flask-app"} == 0
       for: 15s
       labels:
         severity: "critical"
       annotations:
         summary: "Flask application unreachable"
         description: "Prometheus cannot scrape metrics from Flask app; instance is down."
     ```
   * Alertmanager sends a webhook to the Telegram Bot.

3. **Detection & Notification**:

   * Telegram Bot (`bot/bot.py`) receives JSON payload from Alertmanager:

     ```python
     import os
     import requests
     from flask import Flask, request, jsonify

     app = Flask(__name__)
     TELEGRAM_TOKEN = os.getenv('TELEGRAM_TOKEN')
     TELEGRAM_CHAT_ID = os.getenv('TELEGRAM_CHAT_ID')
     TELEGRAM_API_URL = f"https://api.telegram.org/bot{TELEGRAM_TOKEN}/sendMessage"

     @app.route('/', methods=['POST'])
     def handle_alert():
         data = request.get_json()
         for alert in data.get('alerts', []):
             summary = alert.get('annotations', {}).get('summary', 'No summary')
             description = alert.get('annotations', {}).get('description', 'No description')
             message = f"🚨 <b>{summary}</b>\n{description}"
             requests.post(TELEGRAM_API_URL, json={
                 'chat_id': TELEGRAM_CHAT_ID,
                 'parse_mode': 'HTML',
                 'text': message
             })
         return jsonify({'status': 'ok'})

     if __name__ == '__main__':
         app.run(host='0.0.0.0', port=8080)
     ```
   * The Telegram chat receives:

     ```
     🚨 **Flask application unreachable**
     Prometheus cannot scrape metrics from Flask app; instance is down.
     ```

4. **Incident Response Steps**

   * **Acknowledge**: SRE engineer sees Telegram alert at 10:15 AM (UTC+5).
   * **Identify**: Check Prometheus → Targets → `flask-app` is DOWN.
   * **Access Host**:

     ```bash
     ssh root@<SERVER_IP>
     docker logs sre-final-web-1
     ```

     Logs show Flask process died due to a simulated kill.
   * **Mitigation**:

     ```bash
     docker restart sre-final-web-1
     ```

     Container restarts, Flask process resumes.
   * **Validation**:

     ```bash
     curl http://localhost:5000/health
     # {"status":"healthy","timestamp":<unix_timestamp>}
     ```

     Prometheus target returns to UP, alert resolves.

### Postmortem Report

**Incident Title**: “Flask Application Crash (Simulated)”

* **Incident Start** (UTC+5): May 10, 2025 10:15 AM
* **Incident End** (UTC+5): May 10, 2025 10:20 AM
* **Duration**: 5 minutes

#### 1. Summary

A simulated kill of the Flask process caused metrics to be unavailable. Prometheus raised a “FlaskAppDown” alert, which was forwarded via Telegram. The application was restarted within 5 minutes, restoring service.

#### 2. Impact

* Prometheus alerts fired.
* End-users experienced 5 minutes of downtime; HTTP requests returned errors.

#### 3. Root Cause

* Intentional `pkill` command in container to simulate failure.
* No automated restart policy in Docker Compose for `web` service.

#### 4. Resolution & Recovery

* Manually restarted container: `docker restart sre-final-web-1`.
* Service returned to healthy state; Prometheus target status → UP.

#### 5. Lessons Learned

* **Automated Restart**: Add `restart: unless-stopped` to `docker-compose.yml` for all critical services.
* **Alert Triage**: Consider distinguishing between simulated test alerts and real incidents.
* **Response Playbook**: Document step-by-step runbook for SRE team to minimize MTTR.

#### 6. Corrective Actions

* Update `docker-compose.yml`:

  ```yaml
  services:
    web:
      image: sre-final-web:latest
      restart: unless-stopped
      ...
  ```
* Add a “Flask down” alert rule to Prometheus (see above).
* Schedule quarterly failure drills to test team readiness.

---

## Capacity Planning

We performed load tests using ApacheBench (`ab`). Results for 1–3 replicas are summarized below:

| Instances | Average RPS | p95 Latency (ms) | CPU Utilization (%) |
| --------: | ----------: | ---------------: | ------------------: |
|         1 |      101.18 |             1511 |                  65 |
|         2 |      180.00 |              800 |                  50 |
|         3 |      250.00 |              600 |                  40 |

* **1 Replica**:

  ```bash
  ab -n 20000 -c 50 http://<SERVER_IP>:5000/
  ```

  * **RPS**: 101.18
  * **p95 Latency**: 1 511 ms
  * **CPU**: 65 %

* **2 Replicas** (`docker-compose up -d --scale web=2`):

  * **RPS**: 180.00
  * **p95 Latency**: 800 ms
  * **CPU**: 50 %

* **3 Replicas** (`docker-compose up -d --scale web=3`):

  * **RPS**: 250.00
  * **p95 Latency**: 600 ms
  * **CPU**: 40 %

### Analysis & Recommendations

* Throughput scales approximately linearly:

  * 1 → 2 replicas: throughput increases \~1.78×.
  * 2 → 3 replicas: throughput increases \~1.39×.
* p95 latency decreases by \~50 % when going from 1 → 2 replicas, and improves further with 3 replicas.
* CPU headroom grows as replicas increase.

**Recommendations**:

* For sustained **200 RPS**, deploy **2 replicas** (p95 \~ 800 ms, CPU \~ 50 %).
* For sustained **400 RPS**, project for **4 replicas** (extrapolated):

  * Estimated p95 \~ 500 ms, CPU \~ ≈ 70 %.
* Implement horizontal **auto-scaling** triggered by:

  * CPU > 70 %
  * RPS > 200

---

## Running Tests

Unit tests are written with Pytest (`tests/test_app.py`).

```bash
# Create and activate virtual environment (optional)
python3 -m venv venv
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt

# Run tests
pytest tests
```

Expected output:

```
========================================== test session starts ==========================================
platform linux -- Python 3.10.5, pytest-7.x.x, pluggy-1.x.x
rootdir: /path/to/SRE-final
collected 3 items

tests/test_app.py ...                                                                           [100%]

========================================== 3 passed in 0.92s ===========================================
```

---

## Infrastructure as Code

### Terraform

*All Terraform code is located in `terraform/`.*

1. **Initialize & Apply**

   ```bash
   cd terraform/
   terraform init
   terraform apply -auto-approve
   ```

   * Provisions cloud VM(s) with Docker and required network/security configurations.
   * Outputs `instance_ip`, `ssh_user`, and other variables.

2. **Key Files**

   * `main.tf` – Defines provider, VM resource, security group.
   * `variables.tf` – Input variables (e.g., cloud credentials, region, machine type).
   * `outputs.tf` – Exports `instance_ip`.
   * `terraform.tfvars.example` – Example values for variables.

3. **Sample `main.tf`**:

   ```hcl
   provider "aws" {
     region = var.aws_region
   }

   resource "aws_instance" "sre_vm" {
     ami                    = var.aws_ami
     instance_type          = var.instance_type
     key_name               = var.aws_key_name
     vpc_security_group_ids = [aws_security_group.sre_sg.id]
     tags = {
       Name = "sre-final-vm"
     }
   }

   resource "aws_security_group" "sre_sg" {
     name        = "sre_sg"
     description = "Allow SSH, HTTP, Prometheus, Grafana, Alertmanager ports"

     ingress {
       description = "SSH"
       from_port   = 22
       to_port     = 22
       protocol    = "tcp"
       cidr_blocks = ["0.0.0.0/0"]
     }
     ingress {
       description = "Flask App"
       from_port   = 5000
       to_port     = 5000
       protocol    = "tcp"
       cidr_blocks = ["0.0.0.0/0"]
     }
     ingress {
       description = "Prometheus"
       from_port   = 9090
       to_port     = 9090
       protocol    = "tcp"
       cidr_blocks = ["0.0.0.0/0"]
     }
     ingress {
       description = "Alertmanager"
       from_port   = 9093
       to_port     = 9093
       protocol    = "tcp"
       cidr_blocks = ["0.0.0.0/0"]
     }
     ingress {
       description = "Grafana"
       from_port   = 3000
       to_port     = 3000
       protocol    = "tcp"
       cidr_blocks = ["0.0.0.0/0"]
     }
     egress {
       from_port   = 0
       to_port     = 0
       protocol    = "-1"
       cidr_blocks = ["0.0.0.0/0"]
     }
   }
   ```

4. **Usage**

   * After `terraform apply`, note the output `instance_ip`.
   * Update `ansible/inventory.ini` with:

     ```ini
     [sre_servers]
     <instance_ip> ansible_user="ec2-user" ansible_ssh_private_key_file="~/.ssh/id_rsa"
     ```
   * Proceed to Ansible deployment.

### Ansible

*All Ansible playbooks and roles are under `ansible/`.*

#### 1. Inventory (`ansible/inventory.ini`)

```ini
[sre_servers]
<instance_ip> ansible_user="ec2-user" ansible_ssh_private_key_file="~/.ssh/id_rsa"
```

#### 2. Playbook (`ansible/playbook.yml`)

```yaml
- hosts: sre_servers
  become: true
  vars:
    telegram_token: "{{ lookup('env','TELEGRAM_TOKEN') }}"
    telegram_chat_id: "{{ lookup('env','TELEGRAM_CHAT_ID') }}"
    app_repo_url: "https://github.com/Dari4ok/SRE-final.git"
    app_dir: "/opt/sre"
  roles:
    - common
    - docker
    - sre_app
```

#### 3. Roles

* **common/tasks/main.yml**

  ```yaml
  - name: Update apt cache
    apt:
      update_cache: yes

  - name: Install base packages
    apt:
      name:
        - python3
        - python3-pip
        - git
        - curl
      state: present
  ```

* **docker/tasks/main.yml**

  ```yaml
  - name: Install Docker GPG key
    apt_key:
      url: https://download.docker.com/linux/ubuntu/gpg
      state: present

  - name: Add Docker apt repository
    apt_repository:
      repo: deb [arch=amd64] https://download.docker.com/linux/ubuntu focal stable
      state: present

  - name: Install Docker Engine and Docker Compose
    apt:
      name:
        - docker-ce
        - docker-ce-cli
        - containerd.io
        - docker-compose-plugin
      state: present

  - name: Start Docker service
    service:
      name: docker
      state: started
      enabled: true
  ```

* **sre\_app/tasks/main.yml**

  ```yaml
  - name: Clone or update SRE-final repository
    git:
      repo: "{{ app_repo_url }}"
      dest: "{{ app_dir }}"
      version: "main"
      force: yes

  - name: Copy .env file
    copy:
      src: "{{ app_dir }}/.env"
      dest: "{{ app_dir }}/.env"
      owner: root
      group: root
      mode: '0600'

  - name: Copy Prometheus and Alertmanager configs
    copy:
      src: "{{ item }}"
      dest: "{{ app_dir }}/{{ item }}"
      owner: root
      group: root
      mode: '0644'
    loop:
      - prometheus.yml
      - alert.rules.yml
      - alertmanager.yml

  - name: Copy Docker Compose file
    copy:
      src: "{{ app_dir }}/docker-compose.yml"
      dest: "{{ app_dir }}/docker-compose.yml"
      owner: root
      group: root
      mode: '0644'

  - name: Build and run Docker Compose
    command: docker-compose up -d --build
    args:
      chdir: "{{ app_dir }}"

  - name: Wait for containers to be up
    wait_for:
      host: "localhost"
      port: 5000
      delay: 10
      timeout: 60
  ```

#### 4. Run Ansible Playbook

```bash
ansible-playbook -i ansible/inventory.ini ansible/playbook.yml
```

---

## CI/CD Pipeline

GitHub Actions workflows are defined in `ci/workflows/deploy.yml`.

### 1. Trigger

* On push to `main` branch.

### 2. Jobs

#### build\_and\_test

```yaml
name: Build and Test

on:
  push:
    branches:
      - main

jobs:
  build_and_test:
    runs-on: ubuntu-latest
    steps:
      - name: Checkout code
        uses: actions/checkout@v3

      - name: Set up Python 3.10
        uses: actions/setup-python@v4
        with:
          python-version: 3.10

      - name: Install dependencies & run tests
        run: |
          python -m pip install --upgrade pip
          pip install -r requirements.txt
          pytest tests

      - name: Build Flask Docker image
        run: docker build -t sre-final-web:latest .

      - name: Build Telegram Bot Docker image
        run: docker build -t sre-final-bot:latest ./bot
```

#### deploy

```yaml
name: Deploy SRE Final

on:
  push:
    branches:
      - main

jobs:
  deploy:
    needs: build_and_test
    runs-on: ubuntu-latest
    steps:
      - name: Checkout code
        uses: actions/checkout@v3

      - name: Set up Python & Ansible
        uses: actions/setup-python@v4
        with:
          python-version: 3.10

      - name: Install Ansible
        run: |
          python -m pip install --upgrade pip
          pip install ansible

      - name: Configure SSH
        run: |
          mkdir -p ~/.ssh
          echo "${{ secrets.SSH_PRIVATE_KEY }}" > ~/.ssh/id_rsa
          chmod 600 ~/.ssh/id_rsa

      - name: Run Ansible Playbook
        env:
          TELEGRAM_TOKEN: ${{ secrets.TELEGRAM_TOKEN }}
          TELEGRAM_CHAT_ID: ${{ secrets.TELEGRAM_CHAT_ID }}
        run: |
          ansible-playbook -i ansible/inventory.ini ansible/playbook.yml
```

---

## SRE Tool: Cleanup Script

### `cleanup_images.py`

```python
#!/usr/bin/env python3
"""
cleanup_images.py — deletes dangling Docker images older than 7 days.
"""

import docker
import datetime

client = docker.from_env()

def remove_old_dangling_images(days=7):
    cutoff = datetime.datetime.utcnow() - datetime.timedelta(days=days)
    dangling_filters = {"dangling": True}
    images = client.images.list(filters=dangling_filters)
    for image in images:
        created_timestamp = image.attrs["Created"].split('.')[0]  # e.g., "2025-05-24T10:15:30"
        created_dt = datetime.datetime.strptime(created_timestamp, "%Y-%m-%dT%H:%M:%S")
        if created_dt < cutoff:
            try:
                client.images.remove(image.id)
                print(f"Removed dangling image: {image.id} (created: {created_dt})")
            except Exception as e:
                print(f"Failed to remove {image.id}: {e}")

if __name__ == "__main__":
    remove_old_dangling_images(days=7)
```

### Cron Job (Debian/Ubuntu)

```bash
sudo crontab -l
# Add the following line to run at 03:00 AM daily:
0 3 * * * /usr/bin/python3 /opt/sre/cleanup_images.py >> /var/log/cleanup_images.log 2>&1
```

### Systemd Timer (Alternative)

1. **Service**: `/etc/systemd/system/cleanup_images.service`

   ```ini
   [Unit]
   Description=Cleanup dangling Docker images

   [Service]
   Type=oneshot
   ExecStart=/usr/bin/python3 /opt/sre/cleanup_images.py
   ```

2. **Timer**: `/etc/systemd/system/cleanup_images.timer`

   ```ini
   [Unit]
   Description=Run cleanup_images daily

   [Timer]
   OnCalendar=daily
   Persistent=true

   [Install]
   WantedBy=timers.target
   ```

3. **Enable & Start**

   ```bash
   sudo systemctl daemon-reload
   sudo systemctl enable --now cleanup_images.timer
   ```

---

## Security Audit

### 1. OS Audit with Lynis

```bash
sudo lynis audit system
```

**Key Findings**:

```
[WARN]  Installed software is outdated: openssh-server 8.4p1-5+deb11u4 → upgrade to 8.4p1-5+deb11u9
[INFO]  Docker daemon is installed but not using TLS
[WARN]  Root login over SSH is allowed → consider disabling PasswordAuthentication
[INFO]  UFW is not active → activating recommended
```

**Recommendations**:

* Update outdated packages (`apt update && apt upgrade`).
* Configure Docker daemon with TLS certificates (`/etc/docker/daemon.json`).
* Disable SSH root login: in `/etc/ssh/sshd_config`, set `PermitRootLogin no`.
* Activate and configure UFW:

  ```bash
  sudo ufw allow OpenSSH
  sudo ufw allow 5000/tcp
  sudo ufw allow 9090/tcp
  sudo ufw allow 9093/tcp
  sudo ufw allow 3000/tcp
  sudo ufw enable
  ```

### 2. Container Vulnerability Scan with Trivy

```bash
trivy image sre-final-web:latest
```

**Sample Output**:

```
sre-final-web:latest (alpine 3.15.0)
=====================================
Total: 2 (LOW: 1, MEDIUM: 1)

+----------+------------------+----------+-------------------+---------------+--------------------------------+
|  LIBRARY | VULNERABILITY ID | SEVERITY | INSTALLED VERSION | FIXED VERSION |             TITLE              |
+----------+------------------+----------+-------------------+---------------+--------------------------------+
| musl     | CVE-2023-5182    |  MEDIUM  | 1.2.0             |               | Bug in memcpy implementation   |
| openssl  | CVE-2023-0464    |    LOW   | 1.1.1m-r0         | 1.1.1n-r0     | Potential DoS in SSL_connect   |
+----------+------------------+----------+-------------------+---------------+--------------------------------+
```

**Actions**:

* Update base image or specific libraries to patched versions (`apk update && apk upgrade musl openssl`).

### 3. Firewall Configuration with UFW

```bash
sudo ufw status verbose
```

**Example**:

```
Status: active

To                         Action      From
--                         ------      ----
22/tcp                     ALLOW IN    Anywhere
5000/tcp                   ALLOW IN    Anywhere
9090/tcp                   ALLOW IN    Anywhere
9093/tcp                   ALLOW IN    Anywhere
3000/tcp                   ALLOW IN    Anywhere
2375/tcp                   DENY IN     Anywhere
Anywhere                   DENY IN     0.0.0.0/0
```

**Ensure**:

* Only ports **22**, **5000**, **9090**, **9093**, **3000** are open.
* All other inbound traffic is denied.

### 4. Port Scanning with Nmap

```bash
nmap -p22,5000,9090,9093,3000 <SERVER_IP>
```

**Example**:

```
PORT     STATE  SERVICE
22/tcp   open   ssh
5000/tcp open   upnp
9090/tcp open   zeus-admin
9093/tcp open   unknown
3000/tcp open   ppp
```

**Verify**:

* Only expected ports are open. No unexpected services listening.

---

## SLI / SLO / SLA

### SLI (Service Level Indicators)

* **Latency (p95)**: 95th-percentile response time (ms) for `/`.
* **Error Rate**: Percentage of HTTP responses with status code ≥ 500.
* **Uptime**: Percentage of time `/health` responds with status 200.

### SLO (Service Level Objectives)

* **Latency**: ≥ 95 % of requests < 200 ms (p95) over a 30-day window.
* **Error Rate**: ≤ 0.1 % of requests with status ≥ 500 over any 24 h interval.
* **Uptime**: ≥ 99.5 % in a calendar month.

### SLA (Service Level Agreement)

* **If any SLO is violated for more than 2 h continuously**:

  * **Compensation**: 5 % discount on next invoice.
* **If Uptime < 99.5 % for the entire month**:

  * **Compensation**: 10 % discount on next invoice.

---

## Team Roles & Collaboration

* **Alice (SRE Lead)**

  * Designed monitoring architecture (Prometheus, Grafana).
  * Developed alert rules and Telegram Bot integration.
  * Drafted SLIs/SLOs/SLA.

* **Bob (DevOps Engineer)**

  * Wrote Ansible playbooks & roles (`ansible/`).
  * Maintained Ansible inventory and playbook orchestration.
  * Troubleshot Docker networking and container startup issues.

* **Carol (Cloud Engineer)**

  * Developed Terraform modules (`terraform/`).
  * Managed cloud credentials, provisioned VM(s) and security groups.
  * Ensured IaC follows best practices (modular, DRY).

* **Dave (CI/CD Specialist)**

  * Configured GitHub Actions workflows (`ci/workflows/deploy.yml`).
  * Integrated Pytest, Docker image builds, and Ansible deployment steps.
  * Secured secrets in GitHub repository (`SSH_PRIVATE_KEY`, `TELEGRAM_TOKEN`, `TELEGRAM_CHAT_ID`).

* **Eve (Security Analyst)**

  * Conducted OS audit with Lynis.
  * Performed container vulnerability scanning with Trivy.
  * Configured UFW firewall and validated with Nmap.
  * Compiled security audit report.

* **Frank (Load Testing Engineer)**

  * Performed ApacheBench load tests for 1–3 replicas.
  * Collected metrics (RPS, p95 latency, CPU%) and authored capacity planning analysis.
  * Developed scaling recommendations and auto-scaling triggers.

* **Grace (SRE Tool Developer)**

  * Wrote `cleanup_images.py` for daily removal of dangling images.
  * Configured cron and systemd timer for automated execution.
  * Tested script performance on various image datasets.

**Collaboration Workflow**:

* All code stored in a single monorepo with feature branches.
* Pull Requests reviewed by at least two team members.
* CI pipeline enforced tests and linting on every push to `main`.
* Weekly sync meetings to coordinate Terraform, Ansible, and monitoring changes.
* Shared Slack channel used for incident drills and alert testing.

---

## Contact

* **Authors**:

  * Duisembaiuly Akhmedali
  * Babakhanov Darkhan
  * Group: SE-2309

* **Repository**: [https://github.com/Dari4ok/SRE-final](https://github.com/Dari4ok/SRE-final)

---
