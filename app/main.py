from flask import Flask, jsonify, Response
from prometheus_client import Counter, Gauge, generate_latest, CONTENT_TYPE_LATEST
import time
import random

app = Flask(__name__)

# Metrics counters and gauges
REQUEST_COUNT = Counter('app_requests_total', 'Total HTTP requests', ['method', 'endpoint'])
CPU_USAGE = Gauge('app_cpu_usage', 'Simulated CPU usage')
MEMORY_USAGE = Gauge('app_memory_usage', 'Simulated Memory usage')

@app.route("/")
def index():
    REQUEST_COUNT.labels(method='GET', endpoint='/').inc()
    return jsonify(status="OK", message="Welcome to SRE Final Project")

@app.route("/health")
def health():
    REQUEST_COUNT.labels(method='GET', endpoint='/health').inc()
    return jsonify(status="healthy", timestamp=int(time.time()))

@app.route("/status")
def status():
    cpu = round(random.uniform(0.1, 0.9), 2)
    mem = round(random.uniform(0.2, 0.8), 2)
    CPU_USAGE.set(cpu)
    MEMORY_USAGE.set(mem)
    REQUEST_COUNT.labels(method='GET', endpoint='/status').inc()
    return jsonify(cpu_usage=cpu, memory_usage=mem)

@app.route("/metrics")
def metrics():
    return Response(generate_latest(), mimetype=CONTENT_TYPE_LATEST)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
