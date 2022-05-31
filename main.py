from os import name
from dipmp_server import server


if __name__ == "__main__":
    server.run('0.0.0.0', port=5000)