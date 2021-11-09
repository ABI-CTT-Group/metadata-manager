from physiome_metadata.core.dataset import Dataset

if __name__ == '__main__':
    dataset = Dataset()

    # List categories()
    categories = dataset.list_categories()
    print(categories)

    # List fields
    # Horizontal: - first row
    fields = dataset.list_fields("dataset_description", axis=0)
    # Vertical: first column
    fields = dataset.list_fields("subjects", axis=1)


