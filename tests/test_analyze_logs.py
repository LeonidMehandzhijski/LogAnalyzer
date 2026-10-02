import unittest
from datetime import datetime, timedelta

from analyze_logs import find_suspicious_ips, summarize_logs
from log_utils import parse_line

class TestAnalyzeLogs(unittest.TestCase):

    def test_parse_line(self):
        log_line="2026-09-28 12:30:45 192.168.1.10 GET /admin 403"
        result = parse_line(log_line)

        self.assertEqual(result["ip"], "192.168.1.10")
        self.assertEqual(result["method"], "GET")
        self.assertEqual(result["path"], "/admin")
        self.assertEqual(result["status"], 403)
        self.assertEqual(result["timestamp"], datetime(2026,9,28,12,30, 45))

    def test_find_ip_in_window(self):
        fake_logs_by_ip={"6.6.6.6": []}
        start_time = datetime(2026, 8, 16, 4, 0, 0)
        for i in range(5):
            seconds_to_add = i * 2
            timestamp = start_time + timedelta(seconds=seconds_to_add)
            fake_logs_by_ip["6.6.6.6"].append(timestamp)

        result = find_suspicious_ips(fake_logs_by_ip,5,10)
        self.assertIn("6.6.6.6", result)
    def test_find_ip_outside_window(self):
        fake_logs_by_ip_two = {"6.6.6.6": []}
        start_time = datetime(2026, 8, 16, 4, 0, 0)
        for i in range(5):
            seconds_to_add = i * 3
            timestamp = start_time + timedelta(seconds=seconds_to_add)
            fake_logs_by_ip_two["6.6.6.6"].append(timestamp)
        result = find_suspicious_ips(fake_logs_by_ip_two, 5, 10)
        self.assertNotIn("6.6.6.6", result)

    def test_sum_logs_correctly(self):
        start_time = datetime(2026, 8, 16, 4, 0, 0)

        logs = [
            {"ip": "6.6.6.6", "method": "GET", "path": "/login","status":200, "timestamp": start_time},
            {"ip": "6.6.6.6", "method": "GET", "path": "/login", "status":404, "timestamp": start_time + timedelta(seconds=3)},
            {"ip": "6.6.6.6", "method": "GET", "path": "/login", "status":500, "timestamp": start_time + timedelta(seconds=6)},
            {"ip": "1.1.1.1", "method": "GET", "path": "/products", "status":200, "timestamp": start_time + timedelta(seconds=9)},
        ]

        config = {
            "error_status_threshold": 400,
            "suspicious_ip_request_count": 3,
            "suspicious_ip_window_seconds": 10
        }

        summary = summarize_logs(logs, config)

        self.assertEqual(summary["error_count"],2)
        self.assertEqual(summary["most_used_path"], "/login")
        self.assertEqual(summary["most_used_ip"], "6.6.6.6")
        self.assertIn("6.6.6.6", summary["suspicious_ips"])

if __name__ == "__main__":
    unittest.main()