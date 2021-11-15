from pathlib import Path

import pydicom


def load_single_dcm(path):
    """
    Load a single dicom file

    :param path: path to the dicom file
    :type path: string
    :return: an instance of FileDataset that represents a parsed DICOM file.
    :rtype: FileDataset
    """
    path = Path(path)
    file_path = None
    if path.is_file():
        file_path = path
    elif path.is_dir():
        for p in path.iterdir():
            if p.is_file():
                file_path = p
        if not file_path:
            msg = "Dicom file not found"
            raise ValueError(msg)
    if file_path.is_file():
        try:
            dcm = pydicom.read_file(file_path)
        except Exception as e:
            raise Exception(str(e))
    return dcm


def extract_metadata_from_dcm(path, target_tags=None):
    """
    Extract metadata from dicom

    :param path: path to the dicom image. It can be a single file or a folder
    :type path: string
    :param target_tags: optional. if provided, will only extract the metadata for the provided tags.
                        This needs to be in the dictionary format with dicom key and tag pair, e.g. {'name': '0x10, 0x10'}
    :type target_tags: dict
    :return: metadata from the dicom file
    :rtype: dict
    """
    metadata = dict()

    dcm = load_single_dcm(path)

    if target_tags:
        if not isinstance(target_tags, dict):
            msg = "target_tags has to be in dictionary format. e.g. {'name': '0x10, 0x10'}"
            raise TypeError(msg)
        # loop through only the target tags
        for key, tag in target_tags.items():
            try:
                value = dcm[tag].value
            except Exception:
                # skip if value not found
                continue
            metadata[key] = value
    else:
        # loop through all the tags
        for element in dcm:
            key = element.keyword
            value = element.value

            metadata[key] = value

    return metadata
