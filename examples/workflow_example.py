"""
This example workflow uses the metadata_manager module for the metadata management.
Have a look and run the main function to see how the metadata is generated and updated to the SPARC dataset structure.
"""

import os
from pathlib import Path

from metadata_manager import Dataset
from metadata_manager import extract_metadata_from_dcm


def import_scan(dicom_dir, metadata_dir):
    """
    Pretend to move/copy the dicom files into a workspace (a folder to store the results from a workflow step).
    Then extract the metadata from the dicom headers and save it to the SPARC metadata file - subjects.xlsx
    """

    files = os.listdir(dicom_dir)
    for file in files:
        print("Importing " + str(file))

    print("Imported all dicom files")

    # Extracting metadata
    metadata = extract_metadata_from_dcm(dicom_dir)

    # Writing/updating metadata
    dataset = Dataset()
    dataset.load_dataset(metadata_dir)
    # Append a row in dictionary format into a specified SPARC metadata file
    # Here, a new row will be added to the subject metadata file
    # the dictionary keys are the SPARC elements/column names in the metadata file,
    # while the dictionary values are the dicom tags extracted from the dicom headers or the user specified values.
    row = {
        "subject id": metadata.get("PatientID"),
        "age": metadata.get("PatientAge"),
        "species": "human",
        "strain": "n/a"
    }
    dataset.append("subjects", row)
    dataset.save_dataset(metadata_dir)

    return "/path/to/the/imported/scan/dir"


class Workflow(object):
    def __init__(self):
        self._scripts = list()
        self._metadata_dataset = None
        print("Workflow initialisation - done")

    def initialise_metadata(self, metadata_dir):
        if not os.path.isdir(metadata_dir):
            os.makedirs(metadata_dir)

        self._metadata_dataset = Dataset()
        self._metadata_dataset.save_template(metadata_dir)

        self._metadata_dataset.load_dataset(metadata_dir)

        self._metadata_dataset.set_field("dataset_description", element="Metadata Version", header="Value", value="2.0.0")
        self._metadata_dataset.set_field("dataset_description", element="    Title", header="Value", value="Test Project")
        self._metadata_dataset.save_dataset(metadata_dir)

    def import_script(self, script_path, code_description=dict()):
        self._scripts.append(script_path)
        self._metadata_dataset.append("code_description", code_description)
        self._metadata_dataset.save_dataset(metadata_dir)
        print("Script imported")

    def run(self, dicom_dir, metadata_dir):
        # assume there is only one workflow component/script to run
        workspace_1 = import_scan(dicom_dir, metadata_dir)


if __name__ == '__main__':
    dicom_dir = "./resources/series-000001"
    metadata_dir = Path(__file__).parent.resolve() / "./tmp/dataset"
    # Create workflow
    workflow = Workflow()
    workflow.initialise_metadata(metadata_dir)
    # Import workflow component/script
    workflow.import_script("/path/to/workflow/script/import_scan.py",
                           code_description={"Metadata element": "import_scan",
                                             "Description": "Import dicom files and extract metadata from dicom headers",
                                             "Example": None,
                                             "Value": None})
    # Trigger workflow
    workflow.run(dicom_dir=dicom_dir, metadata_dir=metadata_dir)
