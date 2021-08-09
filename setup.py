#!/usr/bin/env python

"""The setup script."""

from setuptools import setup, find_packages

with open("README.md") as readme_file:
    readme = readme_file.read()

requirements = ["requests"]

setup_requirements = [
    "pytest-runner",
]

test_requirements = [
    "pytest>=3",
]

setup(
    author="Sahand Seifi",
    author_email="sahand.seifi@gmail.com",
    python_requires=">=3.6",
    classifiers=[
        "Development Status :: 2 - Pre-Alpha",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: MIT License",
        "Natural Language :: English",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
    ],
    description=" NotificationAPI SDK for server-side (back-end) python projects. ",
    install_requires=requirements,
    license="MIT license",
    long_description=readme,
    include_package_data=True,
    keywords="notificationapi_python_server_sdk",
    name="notificationapi_python_server_sdk",
    packages=find_packages(
        include=[
            "notificationapi_python_server_sdk",
            "notificationapi_python_server_sdk.*",
        ]
    ),
    setup_requires=setup_requirements,
    test_suite="tests",
    tests_require=test_requirements,
    url="https://github.com/notificationapi-com/notificationapi_python_server_sdk",
    version="0.0.6",
    zip_safe=False,
)
