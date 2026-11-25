def parse_log_line(raw_line):
    clean_line = []
    for i in raw_line.split(" | "):
        clean_line.append(i)
    return{
        "Timestamp" : clean_line[0],
        "Level" : clean_line[1],
        "Service" :  clean_line[2],
        "Status_code" : int(clean_line[3]), 
        "Latency MS" :  int(clean_line[4].strip("ms")),
        "Message"  : clean_line[5]
    }

def clean_batch(raw_batch):
    valid_records = []
    quarantined_records = []
    for i in raw_batch:
        try :
            clean_line = parse_log_line(i)
            valid_records.append(clean_line)
        except (ValueError,IndexError) as e:
            quarantined_records.append({"Raw":i,"Error":str(e)})
    return valid_records , quarantined_records

if __name__ == '__main__':
    batch = ["2026-11-24 08:00:00 | INFO | auth-service | 200 | 45ms | User login successful","Corrupted_Packet_Loss"]
    print(clean_batch(batch))

            

        
        
    








