import time
import random
from datetime import datetime
from generate_logs import generate_log_line

SUSPICIOUS_IP = "6.6.6.6"

def main():
    with open("access.log", "a") as f:
        while True:
            if random.random() < 0.15:
                print("Simulating suspicious burst from", SUSPICIOUS_IP)
                for _ in range(6):
                    line = generate_log_line(datetime.now(), ip=SUSPICIOUS_IP)
                    f.write(line + "\n")
                    f.flush()
                    print("Appended:", line)
                    time.sleep(random.uniform(0.5, 1.5))
            else:
                line = generate_log_line(datetime.now())
                f.write(line + "\n")
                f.flush()
                print("Appended:", line)
                time.sleep(random.uniform(1, 3))

if __name__ == "__main__":
    main()