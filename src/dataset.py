class LogDataset:
    def __init__(self):
        self.valid_record = []
        self.quarantine_list = []

    def __len__(self):
        return len(self.valid_record)

    def __getitem__(self, key):
        return self.valid_record[key]

    def __repr__(self):
        return f"LogDataSet (Valid ={len(self.valid_record)}, Quarantine = {len(self.quarantine_list)})"

    def add_batch(self,valid,quarantine):
        self.valid_record.extend(valid)
        self.quarantine_list.extend(quarantine)

    def get_errors(self):
        return self.quarantine_list

    def filter_by_level(self,level):
        return [record for record in self.valid_record if record["Level"] == level]

if __name__ == "__main__":
    log_dataset = LogDataset()
    test_valid = [
    {"Timestamp": "2026-11-24 08:00:00", "Level": "INFO",     "Service": "auth-service",     "Status_code": 200, "Latency MS": 45,   "Message": "User login successful"},
    {"Timestamp": "2026-11-24 08:00:02", "Level": "ERROR",    "Service": "payment-gateway",  "Status_code": 502, "Latency MS": 3200, "Message": "Payment gateway handshake failed"},
    {"Timestamp": "2026-11-24 08:00:04", "Level": "CRITICAL", "Service": "ml-inference",     "Status_code": 500, "Latency MS": 5500, "Message": "ML model latency spike"},
    {"Timestamp": "2026-11-24 08:00:06", "Level": "ERROR",    "Service": "user-db",          "Status_code": 504, "Latency MS": 4000, "Message": "Database connection timeout"},
    ]

    test_quarantined = [
    {"Raw": "CORRUPTED_RAW_SOCKET_DUMP", "Error": "list index out of range"},
    {"Raw": "2026-11-24 08:00:08 | WARN | auth-service", "Error": "list index out of range"},
    ]
    log_dataset.add_batch(test_valid, test_quarantined)
    print(log_dataset)














