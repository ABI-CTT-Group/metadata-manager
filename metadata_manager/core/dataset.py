import os
import shutil
from pathlib import Path
from distutils.dir_util import copy_tree

import pandas as pd
from xlrd import XLRDError


class Dataset(object):
    def __init__(self):
        self._template_version = "2.0.0"  # default
        self._version = self._template_version
        self._current_path = Path(__file__).parent.resolve()
        self._resources_path = Path.joinpath(self._current_path, "../resources")
        self._template_dir = Path()
        self._template = dict()

        self._dataset_path = Path()
        self._dataset = dict()
        self._metadata_extensions = [".xlsx"]

    def set_dataset_path(self, path):
        """
        Set the path to the dataset

        :param path: path to the dataset directory
        :type path: string
        """
        self._dataset_path = Path(path)

    def get_dataset_path(self):
        """
        Return the path to the dataset directory
        :return: path to the dataset directory
        :rtype: string
        """
        return str(self._dataset_path)

    def _get_template_dir(self, version):
        """
        Get template directory path

        :return: path to the template dataset
        :rtype: Path
        """
        version = "version_" + version
        template_dir = self._resources_path / "templates" / version / "DatasetTemplate"

        return template_dir

    def set_template_version(self, version):
        """
        Choose a template version

        :param version: template version
        :type version: string
        """
        version = version.replace(".", "_")
        self._template_version = version

    def _load(self, dir_path):
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
                    metadata = pd.read_excel(path)
                except XLRDError:
                    metadata = pd.read_excel(path, engine='openpyxl')

                metadata = metadata.dropna(how="all")
                metadata = metadata.loc[:, ~metadata.columns.str.contains('^Unnamed')]

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

    def load_from_template(self, version):
        """
        Load dataset from SPARC template

        :param version: template version
        :type version: string
        :return: loaded dataset
        :rtype: dict
        """
        self.set_version(version)
        self._dataset_path = self._get_template_dir(self._version)
        self._dataset = self._load(str(self._dataset_path))

        return self._dataset

    def _convert_version_format(self, version):
        """
        Convert version format
        :param version: dataset/template version
        :type version: string
        :return: version in the converted format
        :rtype:
        """
        version = version.replace(".", "_")

        if "_" not in version:
            version = version + "_0_0"

        return version

    def set_version(self, version):
        """
        Set dataset version version

        :param version: dataset version
        :type version: string
        """
        version = self._convert_version_format(version)

        self._version = version

    def load_template(self, version):
        """
        Load template

        :param version: template version
        :type version: string
        :return: loaded template
        :rtype: dict
        """

        version = self._convert_version_format(version)
        self.set_template_version(version)
        self._template_dir = self._get_template_dir(self._template_version)
        self._template = self._load(str(self._template_dir))

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
            version = self._convert_version_format(version)
            template_dir = self._get_template_dir(version)
        elif not version and self._template_version:
            template_dir = self._get_template_dir(self._template_version)
        else:
            raise ValueError("Template path not found.")

        copy_tree(str(template_dir), str(save_dir))

    def load_dataset(self, dataset_path=None, from_template=False, version=None):
        """
        Load the input dataset into a dictionary

        :param dataset_path: path to the dataset
        :type dataset_path: string
        :param from_template: whether to load the dataset from a SPARC template
        :type from_template: bool
        :param version: dataset version
        :type version: string
        :return: loaded dataset
        :rtype: dict
        """
        if from_template:
            self._dataset = self.load_from_template(version=version)
        else:
            self._dataset = self._load(dataset_path)

        return self._dataset

    def save(self, save_dir, remove_empty=False):
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
            save_dir.mkdir(parents=True, exist_ok=False)

        for key, value in self._dataset.items():
            if isinstance(value, dict):
                file_path = Path(value.get("path"))
                filename = file_path.name
                data = value.get("metadata")

                if remove_empty:
                    data = self._filter(data, filename)

                if isinstance(data, pd.DataFrame):
                    data.to_excel(Path.joinpath(save_dir, filename), index=False)

            elif Path(value).is_dir():
                dir_name = Path(value).name
                dir_path = Path.joinpath(save_dir, dir_name)
                copy_tree(str(value), str(dir_path), update=1)

            elif Path(value).is_file():
                filename = Path(value).name
                file_path = Path.joinpath(save_dir, filename)
                try:
                    shutil.copyfile(value, file_path)
                except shutil.SameFileError:
                    # overwrite file by copy, remove then rename
                    file_path_tmp = str(file_path) + "_tmp"
                    shutil.copyfile(value, file_path_tmp)
                    os.remove(file_path)
                    os.rename(file_path_tmp, file_path)

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
            metadata = pd.read_excel(path)
        except XLRDError:
            metadata = pd.read_excel(path, engine='openpyxl')

        filename = path.stem
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

    def list_categories(self, version):
        """
        list all categories based on the metadata files in the template dataset

        :param version: reference template version
        :type version: string
        :return: all metadata categories
        :rtype: list
        """
        categories = list()

        self.load_template(version=version)

        for key, value in self._template.items():
            if isinstance(value, dict):
                file_path = Path(value.get("path"))
                category = file_path.stem
                categories.append(category)

        print("Categories:")
        for category in categories:
            print(category)

        return categories

    def list_elements(self, category, axis=0, version=None):
        """
        List field from a metadata file

        :param category: metadata category
        :type category: string
        :param axis: If axis=0, column-based. list all column headers. i.e. the first row.
                     If axis=1, row-based. list all row index. i.e. the first column in each row
        :type axis: int
        :param version: reference template version
        :type version: string
        :return: a list of fields
        :rtype: list
        """
        fields = None

        if category == "dataset_description":
            axis = 1

        if version:
            version = self._convert_version_format(version)
            template_dir = self._get_template_dir(version)

            element_description_file = template_dir / "../element_descriptions.xlsx"

            try:
                element_description = pd.read_excel(element_description_file, sheet_name=category)
            except XLRDError:
                element_description = pd.read_excel(element_description_file, sheet_name=category, engine='openpyxl')

            print("Category: " + str(category))
            for index, row in element_description.iterrows():
                print(str(row["Element"]))
                print("    Type: " + str(row["Type"]))
                print("    Description: " + str(row["Description"]))
                print("    Example: " + str(row["Example"]))

            fields = element_description.values.tolist()
            return fields

        if not self._template:
            self.load_template(version=None)

        data = self._template.get(category)
        metadata = data.get("metadata")
        # set the first column as the index column
        metadata = metadata.set_index(list(metadata)[0])
        if axis == 0:
            fields = list(metadata.columns)
        elif axis == 1:
            fields = list(metadata.index)

        print("Fields:")
        for field in fields:
            print(field)

        return fields

    def set_field(self, category, row_index, header, value):
        """
        Set single field by row idx/name and column name (the header)

        :param category: metadata category
        :type category: string
        :param row_index: row index in excel. Excel index starts from 1 where index 1 is the header row. so actual data index starts from 2
        :type row_index: int
        :param header: column name. the header is the first row
        :type header: string
        :param value: field value
        :type value: string
        :return: updated dataset
        :rtype: dict
        """
        if not self._dataset:
            msg = "Dataset not defined. Please load the dataset in advance."
            raise ValueError(msg)

        metadata = self._dataset.get(category).get("metadata")

        if not isinstance(row_index, int):
            msg = "Value error. Row index should be int."
            raise ValueError(msg)

        try:
            # Convert excel row index to dataframe index: index - 2
            row_index = row_index - 2
            metadata.loc[row_index, header] = value
        except ValueError:
            msg = "Value error. row does not exists."
            raise ValueError(msg)

        self._dataset[category]["metadata"] = metadata

        return self._dataset

    def append(self, category, row):
        """
        Append a row to a metadata file

        :param category: metadata category
        :type category: string
        :param row: a row to be appended
        :type row: dic
        :return: updated dataset
        :rtype: dict
        """
        if not self._dataset:
            msg = "Dataset not defined. Please load the dataset in advance."
            raise ValueError(msg)

        metadata = self._dataset.get(category).get("metadata")
        metadata = metadata.append(row, ignore_index=True)

        self._dataset[category]["metadata"] = metadata

        return self._dataset
