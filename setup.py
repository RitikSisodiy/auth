import setuptools

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setuptools.setup(
    name="register",
    version="v0.0.1",
    install_requires=[
        "Django", 
        "redis",
        "requests",
        "djangorestframework",
    ],
    author="<your-name>",
    author_email="<your-email>",
    description="Django project",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/<your-github-handle>/<your-repo>",
    project_urls={
        "Bug Tracker": "https://github.com/<your-github-handle>/<your-repo>/issues",
    },
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    package_dir={"": "."},
    packages=setuptools.find_packages(where="."),
    python_requires=">=3.9"
)