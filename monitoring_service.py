import json
import time

from redis_util import redis_client
from server import ALL_SERVERS


class MonitoringService:
    def __init__(self, all_servers=None):
        self.all_servers = all_servers if all_servers else ALL_SERVERS
        self.redis_client = redis_client
        self.server_health_history = {server_id: True for server_id in self.all_servers.keys()}

    def publish_failed_server(self, server_id):
        listeners = self.redis_client.publish("server:down", json.dumps({"server_id": server_id}))
        print(f"[MONITORING] Failed server published to {listeners} clients")

    def publish_recovered_server(self, server_id):
        listeners = self.redis_client.publish("server:recovery", json.dumps({"server_id": server_id}))
        print(f"[MONITORING] Recovered server published to {listeners} clients")

    def check_servers(self):
        while True:
            for server_id, server in self.all_servers.items():
                try:
                    server_status = server.status().get("status")
                    is_healthy = server_status == "healthy"
                    
                    # If server was unhealthy and is now healthy, publish recovery
                    if not self.server_health_history[server_id] and is_healthy:
                        print(f"[MONITORING] | [ALERT] {server_id} has RECOVERED!")
                        self.publish_recovered_server(server_id)
                    
                    # If server was healthy and is now unhealthy, publish failure
                    elif self.server_health_history[server_id] and not is_healthy:
                        print(f"[MONITORING] | [ALERT] {server_id} is DOWN!")
                        self.publish_failed_server(server_id)
                    
                    # Update health history
                    self.server_health_history[server_id] = is_healthy

                except Exception:
                    if self.server_health_history[server_id]:
                        print(f"[MONITORING] | [ALERT] {server_id} is DOWN!")
                        self.publish_failed_server(server_id)
                        self.server_health_history[server_id] = False

            time.sleep(2)  # Check every 2 seconds


if __name__ == "__main__":
    ms = MonitoringService()
    ms.check_servers()
