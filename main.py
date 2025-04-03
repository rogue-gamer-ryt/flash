import time

from load_balancer import LoadBalancer
from monitoring_service import MonitoringService

import threading


load_balancer = LoadBalancer()
monitoring_service = MonitoringService()

lb_fail_thread = threading.Thread(target=load_balancer.listen_for_server_status_changes, daemon=True)
monitor_thread = threading.Thread(target=monitoring_service.check_servers, daemon=True)

# Start threads
lb_fail_thread.start()
monitor_thread.start()

try:
    while True:
        time.sleep(1)
except KeyboardInterrupt:
    print("\n[MAIN] Shutting down services...")