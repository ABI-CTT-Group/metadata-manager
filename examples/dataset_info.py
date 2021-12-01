from metadata_manager import Dataset

if __name__ == '__main__':
    dataset = Dataset()

    # List categories()
    categories = dataset.list_categories()
    print(categories)

    # List fields
    # Horizontal: first row
    fields = dataset.list_elements(category="dataset_description")
    # Vertical: first column
    fields = dataset.list_elements(category="subjects")


