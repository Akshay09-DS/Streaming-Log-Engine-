def stream_file_lines(file_path):
    with open(file_path,"r") as f:
        for i in f:
            yield i.strip()
       
def batch_streamer(line_stream,batch_size=100):
    batch = []
    for line in line_stream:
        batch.append(line)
        if len(batch) == batch_size:
            yield batch
            batch = []

    if batch:
        yield batch

if __name__=='__main__':
    a = stream_file_lines("data/raw_logs.log")
    batch = batch_streamer(a,)
    batchcount = 0
    for i in batch:
        batchcount += 1
        print(len(i))
    print(batchcount)
    

