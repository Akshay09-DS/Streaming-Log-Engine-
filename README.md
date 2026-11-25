# Streaming ETL Log Engine

A modular, memory-efficient **Streaming ETL & Log Quarantine Engine** written in pure Python. Designed to ingest high-volume server logs in chunks using lazy generators, isolate malformed records without halting execution, benchmark pipeline latency via custom decorators, and expose validated records through a PyTorch-style dataset container.

---

## Key Engineering Highlights

* **Zero-RAM Lazy Streaming (`src/streamer.py`):** Uses Python generators (`stream_file_lines`, `batch_streamer`) to read and batch records line-by-line instead of loading entire files into memory via `.readlines()`.
* **Fault-Tolerant Quarantine Pattern (`src/cleaner.py`):** `parse_log_line` and `clean_batch` parse delimited server logs into typed records (`Status_code` and `Latency MS` cast to `int`) and route corrupted rows (`ValueError`, `IndexError`) into a dead-letter quarantine ledger with exact error diagnostics (`data/quarantine_report.json`).
* **PyTorch-Style Dataset Container (`src/dataset.py`):** `LogDataset` implements Python dunder methods (`__len__`, `__getitem__`, `__repr__`) along with `add_batch()`, `get_errors()`, and `filter_by_level()` for clean downstream querying.
* **Decorator Telemetry (`src/telemetry.py`):** Custom `@timer` decorator benchmarks pipeline execution time with `time.perf_counter()`.
* **Zero External Dependencies:** Built 100% with the Python standard library.

---

## Project Structure

```text
Log_engine/
├── data/
│   └── raw_logs.log          # 25,000 multi-service synthetic logs (with ~3% injected corruption)
├── src/
│   ├── __init__.py
│   ├── telemetry.py          # @timer latency profiler decorator
│   ├── streamer.py           # Lazy file streamer & batch chunker generators
│   ├── cleaner.py            # Delimited log parser & quarantine error handler
│   └── dataset.py            # LogDataset container (__len__, __getitem__, __repr__)
├── main.py                   # Pipeline orchestrator & CLI summary dashboard
├── .gitignore
└── README.md
```

---

## Quick Start

1. **Clone the repository:**
   ```bash
   git clone https://github.com/<your-username>/<your-repo-name>.git
   cd <your-repo-name>
   ```

2. **Run the pipeline:**
   ```bash
   python main.py
   ```

---

## Sample Output (25,000 Records, Batch Size = 5,000)

```text
====================================================================================================
🚀 PIPELINE INGESTION SUMMARY
==================================================
Total Valid Records       : 24,252
Total Quarantined (Bad)   : 748
Error Level Count         : 4,030
Critical Level Count      : 4,106
Status                    : LogDataSet (Valid =24252, Quarantine = 748)
====================================================================================================
[TIMER]: run_pipeline executed in 0.10802570000009837
```

Corrupted records are automatically exported to `data/quarantine_report.json` with their raw text and exception message for auditing.
