import redis


class RedisClient:
    _instance = None

    def __new__(cls, host='localhost', port=6379, db=0):
        if cls._instance is None:
            cls._instance = super(RedisClient, cls).__new__(cls)
            cls._instance.host = host
            cls._instance.port = port
            cls._instance.db = db
            cls._instance._initiate_client()
        return cls._instance

    def _initiate_client(self):
        self.client = redis.Redis(host=self.host, port=self.port, db=self.db)

    def get_client(self):
        return self.client


redis_client = RedisClient(host='localhost', port=6379, db=0).get_client()

