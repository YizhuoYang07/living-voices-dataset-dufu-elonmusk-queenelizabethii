from setuptools import setup, find_packages

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

with open("requirements.txt", "r", encoding="utf-8") as fh:
    requirements = [line.strip() for line in fh if line.strip() and not line.startswith("#")]

setup(
    name="living-voices-dataset",
    version="1.0.0",
    author="Living Voices Team",
    author_email="living-voices-team@uts.edu.au",
    description="A multilingual dataset for persona-based conversational AI systems",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/living-voices/living-voices-dataset",
    project_urls={
        "Bug Tracker": "https://github.com/living-voices/living-voices-dataset/issues",
        "Documentation": "https://living-voices-dataset.readthedocs.io/",
        "Source Code": "https://github.com/living-voices/living-voices-dataset",
    },
    packages=find_packages(where="tools"),
    package_dir={"": "tools"},
    classifiers=[
        "Development Status :: 4 - Beta",
        "Intended Audience :: Science/Research",
        "Intended Audience :: Education",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Topic :: Scientific/Engineering :: Artificial Intelligence",
        "Topic :: Text Processing :: Linguistic",
    ],
    python_requires=">=3.9",
    install_requires=requirements,
    extras_require={
        "dev": [
            "pytest>=7.1.0",
            "pytest-cov>=3.0.0",
            "black>=22.6.0",
            "isort>=5.10.0",
            "pylint>=2.14.0",
            "mypy>=0.971",
            "pre-commit>=2.20.0",
        ],
        "docs": [
            "sphinx>=5.1.0",
            "sphinx-rtd-theme>=1.0.0",
        ],
        "all": [
            "datasets>=2.4.0",
            "evaluate>=0.2.0",
            "wandb>=0.13.0",
        ],
    },
    entry_points={
        "console_scripts": [
            "living-voices-validate=tools.validation.validate_all:main",
            "living-voices-collect=tools.data_collection.collect:main",
            "living-voices-process=tools.data_processing.process:main",
        ],
    },
    include_package_data=True,
    zip_safe=False,
    keywords=[
        "nlp",
        "dataset",
        "rag",
        "conversational-ai",
        "persona",
        "multilingual",
        "dialogue-systems",
        "information-retrieval",
    ],
)