from setuptools import setup, find_packages

with open("requirements.txt") as f:
	install_requires = f.read().strip().split("\n")

# get version from __version__ variable in conceptual/__init__.py
from conceptual import __version__ as version

setup(
	name="conceptual",
	version=version,
	description="Conceptual Drilling",
	author="Jigar Tarpara",
	author_email="team@khatavahi.in",
	packages=find_packages(),
	zip_safe=False,
	include_package_data=True,
	install_requires=install_requires
)
