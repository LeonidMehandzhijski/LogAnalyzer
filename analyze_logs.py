import time

def watch_file(file_path):
    with open(file_path, "r") as file:
        file.seek(0, 2)
        try:
            while True:
                line = file.readline()
                if line == "": time.sleep(0.5)
                else:
                    parseline = parse_line(line)
                    if parseline["status"] >= 400: print("ALERT: ", parseline["status"], " from ", parseline["ip"], " on ", parseline["path"])
        except KeyboardInterrupt:
            print("\nStopped watching.")


import argparse

def get_args():
    parser = argparse.ArgumentParser(description="Analyze web server access logs")
    parser.add_argument("--file", default="access.log", help="Path to the log file")
    parser.add_argument("--watch", action="store_true", help="Watch the file for new entries in real time")
    return parser.parse_args()

def parse_line(line):
            clean_line = line.strip()
            timestamp, ip, method, path, status = clean_line.rsplit(" ", 4)
            status_int = int(status)
            log_data = {
                "timestamp": timestamp,
                "ip": ip,
                "method": method,
                "path": path,
                "status": status_int,
            }
            return log_data
def load_logs(file_path="access.log"):
    alllogs = []
    with open(file_path, "r") as file:
        for line_num, line in enumerate(file,1):
            if line_num > 500:
                break
            if not line.strip():
                continue

            singleline = parse_line(line)
            alllogs.append(singleline)
    return alllogs

def main():
    args = get_args()
    most_used_path = {}
    most_used_ip = {}
    max_status = 0
    path_counter = {}
    ip_counter = {}
    logs = load_logs(args.file)
    for log in logs:
        if log["status"] >= 400:
            max_status += 1
        current_path = log["path"]
        if current_path in path_counter:
            path_counter[current_path] += 1
        else:
            path_counter[current_path] = 1

        current_ip = log["ip"]
        if current_ip in ip_counter:
            ip_counter[current_ip] += 1
        else:
            ip_counter[current_ip] = 1
    most_used_path = max(path_counter, key=path_counter.get)
    most_used_ip = max(ip_counter, key=ip_counter.get)
    print(max_status, "amount of logs had status requests above 400")
    print(most_used_path, "is the path that got hit the most")
    print(most_used_ip, "is the ip that made the most requests")
    if args.watch:
        print(f"\nWatching {args.file} for new entries... (Ctrl+C to stop)")
        watch_file(args.file)
if __name__ == "__main__":
    main()