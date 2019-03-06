import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="lidilite",
    version="0.1",
    author="Kerybas",
    author_email="kerybas@protonmail.com",
    description="Simply write lists of dictionaries into sqlite.",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/Kerybas/Lidilite",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
)