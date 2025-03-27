from setuptools import setup, find_packages

setup(
    name="ethicsupply",
    version="1.0.0",
    description="Ethical AI Supply Chain Optimizer",
    author="Mohammad Afsharfar",
    author_email="mohammad.afsharfar@example.com",
    packages=find_packages(),
    install_requires=[
        "PyQt6>=6.4.0",
        "pandas>=1.5.0",
        "numpy>=1.21.0",
        "plotly>=5.13.0",
        "tensorflow>=2.12.0",
        "scikit-learn>=1.0.0",
    ],
    python_requires=">=3.8",
    entry_points={
        "console_scripts": [
            "ethicsupply=src.main:main",
        ],
    },
    classifiers=[
        "Development Status :: 4 - Beta",
        "Intended Audience :: Business/Industry",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Topic :: Office/Business",
    ],
) 