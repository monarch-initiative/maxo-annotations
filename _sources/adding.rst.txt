.. _adding:

==================================
Adding a MAxO Annotation with POET
==================================

To add annotations, first login to POET as described in :ref:`poet`.

In this example, we will add an annotation for 
`Immunodeficiency with hyper IgM, type 5 (OMIM:608106) <https://omim.org/entry/608106>`_. 
You can search for the disease using the OMIM id (``OMIM:608106`` or ``608106``), the Mondo ID (``MONDO:0011971`` or ``0011971``) 
or the disease name (``Immunodeficiency with hyper IgM, type 5``).


.. figure:: img/poet-annot1.png
    :scale: 75 %
    :align: center
    :alt: POET - searching for OMIM:608106

|

Select the correct disease entry, and go to the Treatment annotation page:

.. figure:: img/poet-annot2.png
    :scale: 75 %
    :align: center
    :alt: POET - Treatmment annotation page


|

We will annotate this publication: `Imai K, et al. (2003) Human uracil-DNA glycosylase deficiency associated with profoundly 
impaired immunoglobulin class-switch recombination. Nat Immunol 4:1023-8 <https://pubmed.ncbi.nlm.nih.gov/12958596/>`_. 
This article describes three patients, each of whom received  intravenous immunoglobulin (IVIG) treatment, which corresponds to the 
MAxO term `immunoglobulin infusion therapy (MAXO:0001480) <https://www.ebi.ac.uk/ols4/ontologies/maxo/classes/http%253A%252F%252Fpurl.obolibrary.org%252Fobo%252FMAXO_0001480>`_.

We click on the blue ``+`` button and open the treatment curation dialog. We can now add the term by typing the first several letters and waiting 
for the autocomplete to show us matching terms.


.. figure:: img/poet-annot3.png
    :scale: 75 %
    :align: center
    :alt: POET - Treatmment annotation page

|

We choose the correct MAxO term and then choose the HPO term that represents the direct target of the treatment, again using autocomplete 
(`Decreased circulating IgG level HP:0004315 <https://hpo.jax.org/app/browse/term/HP:0004315>`_). The choose from one of the five 
:ref:`_maxo_relations` using the drop down menu  (in this case, ``TREATS``).

.. figure:: img/poet-annot4.png
    :scale: 75 %
    :align: center
    :alt: POET - Treatmment annotation page

|

Finally, we need to add the citation. Click on the ``Select Source`` button. If you do not see the correct citation, you can add a new 
one using the dialog shown below (search on the PMID; in this case, ``12958596``).

.. figure:: img/poet-annot5.png
    :scale: 75 %
    :align: center
    :alt: POET - Treatmment annotation page

|

Finally, when all required data have been entered, the ``SUBMIT`` button will be activated, as shown below.


.. figure:: img/poet-annot6.png
    :scale: 75 %
    :align: center
    :alt: POET - Treatmment annotation page

|

After you submit an annotation, the HPO/POET team will review the data and add it to the repository or ask questions to clarify any open questions.




