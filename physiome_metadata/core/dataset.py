import shutil
from pathlib import Path


class Dataset(object):
    def __init__(self):
        self._template_version = "2.0.0"  # default
        self._current_path = Path(__file__).parent.resolve()
        self._resources_path = Path.joinpath(self._current_path, "../resources")
        self._template_dir = Path()

        self.set_template()

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
