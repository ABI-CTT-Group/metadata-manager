from pathlib import Path

from physiome_metadata.core.dataset import Dataset

if __name__ == '__main__':
    dataset = Dataset()

    # Set dataset path. If the template dataset is already saved in "./tmp/template". you can then do:
    # dataset_dir = "/path/to/dataset/dir"
    dataset_dir = Path(__file__).parent.resolve() / "./tmp/template"

    dataset.load_dataset(dataset_dir)

    # Update a field in the dataset_description metadata file. row=="Metadata Version", column=="Value",
    # and value will be set "testValue"
    dataset.set_field("dataset_description", idx="Metadata Version", header="Value", value="testValue")

    # Append a row to the "subjects" metadata file. "subject id" will be set to "test_id"
    dataset.append("subjects", {"subject id": "test_id"})

    dataset.save_dataset(dataset_dir)
