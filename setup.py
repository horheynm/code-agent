import os
from setuptools import setup, find_packages

is_release: bool = str(os.getenv("IS_RELEASE", "False")).lower() in ("true", "1", "t")


def read_version():
    with open("VERSION") as version_file:
        version = version_file.read().strip()
        if is_release:
            version = version.split("a")[0]
        return version


def get_package_name():
    name = "small-agent"
    if is_release:
        return name
    return name + "-nightly"


required_packages = [
    "openai==1.35.7",
    "pydantic==2.7.4",
]

extra_reqs = {
    "dev": [
        "pydantic==2.7.4",
        "pytest==8.2.2",
        "black==24.4.2",
        "ruff==0.5.0",
    ]
}

setup(
    name=get_package_name(),  # Set package name based on release status
    version=read_version(),  # Read version from VERSION file
    author="George",
    author_email="george.scratch.dev@gmail.com",
    license="Apache 2.0",
    description="Code generation LLM agent for fast prototyping",
    package_dir={"": "src"},
    packages=find_packages("src", include=["code_agent"]),
    install_requires=required_packages,
    extras_require=extra_reqs,
)
