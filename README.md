# metadata-manager

Python module for generating and managing metadata in the [SPARC Dataset structure](https://sparc.science/help/3FXikFXC8shPRd8xZqhjVT).
See the documentation for more information.

## Dependencies

See requirements.txt for python dependencies.
The python module named parameterized is used for testing.

### Install dependencies

```
pip install -r requirements.txt
```

## Accessing documentation

The documentation is hosted on Readthedocs - add link

The documentation is hosted on an ABI webserver that is accessible only within
the university or via VPN - add link

## Building documentation locally

### From the terminal
1. Clone the repository to your local machine.

2. Navigate to the docs/

3. Issue the command: `make html`

4. Open the index.html file in `docs/build/` folder

See the following [instructions](https://research-software-development-tutorials.readthedocs.io/en/latest/beginner/documenting_code/updating_documentation.html#updating-documentation) for more information regarding updating documentation.

## Contributing to documentation

### Updating the documentation
1. Fork this repository from an upstream repository to your github account (An Upstream repository is the Parent/Original repository from where you forked your repository)

2. Edit the restructuredText (.rst) or markdown (.md) files in the 
`docs/sources` folder (editing of these files can performed directly using the 
file editing tools provided by github. This will allow you to commit your 
changes to the repository.

3. Make a pull request from your fork to the master branch of the Upstream repository.

4. Your changes will be reviewed and pulled into the Upstream repository.

Over time, your fork may become out of sync with the master branch of the Upstream repository. Create a pull request on your fork to pull in the latest changes from the master branch of the Upstream repository to get your fork back up-to-date. This can be performed directly on the github website.

## Resources/references

- The SPARC dataset template in ./metadata_manager/resources/templates is retrieved from [this repository](https://github.com/SciCrunch/sparc-curation).
- The example dicom image ./examples/resources/series-000001 is retrieved from [DICOM Library](https://www.dicomlibrary.com/?manage=feb6447a72c9a0a31e1bb4459e547964)
