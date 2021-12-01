from metadata_manager import Dataset

if __name__ == '__main__':
    dataset = Dataset()

    # List categories()
    categories = dataset.list_categories()
    print(categories)

    # List SPARC elements
    elements = dataset.list_elements(category="dataset_description")
    elements = dataset.list_elements(category="subjects")


