"""Module setup."""

import os
from setuptools import setup, find_packages

PACKAGE_NAME = "prism_cloudcontroller"

with open(os.path.abspath("openapi-generator/prism-agent-client/README.md"), "r") as fh:
    long_description = fh.read()


def parse_requirements(filename: str):
    """Load requirements from a pip requirements file."""
    lineiter = (line.strip() for line in open(filename))
    return [line for line in lineiter if line and not line.startswith("#")]


if __name__ == "__main__":
    setup(
        name=PACKAGE_NAME,
        version="1.3.0",
        description="A simple python package for controlling an prism agent through the admin-api interface",
        long_description=long_description,
        long_description_content_type="text/markdown",
        url="https://github.com/lohanspies/prism_v2_playground/tree/master/openapi-generator/prism-agent-client/prism_agent_client",
        packages=find_packages(),
        include_package_data=True,
        package_data={
            "openapi-generator/prism-agent-client/prism_agent_client": [
                "requirements.txt",
            ]
        },
        tests_require=parse_requirements("requirements.dev.txt"),
        install_requires=parse_requirements("requirements.txt"),
        python_requires=">=3.8",
        classifiers=[
            "Programming Language :: Python :: 3",
            "License :: OSI Approved :: Apache Software License",
            "Operating System :: OS Independent",
        ],
    )
