"""
This example workflow uses the physiome_metadata module for the metadata management
Only one workflow step (import scan) involved here.
"""
import os
from pathlib import Path

from physiome_metadata import Dataset
from physiome_metadata import extract_metadata_from_dcm


def import_scan(dicom_dir, metadata_dir):
    # Extracting metadata
    metadata = extract_metadata_from_dcm(dicom_dir)

    # Writing/updating metadata
    dataset = Dataset()
    dataset.load_dataset(metadata_dir)
    row = {
        "subject id": metadata.get("PatientID"),
        "age": metadata.get("PatientAge"),
        "species": "human",
        "strain": "n/a"
    }
    dataset.append("subjects", row)
    dataset.save_dataset(metadata_dir)

    files = os.listdir(dicom_dir)
    for file in files:
        print("Importing " + str(file))

    print("Imported all dicom files")


class Workflow:
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
        "Metadata Version"
        self._metadata_dataset.set_field("dataset_description", element="Metadata Version", header="Value", value="2.0.0")
        self._metadata_dataset.set_field("dataset_description", element="    Title", header="Value", value="Test Project")
        self._metadata_dataset.save_dataset(metadata_dir)

    def import_script(self, script_path):
        self._scripts.append(script_path)
        print("Script imported")

    def run(self, dicom_dir, metadata_dir):
        # assume there is only one workflow component/script to run
        import_scan(dicom_dir, metadata_dir)


if __name__ == '__main__':
    dicom_dir = "./resources/series-000001"
    metadata_dir = Path(__file__).parent.resolve() / "./tmp/dataset"
    # 1. create workflow
    workflow = Workflow()
    workflow.initialise_metadata(metadata_dir)
    # 2. import workflow component/script
    script_path = "/path/to/workflow/script.py"
    workflow.import_script(str(script_path))
    # 3. trigger workflow
    workflow.run(dicom_dir=dicom_dir, metadata_dir=metadata_dir)
