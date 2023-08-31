from setuptools import setup

with open("README.md", "r") as fh:
    readme_file = fh.read()

setup(
    name="Kurzschluss Analyser",
    version="1.0.0",
    description="Analyzer Tool um Kurzschluss Messungen von Fahrbahnleitungen zu analysieren",
    long_description=readme_file,
    long_description_content_type="text/markdown",
    author="Matthias Thoma",
    license="MIT",
    classifiers=[
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python",
        "Programming Language :: Python :: 2",
        "Programming Language :: Python :: 3",
    ],
    packages=["kurzschlussanalyzer"],
    include_package_data=True,
    install_requires=[
        "altgraph",
        "contourpy",
        "cycler",
        "fonttools",
        "kiwisolver",
        "macholib",
        "matplotlib",
        "numpy",
        "packaging",
        "pandas",
        "Pillow",
        "pyinstaller",
        "pyinstaller-hooks-contrib",
        "pyparsing",
        "python-dateutil",
        "pytz",
        "six",
        "tzdata"
    ],
    entry_points={"app": ["prog=kurzschlussanalyser:main"]}
)