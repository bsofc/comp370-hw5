import csv
from datetime import datetime
import argparse

CREATED_COL = "Created Date"
COMPLAINT_COL = "Complaint Type"
BOROUGH_COL = "Borough"

def parse_date(text):
    if not text:
        return None
    for fmt in ("%m/%d/%Y %I:%M:%S %p", "%m/%d/Y %H:%M", "%Y-%m-%d %H:%M:%S", "%Y-%m-%d"):
        try:
            return datetime.strptime(text,fmt)
        except ValueError:
            pass
    return None


def main():
    parser = argparse.ArgumentParser()

    #required input file
    parser.add_argument("-i","--input", required=True, help="Input CSV.")

    #required start date
    parser.add_argument("-s","--start", required=True, help="Start date (YYYY-MM-DD) Inclusive")

    #required end date
    parser.add_argument("-e","--end", required=True, help="End date (YYYY-MM-DD) Inclusive")

    #optieional output (if not given, prints to stdout)
    parser.add_argument("-o","--output", default=None, help="Optional output CSV file")

    args = parser.parse_args()

    #convert string to time
    start_day = datetime.strptime(args.start, "%Y-%m-%d")
    end_day = datetime.strptime(args.end, "%Y-%m-%d")
    #inclusive to the end of the date until 23:59:59
    end_day = end_day.replace(hour=23, minute=59, second=59)

    counts = {}

    with open(args.input , "r") as f:
        #csv reader
        reader = csv.DictReader(f)
        for row in reader:
            #get created_date
            created_text = row.get(CREATED_COL, "")
            created_dt = parse_date(created_text)

            complaint = row.get(COMPLAINT_COL,"").strip().lower()
            borough = row.get(BOROUGH_COL,"").strip().lower().title()

            #skip if needed
            if not complaint or not borough or created_dt is None :
                continue

            if not (start_day <= created_dt <= end_day):
                continue
          
            key = (complaint,borough)
            counts[key] = counts.get(key, 0) +1

    if args.output:
        out_f = open(args.output, "w")

    else:
        import sys
        out_f = sys.stdout

    writer = csv.writer(out_f)
    writer.writerow(["complain type", "borough", "count"])

    for (complaint, borough), c in sorted(counts.items(), key=lambda item: item[1], reverse=True):
        writer.writerow([complaint,borough,c])

    if args.output:
        out_f.close()



if __name__ == "__main__":
        main()




