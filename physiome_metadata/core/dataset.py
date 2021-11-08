import shutil
from pathlib import Path

import pandas as pd
from xlrd import XLRDError


class Dataset(object):
    def __init__(self):
        self._template_version = "2.0.0"  # default
        self._current_path = Path(__file__).parent.resolve()
        self._resources_path = Path.joinpath(self._current_path, "../resources")
        self._template_dir = Path()
        self._template = dict()

        self._dataset_path = Path()
        self._dataset = dict()
        self._metadata_extensions = [".xlsx"]

        self.load_template()

    def set_dataset_path(self, path):
        """
        Set the path to the dataset
        :param path: path to the dataset directory
        :type path: string
        """
        self._dataset_path = Path(path)

    def set_template_version(self, version):
        """
        Choose a template version
        :param version: template version
        :type version: string
        """
        self._template_version = version

    def set_template(self, version=None):
        """
        Set template version & path
        :param version: template version
        :type version: string
        """
        if version:
            self.set_template_version(version)

        version = self._template_version.replace(".", "_")

        if "_" not in version:
            version = version + "_0_0"

        version = "version_" + version
        template_dir = self._resources_path / "templates" / version / "DatasetTemplate"

        self._template_dir = template_dir

    def load(self, dir_path):
        """
        Load the input dataset into a dictionary
        :param dir_path: path to the dataset dictionary
        :type dir_path: string
        :return: loaded dataset
        :rtype: dict
        """
        dataset = dict()

        dir_path = Path(dir_path)
        for path in dir_path.iterdir():
            if path.suffix in self._metadata_extensions:
                try:
                    metadata = pd.read_excel(path, index_col=[0])
                except XLRDError:
                    metadata = pd.read_excel(path, index_col=[0], engine='openpyxl')

                key = path.stem
                value = {
                    "path": path,
                    "metadata": metadata
                }
            else:
                key = path.name
                value = path

            dataset[key] = value

        return dataset

    def load_template(self, version=None):
        """
        Load template
        :param version: template version
        :type version: string
        :return: loaded dataset
        :rtype: dict
        """
        self.set_template(version)
        self._template = self.load(self._template_dir)

        return self._template

    def save_template(self, save_dir, version=None):
        """
        Save the template directory locally
        :param save_dir: path to the output folder
        :type save_dir: string
        :param version: template version
        :type version: string
        """
        if version:
            self.set_template(version)

        shutil.copytree(self._template_dir, save_dir)

    def load_dataset(self, dataset_path):
        """
        Load the input dataset into a dictionary
        :param dataset_path: path to the dataset
        :type dataset_path: string
        :return: loaded dataset
        :rtype: dict
        """
        self._dataset = self.load(dataset_path)

        return self._dataset

    def save_dataset(self, save_dir, remove_empty=False):
        """
        Save dataset
        :param save_dir: path to the dest dir
        :type save_dir: string
        :param remove_empty: (optional) If True, remove rows which do not have values in the "Value" field
        :type remove_empty: bool
        """
        if not self._dataset:
            msg = "Dataset not defined. Please load the dataset or the template dataset in advance."
            raise ValueError(msg)

        save_dir = Path(save_dir)
        if not save_dir.is_dir():
            save_dir.mkdir()

        for key, value in self._dataset.items():
            if isinstance(value, dict):
                file_path = Path(value.get("path"))
                filename = file_path.name
                data = value.get("metadata")

                if remove_empty:
                    data = self._filter(data, filename)

                if isinstance(data, pd.DataFrame):
                    data.to_excel(Path.joinpath(save_dir, filename))

            elif Path(value).is_dir():
                dir_name = Path(value).name
                dir_path = Path.joinpath(save_dir, dir_name)
                shutil.copytree(value, dir_path)

            elif Path(value).is_file():
                filename = Path(value).name
                file_path = Path.joinpath(save_dir, filename)
                shutil.copyfile(value, file_path)

    def load_metadata(self, path):
        """
        Load & update a single metadata
        :param path: path to the metadata file
        :type path: string
        :return: metadata
        :rtype: Pandas.DataFrame
        """
        path = Path(path)
        try:
            metadata = pd.read_excel(path, index_col=[0])
        except XLRDError:
            metadata = pd.read_excel(path, index_col=[0], engine='openpyxl')

        filename = path.name
        self._dataset[filename] = {
            "path": path,
            "metadata": metadata
        }

        return metadata

    def _filter(self, metadata, filename):
        """
        Remove column/row if values not set
        :param metadata: metadata
        :type metadata: Pandas.DataFrame
        :param filename: name of the metadata
        :type filename: string
        :return: updated metadata
        :rtype: Pandas.DataFrame
        """
        if "dataset_description" in filename:
            # For the dataset_description metadata, remove rows which do not have values in the "Value" fields
            metadata = metadata.dropna(subset=["Value"])

        return metadata
