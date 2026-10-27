from setuptools import setup, find_packages

setup(
    name="manim-brand-icons",
    version="0.1.0",
    description="Offline and dynamic brand icon assets for Manim Community using simplepycons and Brandfetch/Clearbit",
    author="Manim Community Contributor",
    packages=find_packages(),
    install_requires=[
        "simplepycons>=1.16.0",
        "requests>=2.28.0",
        "cairosvg>=2.7.0"
    ],
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
    ],
    python_requires=">=3.8",
)
