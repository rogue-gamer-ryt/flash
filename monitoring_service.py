import json
import time

from redis_util import redis_client
from server import ALL_SERVERS


class MonitoringService:
    def __init__(self, all_servers=None):
        self.all_servers = all_servers if all_servers else ALL_SERVERS
        self.redis_client = redis_client

    def publish_failed_server(self, server_id):
        listeners = self.redis_client.publish("server:down", json.dumps({"server_id": server_id}))
        print(f"[MONITORING] Failed server published to {listeners} clients")

    def check_servers(self):
        while True:
            for _, server in self.all_servers.items():
                try:
                    server_status = server.status().get("status")

                    if server_status == "healthy":
                        continue
                    else:
                        raise Exception("Unaccepted response")
                except Exception:
                    print(f"[MONITORING][ALERT] {server.server_id} is DOWN!")
                    self.publish_failed_server(server.server_id)

            time.sleep(2)  # Check every 2 seconds


if __name__ == "__main__":
    ms = MonitoringService()
    ms.check_servers()
