Examples
========

This section demonstrates some usage examples of the metadata management module.
The example scripts can be found in the ``./examples`` folder.

Loading and saving the template dataset
---------------------------------------

Run ``template_operations.py`` to load and the the template dataset in ``./examples/temp/``.
The template dataset is in `the SPARC dataset structure <https://sparc.science/help/3FXikFXC8shPRd8xZqhjVT>`_ and retried from `the sparc-curation repository <https://github.com/SciCrunch/sparc-curation>`_.
Default template version number: 2.0.0

.. literalinclude:: ../../examples/template_operations.py
      :language: python

Listing metadata elements
-------------------------

Run ``dataset_info.py`` to list the SPARC metadata elements for a given metadata file.

.. code-block:: python

    elements = dataset.list_fields(category="METADATA_FILE", axis=0)

Where
   * METADATA_FILE: The name of the metadata file, e.g "dataset_description" or "subjects"
   * axis: If axis=0, list the headers (the first row). If axis=1, list the index column (the first column). Please set axis to 0 for dataset_description. For the other metadata files, set axis to 1.

.. literalinclude:: ../../examples/dataset_info.py
      :language: python

Updating metadata
-----------------

Run ``update_dataset.py`` to update metadata or append a row to the metadata file.

There are two types of the metadata file:
The dataset_description file is in a different structure from the others.
Use ``dataset.set_field(category="metadata", element="Metadata Version", header="Value", value="testValue")`` to update ``dataset_description``,
and use ``dataset.append(category="subjects", row={"subject id": "test_id"})`` to append a row to other metadata files

Where

   * ``category``: the name of the metadata file
   * ``element``: SPARC element. It is also the first column in table (i.e. the index column)
   * ``header``: the first row is set to be the header
   * ``value``: the value to be set/update
   * ``row``: this parameter need to be in the Python dictionary format. It contains the mapping between the field name and its value

.. literalinclude:: ../../examples/update_dataset.py
      :language: python

Extracting metadata from dicom
------------------------------

A convenience function ``metadata = extract_metadata_from_dcm(dcm_path, target_tags=target_tags)`` can help with extracting all the metadata or the user-specified tags from the dicom files.
Run ``extract_metadata_from_dcm.py`` to see how it works.
This example will extract the metadata from an example dicom file (data retrieved from `DICOM Library <https://www.dicomlibrary.com/?manage=feb6447a72c9a0a31e1bb4459e547964>`_) to a Python dictionary  in the structure of ``{"tag_name_1": "value", "tag_name_N": "value"}``.

.. literalinclude:: ../../examples/extract_metadata_from_dcm.py
      :language: python


Workflow example
----------------

This example shows how to apply the metadata module to a data processing workflow.
Run ``workflow_example_1.py`` to see how it works.
The example script will create a dummy workflow object and the metadata dataset in the SPARC structure in ``./examples/temp/``.
Then import only one data processing script to the workflow.
Here we assume the import script will import all the dicom files in a folder and extract the metadata from these dicom files. Then update the metadata dataset using the extracted values.
This is where the Metadata Manager module comes in.

.. literalinclude:: ../../examples/workflow_example_1.py
      :language: python


