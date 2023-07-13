.. _format:

========================
MAxO Annotations: Format 
========================



The
`maxo_annotations.tsv <https://github.com/monarch-initiative/maxo-annotations/blob/master/annotations/maxo_annotations.tsv>`_
file contains 14 columns separated by tabs (*TSV* format).

- disease_id	
- disease_name	
- citation	
- maxo_id	
- maxo_label	
- hpo_id	
- maxo_relation	
- evidence_code	
- extension_id	
- extension_label	
- attribute	
- creator	
- last_update	
- created_on


Each row in the table specifies a medical action for the management of a specific clinical 
feature (HPO term) in the context of a specific disease. In some cases, the medical action can 
be said to treat the entire disease, in which case the disease_id (a Mondo term) is used instead 
of an HPO term.


The format of the attribute column is inspired by `GTF format <https://useast.ensembl.org/info/website/upload/gff.html>`_.
It contains a semicolon-separated list of tag-value pairs, providing additional information about each annotation.
Currently, the only attribute is ``comment``, but we anticipate adding additional attributes to represent data such
as variant-specific treatments in the future.


.. csv-table:: MAxO Annotations
   :file: _static/example_annots.csv
   :widths: 8,7,7,7,7,7,7,7,7,7,7,7,7,7,7
   :header-rows: 1
   :class: tight-table   



