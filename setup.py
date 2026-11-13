from setuptools import setup, find_packages

setup(
    name="isomorph",
    version="1.0.0",
    author="Subrat Sahu",
    author_email="subratsahu195@gmail.com",
    description="Cross-Disciplinary Structural Isomorphism & Dialectic Discovery Engine for Scientific Breakthroughs",
    long_description=open("README.md", encoding="utf-8").read(),
    long_description_content_type="text/markdown",
    url="https://github.com/subratsahu3/isomorph",
    packages=find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Topic :: Scientific/Engineering :: Artificial Intelligence",
        "Topic :: Scientific/Engineering :: Information Analysis",
    ],
    python_requires=">=3.9",
    install_requires=[],
    extras_require={
        "accelerated": ["networkx>=3.0", "numpy>=1.24.0"],
    },
    entry_points={
        "console_scripts": [
            "isomorph=isomorph.cli.main:main",
        ],
    },
    include_package_data=True,
    package_data={
        "isomorph": ["web/*.html"],
    },
)
