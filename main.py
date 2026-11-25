from src.telemetry import timer
from src.streamer import stream_file_lines,  batch_streamer
from src.cleaner import clean_batch
from src.dataset import LogDataset

@timer 
def run_pipeline(file_path,batch_size=100):
    logdataset = LogDataset()
    for batch in batch_streamer(stream_file_lines(file_path), batch_size):
        cleaned_batch, quarantined_batch = clean_batch(batch)
        logdataset.add_batch(cleaned_batch,quarantined_batch)
    print("\n" + "=" * 100)
    print("🚀 PIPELINE INGESTION SUMMARY")
    print("=" * 50)
    print(f"Total Valid Records       : {len(logdataset):,}")
    print(f"Total Quarantined (Bad)   : {len(logdataset.get_errors()):,}")
    print(f"Error Level Count         : {len(logdataset.filter_by_level('ERROR')):,}")
    print(f"Critical Level Count      : {len(logdataset.filter_by_level('CRITICAL')):,}")
    print(f"Status                    : {repr(logdataset)}")
    print("=" * 100)
    import json
    with open("data/quarantine_report.json","w") as f:
        f.write(json.dumps(logdataset.quarantine_list,indent=4))


if __name__=='__main__':
    run_pipeline("data/raw_logs.log", batch_size=5000)









