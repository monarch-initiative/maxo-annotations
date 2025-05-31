from pathlib import Path
import os

## Update obsolete terms by hand

current_file = Path(__file__).resolve()
current_dir = current_file.parent.parent
fname = os.path.join(current_dir, "annotations", "maxo_diagnostic_annotations.tsv")

update_d = {
    ("MAXO:0001006", "blood cell count"): ["MAXO:0001509", "blood cell count"]
}


lines = list()

with open(fname) as f:
    for line in f:
        if "MAXO:0001006" in line:
            line = line.replace("MAXO:0001006", "MAXO:0001509")
        lines.append(line)


fh = open(fname, "wt")
for line in lines:
    fh.write(line)
fh.close()