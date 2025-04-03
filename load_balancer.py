import json
from redis_util import redis_client
from server import ALL_SERVERS


class LoadBalancer:
    def __init__(self, all_servers=None):
        self.all_servers = all_servers if all_servers else ALL_SERVERS
        self.redis_client = redis_client

    def _remove_server(self, server_id):
        if server_id in self.all_servers:
            print(f"[LOAD BALANCER] Removing {server_id} from config...")
            self.all_servers[server_id].is_active = False

    def _add_server(self, server_id):
        if server_id in self.all_servers:
            print(f"[LOAD BALANCER] Adding {server_id} back to config...")
            self.all_servers[server_id].is_active = True

    def listen_for_failures(self):
        subscriber = self.redis_client.pubsub()
        subscriber.subscribe("server:down", "server:recovery")
        print("[LOAD BALANCER] Listening for server status changes...")
        for message in subscriber.listen():
            if message["type"] == "message":
                data = json.loads(message["data"])
                if message["channel"].decode() == "server:down":
                    self._remove_server(data["server_id"])
                elif message["channel"].decode() == "server:recovery":
                    self._add_server(data["server_id"])
