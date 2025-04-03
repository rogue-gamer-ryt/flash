import json
from redis_util import redis_client
from server import ACTIVE_SERVERS, Server


class LoadBalancer:
    def __init__(self, active_servers=None):
        self.active_servers = active_servers if active_servers else ACTIVE_SERVERS
        self.redis_client = redis_client

    def _remove_server(self, server_id):
        if server_id in self.active_servers:
            print(f"[LOAD BALANCER] Removing {server_id} from config...")
            self.active_servers[server_id].is_active = False


    def listen_for_failures(self):
        subcriber = self.redis_client.pubsub()
        subcriber.subscribe("server:down")
        print("[LOAD BALANCER] Listening for failures...")
        for message in subcriber.listen():
            if message["type"] == "message":
                data = json.loads(message["data"])
                self._remove_server(data["server_id"])