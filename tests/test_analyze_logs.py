import unittest
from datetime import datetime, timedelta
from analyze_logs import parse_line, find_suspicious_ips


class TestAnalyzeLogs(unittest.TestCase):

    def test_parse_line(self):
        log_line="2026-09-28 12:30:45 192.168.1.10 GET /admin 403"
        result = parse_line(log_line)

        self.assertEqual(result["ip"], "192.168.1.10")
        self.assertEqual(result["method"], "GET")
        self.assertEqual(result["path"], "/admin")
        self.assertEqual(result["status"], 403)
        self.assertEqual(result["timestamp"], datetime(2026,9,28,12,30, 45))

    def test_find_sus_ip_flag_correct(self):
        fake_logs_by_ip={"6.6.6.6": []}
        for i in range(5):
            start_time = datetime(2026, 8, 16, 4, 0, 0)
            seconds_to_add = i * 2
            timestamp = start_time + timedelta(seconds=seconds_to_add)
            fake_logs_by_ip["6.6.6.6"].append(timestamp)

        result = find_suspicious_ips(fake_logs_by_ip,5,10)
        self.assertIn("6.6.6.6", result)
    def test_find_sus_ip_flag_incorrect(self):
        fake_logs_by_ip_two = {"6.6.6.6": []}
        for i in range(5):
            start_time = datetime(2026, 8, 16, 4, 0, 0)
            seconds_to_add = i * 3
            timestamp = start_time + timedelta(seconds=seconds_to_add)
            fake_logs_by_ip_two["6.6.6.6"].append(timestamp)
        result = find_suspicious_ips(fake_logs_by_ip_two, 5, 10)
        self.assertNotIn("6.6.6.6", result)

if __name__ == "__main__":
    unittest.main()