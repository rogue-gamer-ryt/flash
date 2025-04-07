# Server Health Monitoring System

A distributed system that monitors server health status using Redis pub/sub for real-time communication between components. 

I built this to project to understand the fundamentals of how the Pub/Sub messaging pattern works. This project mimics the usage of Pub/Sub message pattern for server health monitoring.  

## Overview

This project implements a server health monitoring system with the following components:

- **Monitoring Service**: Continuously checks server health and publishes status changes
- **Load Balancer**: Listens for server status changes and manages server availability
- **Server**: Simulates server instances with health status checks
- **Redis Pub/Sub**: Used for real-time communication between components

## Features

- Real-time server health monitoring
- Automatic server failure detection
- Server recovery detection
- Load balancer integration
- Distributed architecture using Redis pub/sub

## Components

### Monitoring Service
- Continuously monitors server health status
- Publishes messages to Redis channels:
  - `server:down`: When a server becomes unhealthy
  - `server:recovery`: When a previously unhealthy server recovers
- Maintains server health history for recovery detection

### Load Balancer
- Subscribes to Redis channels for server status changes
- Manages server availability based on health status
- Automatically removes unhealthy servers from the pool
- Re-adds recovered servers to the active pool

### Server
- Simulates server instances with health status checks
- Provides health status through a status endpoint
- Randomly generates health status for demonstration purposes

## Prerequisites

- Python 3.x
- Docker

## Installation

1. Clone the repository:
```bash
git clone https://github.com/rogue-gamer-ryt/flash.git
cd flash
```

2. Install dependencies:
```bash
pip install redis
```

3. Start Redis using Docker:
```bash
docker run -d --name redis-server -p 6379:6379 redis:latest
```

To stop Redis:
```bash
docker stop redis-server
docker rm redis-server
```

## Usage

1. Start the main application:
```bash
python main.py
```

The system will:
- Start monitoring all servers
- Begin listening for server status changes
- Automatically manage server availability

## Project Structure

```
.
├── main.py                 # Main application entry point
├── monitoring_service.py   # Server health monitoring service
├── load_balancer.py       # Load balancer implementation
├── server.py              # Server simulation
├── redis_util.py          # Redis client utility
└── README.md              # Project documentation
```

## How It Works

1. The Monitoring Service continuously checks server health status
2. When a server becomes unhealthy:
   - A message is published to the `server:down` channel
   - The Load Balancer receives the message and marks the server as inactive
3. When a server recovers:
   - A message is published to the `server:recovery` channel
   - The Load Balancer receives the message and marks the server as active again

## Testing

The system includes simulated server health status for demonstration purposes. Servers randomly change their health status to demonstrate the monitoring and load balancing functionality.

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## License

This project is licensed under the MIT License - see the LICENSE file for details.
