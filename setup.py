import setuptools

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setuptools.setup(
    name="viggy-3d",
    version="0.0.1",
    author="Vignesh M Pai",
    author_email="vigneshpai2003@gmail.com",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/vigneshpai2003/viggy-3d",
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    package_dir={"": "src"},
    packages=setuptools.find_packages(where="src"),
    python_requires=">=3.8",
)