from pathlib import Path

from metadata_manager import extract_metadata_from_dcm


if __name__ == '__main__':
    dcm_path = Path(__file__).parent.resolve() / "./resources/series-000001/image-000001.dcm"
    dcm_path = Path(__file__).parent.resolve() / "./resources/series-000001/"

    # Extracting all tags
    metadata = extract_metadata_from_dcm(dcm_path)
    print(metadata)

    # Extracting only a few tags
    target_tags = {
        'name': (0x10, 0x10),
        'id': (0x10, 0x20),
        'birth_date': (0x0010, 0x0030),
        'gender': (0x0010, 0x0040),
        'age': (0x0010, 0x1010),
        'height': (0x0010, 0x1020),
        'weight': (0x0010, 0x1030)
    }
    metadata = extract_metadata_from_dcm(dcm_path, target_tags=target_tags)
    print(metadata)
