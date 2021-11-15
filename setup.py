import setuptools
from os.path import join, abspath, dirname

with open("README.md", "r", encoding="utf-8") as fh:
    LONG_DESCRIPTION = fh.read()


with open(join(abspath(dirname(__file__)), 'VERSION'), 'r') as f:
    VERSION = f.read().strip()


DEPENDENCIES = [
    "Glymur",
    "numpy"
]

setuptools.setup(
    name="sat-mapping-cyborg-ai",
    version=VERSION,
    author="Lukas Ikle",
    author_email="lukas.ikle@itweet.ch",
    description="A package to fetch sentinel 2 Satellite data from Google.",
    long_description=LONG_DESCRIPTION,
    long_description_content_type="text/markdown",
    url="https://github.com/iklelukas/sat_mapping",
    project_urls={
        "Bug Tracker": "https://github.com/iklelukas/sat_mapping/issues",
    },
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    package_dir={"": "src"},
    packages=setuptools.find_packages(where="src"),
    python_requires=">=3.6",
    include_package_data=True,
    install_requires=DEPENDENCIES
)
