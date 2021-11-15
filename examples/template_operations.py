from metadata_manager import Dataset

if __name__ == '__main__':
    dataset = Dataset()
    # Load the SPARC template dataset. source from https://github.com/SciCrunch/sparc-curation
    template = dataset.load_template(version="2.0.0")
    # Save the template dataset
    dataset.save_template(save_dir="./tmp/template/")

