.. _guidelines:

==========================
MAxO Annotation Guidelines 
==========================

Scope of MAxO
^^^^^^^^^^^^^

To understand the scope of MAxO annotations, it is important to first understand the scope of MAxO.



1. *Clinical tests*. 

Descriptions of clinical tests are included In contrast, clinical results are out of scope.
purely research lab tests are not in scope.
2. Recommendations for diagnostics, therapy, treatment, or prevention or avoidance. 
3. 
4. Life skills would not be included, but it will be decided on a case by case basis.

Examples: hearing aid usage and speech therapy (yes), sign language (no)
	
3. Clinical tests, examinations, and clinically relevant biomarker assessments will be included, but developmental research will not. Think CLIA certified tests.

Examples: Clinical tests (yes), (no)
	
4. Supplementation or alternative therapies are only included if there are studies indicating their utility and have been recommended in the clinical literature. This section will be kept minimal and decided on a case by case basis.

Examples: chiropractic therapy, amino acid/vitamin supplementation(yes), herbal supplementation(no)-* 



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

Therapeutic annotations
^^^^^^^^^^^^^^^^^^^^^^^



