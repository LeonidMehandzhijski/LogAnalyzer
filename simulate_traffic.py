import time
import random
from datetime import datetime
from generate_logs import random_ip, PATHS, METHODS, STATUS_CODES, generate_log_line

def main():
    with open("access.log", "a") as f:
        try:
            while True:
                line = generate_log_line(datetime.now())
                f.write(line + "\n")
                f.flush()
                print("Appended:", line)
                time.sleep(random.uniform(1,3))
        except KeyboardInterrupt:
            print("\nStopped generating logs...")

if __name__ == "__main__":
    main()