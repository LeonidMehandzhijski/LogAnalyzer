import random
from datetime import datetime, timedelta

PATHS = ["/", "/login", "/admin", "/api/users","/products", "/checkout"]
METHODS = ["GET", "POST"]
STATUS_CODES = [200, 200, 200, 301, 404, 403, 500]

def random_ip():
    return f"{random.randint(1,223)}.{random.randint(0,255)}.{random.randint(0,255)}.{random.randint(0,255)}"

def generate_log_line(timestamp, ip=None):
    if ip is None:
        ip = random_ip()
    method = random.choice(METHODS)
    path = random.choice(PATHS)
    status = random.choice(STATUS_CODES)
    return f"{timestamp.strftime('%Y-%m-%d %H:%M:%S')} {ip} {method} {path} {status}"

def main():
    start = datetime.now()
    with open("access.log", "w") as f:
        for i in range(500):
            ts = start + timedelta(seconds=i * random.randint(1,5))
            f.write(generate_log_line(ts) + "\n")

if __name__ == "__main__":
    main()