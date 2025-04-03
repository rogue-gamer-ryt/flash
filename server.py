from random import random

from redis_util import redis_client


class Server:
    def __init__(self, server_id):
        self.server_id = server_id
        self.redis_client = redis_client
        self.is_active = True

    def status(self):
        status = "healthy" if random() > 0.2 else "unhealthy"  # just to simulate health status
        print(f"[SERVER] | [HEARTBEAT] {self.server_id} - {status}")
        return {"server_id": self.server_id, "status": status}


ALL_SERVERS = {
    f"server_{i}": Server(f"server_{i}") for i in range(1, 6)
}
