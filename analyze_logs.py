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
def load_logs():
    alllogs = []
    with open("access.log", "r") as file:
        for line_num, line in enumerate(file,1):
            if line_num > 500:
                break
            if not line.strip():
                continue

            singleline = parse_line(line)
            alllogs.append(singleline)
    return alllogs

def main():
    most_used_path = {}
    most_used_ip = {}
    max_status = 0
    path_counter = {}
    ip_counter = {}
    logs = load_logs()
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
if __name__ == "__main__":
    main()