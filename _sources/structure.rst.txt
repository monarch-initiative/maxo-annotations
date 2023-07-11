.. _maxo_structure:

==============================
Structure of a MAxO Annotation
==============================


The MAxO annotation model includes disease ID and label using the `MONDO ontology <https://www.ebi.ac.uk/ols4/ontologies/mondo>`_,
the MAxO term id and label, and a `Human Phenotype Ontology (HPO) <https://hpo.jax.org/app/>`_
term that represents the target of the treatment. If the treatment targets the disease itself rather than specific 
manifestations of the disease, this is indicated by the symbol DISEASE.TREATMENT. 
Finally, two fields for an extension ID and label can be used to specify additional information about a treatment. 
For instance, in the example, the MAxO term serotonin-norepinephrine reuptake inhibitor agent therapy is further specified 
with the `ChEBI <https://www.ebi.ac.uk/ols4/ontologies/chebi>`_ term for fluoxetine, which is a specific type of 
serotonin-norepinephrine reuptake inhibitor. Lastly, an additional field is available for comments. 
In the example provided in Table 2, fluoxetine, a treatment commonly used for one type of congenital 
myasthenic syndrome (slow-channel congenital myasthenic syndrome, CMS 1A/2A/3A/4A), may worsen symptoms of 
fatigable weakness if administered to patients with a different type of congenital myasthenic syndrome 
caused by defects in the same gene, fast-channel CMS (CMS 1B/2B/4B). 
Fluoxetine is a common treatment for depression that may mistakenly be administered to patients affected 
by fast-channel CMS without understanding the need for its avoidance. 
The two MAxO entries listed in Table 2 are linked to the specific CMS subtypes involved and 
can thus indicate the precise diseases for which fluoxetine is an appropriate treatment (example 1) and in 
which it should be avoided, i.e., the treatment is contraindicated. 



.. csv-table:: MAxO Annotation Example
   :file: _static/example.csv
   :widths: 20, 40, 40
   :header-rows: 1
   :class: tight-table   


Note that the ontology extension field is mainly needed for pharmaceutical annotations. MAxO contains 
terms for medication categories (e.g., beta blocker) and not for specific medications (e.g. propranolol), 
and if the specific mediciation is relevant for an annotation, the extension field can be used. POET supports 
annotation with  `ChEBI <https://www.ebi.ac.uk/ols4/ontologies/chebi>`_ terms.

