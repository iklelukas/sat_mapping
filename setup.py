import setuptools

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()


DEPENDENCIES = [
    "wheel",
    "crcmod",
    "lxml",
    "setuptools",
    "numpy",
    "Glymur",
]


GSUTIL_DEPENDENCIES = [
    "argcomplete>=1.9.4",
    "testresources",
    "crcmod>=1.7",
    "fasteners>=0.14.1",
    "gcs-oauth2-boto-plugin>=3.0",
    "google-apitools>=0.5.32",
    "httplib2>=0.18",
    "google-reauth>=0.1.0",
    "monotonic>=1.4",
    "pyOpenSSL>=0.13",
    "retry_decorator>=1.0.0",
    "six>=1.12.0",
]


setuptools.setup(
    name="sat-mapping-cyborg-ai",
    version="0.0.23",
    author="Lukas Ikle",
    author_email="lukas.ikle@itweet.ch",
    description="A package to fetch sentinel 2 Satellite data from Google",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/pypa/sampleproject",
    project_urls={
        "Bug Tracker": "https://github.com/pypa/sampleproject/issues",
    },
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: LINUX",
    ],
    package_dir={"": "src"},
    packages=setuptools.find_packages(where="src"),
    python_requires=">=3.6",
    include_package_data=True,
    install_requires=DEPENDENCIES + GSUTIL_DEPENDENCIES
)
