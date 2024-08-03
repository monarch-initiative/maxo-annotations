from collections import defaultdict
import argparse
import typing
import hpotk
import random





class AutomaxoEntry:
    """
    Each instance represents one line derived from automaxo/automaxoviewer annotation.
    """
    def __init__(self, line) -> None:
        self._line = line.strip()
        fields = self._line.split("\t")
        if len(fields) < 6:
            print("Malformed line:")
            print(fields)
        self._mondo_id = fields[0]
        self._mondo_label = fields[1]
        self._pmid = fields[2]
        self._maxo = fields[3]
        self._maxo_label = fields[4]
        self._hpo = fields[5]
        self._relation = fields[6]

    def __hash__(self):
        return hash((self._pmid, self._maxo, self._hpo))

    def __eq__(self, other):
        if not isinstance(other, type(self)): return NotImplemented
        return self._pmid == other._pmid and self._maxo == other._maxo and self._hpo == other._hpo
    
    @property
    def mondo_id(self):
        return self._mondo_id
    
    @property
    def mondo_label(self):
        return self._mondo_label
    
    @property
    def maxo_id(self):
        return self._maxo
    
    @property
    def maxo_label(self):
        return self._maxo_label
    
    @property
    def hpo_id(self):
        return self._hpo
    
    @property
    def relation(self):
        return self._relation

    @property
    def line(self):
        return self._line


def parse_automaxo(fname):
    lines = set()
    disease_to_lines_d = defaultdict(list)
    with open(fname) as f:
        next(f) # discard header
        for line in f:
            print(line)
            if len(line) < 10:
                continue
            entry = AutomaxoEntry(line)
            if entry in lines:
                print("Error: duplicate - " + line)
            else:
                lines.add(AutomaxoEntry(line))
    print(f"Got {len(lines)} entries")
    # transform to list and sort it
    for line in lines:
        disease_to_lines_d[line.mondo_id].append(line)
    print(f"Extracted {len(disease_to_lines_d)} diseases")
    return disease_to_lines_d

def get_disease_line(annot_list: typing.List[AutomaxoEntry], hpo: hpotk.Ontology) -> typing.List[str]:
    n_entries = len(annot_list)
    unique_maxo_terms = {x._maxo for x in annot_list}
    unique_hpo_terms = {x.hpo_id for x in annot_list}
    ran_entry = random.choice(annot_list)
    items = list()
    mondo = f"{ran_entry.mondo_label} ({ran_entry.mondo_id})"
    items.append(mondo)
    items.append(str(n_entries))
    items.append(str(len(unique_maxo_terms)))
    items.append(str(len(unique_hpo_terms)))
    maxo = f"{ran_entry.maxo_label} ({ran_entry.maxo_id})"
    items.append(maxo)
    items.append(ran_entry.relation)
    hpo_id = ran_entry.hpo_id
    if hpo_id not in hpo:
        raise ValueError(f"Could not find {hpo_id}")
    term = hpo.get_term(hpo_id)
    hpo_str = f"{term.name} ({hpo_id})"
    if hpo_id == "HP:0000118":
        items.append(mondo)
    else:
        items.append(hpo_str)
    return items


def get_total_stats(disease_to_lines_d: typing.Dict[str, typing.List[AutomaxoEntry]]) -> None:
    unique_maxo_set = set()
    unique_hpo_set = set()
    total_annots = 0
    for annot_list in disease_to_lines_d.values():
        for annot in annot_list:
            unique_maxo_set.add(annot.maxo_id)
            unique_hpo_set.add(annot.hpo_id)
            total_annots += 1
    print(f"Total new annotations {total_annots}")
    print(f"Total unique HPO terms used {len(unique_hpo_set)}")
    print(f"Total unique MAxO terms used {len(unique_maxo_set)}")



if __name__ == '__main__':
    # construct the argument parse and parse the arguments
    ap = argparse.ArgumentParser()
    ap.add_argument("-a", "--automaxo", required=True, help="path to automaxo curation file")
    ap.add_argument("-o", "--out", default="am_summary.tsv", help="name of output file")
    args = ap.parse_args()
    automax_file = args.automaxo
    outfile = args.out
    disease_to_lines_d= parse_automaxo(automax_file)
    store = hpotk.configure_ontology_store()
    hpo = store.load_hpo()
    lines_list = list()
    for annot_list in disease_to_lines_d.values():
        lines_list.append(get_disease_line(annot_list=annot_list, hpo=hpo))
    sorted_lines = sorted(lines_list, key=lambda x: x[0].lower())
    fh = open(outfile, "wt")
    header = ["Mondo", "annotations", "MAxO (n)", "HPO (n)", "example MAxO", "example relation", "Example HPO"]
    fh.write("\t".join(header) + "\n")
    for sl in sorted_lines:
        fh.write("\t".join(sl) + "\n")
    fh.close()
    get_total_stats(disease_to_lines_d=disease_to_lines_d)
