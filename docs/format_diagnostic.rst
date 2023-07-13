.. _format_diagnostic:

===================================
MAxO Diagnostic Annotations: Format 
===================================

The
`maxo_diagnostic_annotations.tsv <https://github.com/monarch-initiative/maxo-annotations/blob/master/annotations/maxo_diagnostic_annotations.tsv>`_
file contains six columns separated by tabs (*TSV* format).

- hpo_id
- hpo_label 
- predicate_id: ``is_observable_through`` or ``is_prenatally_observable_through``
- maxo_id
- maxo_label
- creator_id

Each row in the table specifies a diagnostic modality that is able to ascertain the HPO term in question.
The following table shows a few examples


.. csv-table:: MAxO Diagnostic Annotations
   :file: _static/example_diagnostic_annots.csv
   :widths: 10, 25,10,10,25, 20
   :header-rows: 1
   :class: tight-table   




