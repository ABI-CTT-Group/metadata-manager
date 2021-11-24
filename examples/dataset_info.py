from metadata_manager import Dataset

if __name__ == '__main__':
    dataset = Dataset()

    # List categories()
    categories = dataset.list_categories()
    print(categories)

    # List fields
    # Horizontal: first row
    fields = dataset.list_fields(category="dataset_description", axis=0)
    # Vertical: first column
    fields = dataset.list_fields(category="subjects", axis=1)


