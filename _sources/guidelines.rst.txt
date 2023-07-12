.. _guidelines:

==========================
MAxO Annotation Guidelines 
==========================


To understand the scope of MAxO annotations, it is important to first understand the scope of MAxO.

Scope of MAxO
^^^^^^^^^^^^^


Numerous computational resources exist to annotate and analyze pharmaceutical data, including 
`DrugCentral <https://drugcentral.org/>`_, 
`DrugBank <https://go.drugbank.com/>`_, and the 
`PharmGKB <https://www.pharmgkb.org/>`_.`
However, clinical management includes many other measures that collectively 
we refer to as medical actions. For instance, clinicians may prescribe a certain dietary 
intervention such as coenzyme Q10 supplementation for individuals with primary coenzyme Q10 deficiencies, 
or recommend the avoidance of a ketogenic diet, which although helpful for some individuals with epilepsy 
is contraindicated for individuals with certain diseases. Other medical actions include surgical procedures, 
ablations, treatment with biologics, behavioral and cognitive interventions, deep brain stimulation, and 
many others.  


There are two main types of MAxO annotations. 


Diagnostic annotations
^^^^^^^^^^^^^^^^^^^^^^

The diagnostic annotations relate MAxO terms to individual phenotypic abnormalities 
represented by `Human Phenotype Ontology <https://hpo.jax.org/app/>`_ terms. These MAxO annotations 
indicate how to ascertain a phenotypic abnormality. For instance, 
`Rib fusion (HP:0000902) <https://hpo.jax.org/app/browse/term/HP:0000902>`_ 
is_observable_through	
`chest radiograph procedure (MAXO:0010356) <https://www.ebi.ac.uk/ols4/ontologies/maxo/classes/http%253A%252F%252Fpurl.obolibrary.org%252Fobo%252FMAXO_0010356>`_.

Diagnostic annotations are independent of the disease in the sense that the same diagnostic procedure can be used 
to ascertain the feature regardless of the underlying disease. For instance, rib fusion is a feature of multiple 
diseases including `Congenital disorder of glycosylation, type IIg <https://hpo.jax.org/app/browse/disease/OMIM:611209>`_, 
`Craniofacial dysmorphism, skeletal anomalies, and impaired intellectual development 1 <https://hpo.jax.org/app/browse/disease/OMIM:213980>`_,
and `Escobar syndrome <https://hpo.jax.org/app/browse/disease/OMIM:265000>`_, but in each case the same diagnostic procedure,
a chest radiograph, can be used to ascertain whether rib fusion is present.

Descriptions of clinical tests are included In contrast, purely research lab tests are not in scope. MAxO is not 
intended to be used for annotating results of clinical tests.

Therapeutic annotations
^^^^^^^^^^^^^^^^^^^^^^^

These annotations are made for each disease or disease group, annotating 
`Mondo <https://www.ebi.ac.uk/ols4/ontologies/mondo>`_ terms.

It is possible to annotate at a specific disease, e.g., 
`Bardet-Biedl syndrome 5 (MONDO:0014434) <https://www.ebi.ac.uk/ols4/ontologies/mondo/classes/http%253A%252F%252Fpurl.obolibrary.org%252Fobo%252FMONDO_0014434>`_,
or a group of related diseases, e.g.,
`Bardet-Biedl syndrome (MONDO:0015229) <https://www.ebi.ac.uk/ols4/ontologies/mondo/classes/http%253A%252F%252Fpurl.obolibrary.org%252Fobo%252FMONDO_0015229?lang=en>`_,
which is a grouping class in Mondo that includes each of the 22 genetic subtypes of this disease.

Annotations can be made for that following items:

**Therapeutic procedure**: 
    - Biologic therapy
    - Pharmacotherapy
    - Physical therapy
    - Radiation therapy
    - Surgical procedure
    - etc.

**Palliative care**: 
    - end-of-life care
    - pain management
    - etc.

**Preventative therapeutics**: 
    - smoking prevention
    - preventative immunization
    - prevention of abnormal physiologic state, i.e., hypertension prevention
    - ketosis prevention
    - etc.

**Complementary and alternative therapies**: 
    - Acupuncture therapy
    - Chiropractic therapy
    - etc.

**Medical action avoidance**:
    - ketogenic diet intake avoidance
    - avoid CT scan
    - radiograph imaging avoidance
    - etc.



Supplementation or alternative therapies are only included if there are studies 
indicating their utility and have been recommended in the clinical literature. 
Examples: chiropractic therapy, amino acid/vitamin supplementation(yes), herbal supplementation(no)-* 

