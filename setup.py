from setuptools import setup, find_packages

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setup(
    name="coexum",
    version="0.1.0-rc1",
    description="Rede descentralizada de computação em IA",
    long_description=long_description,
    long_description_content_type="text/markdown",
    author="Potiguar AI Lab",
    author_email="contato@coexum.org",
    url="https://github.com/potiguarailab/coexum",
    packages=find_packages(exclude=["tests", "docs"]),
    entry_points={
        "console_scripts": [
            "coexum=agent.cli:cli",
        ],
    },
    install_requires=[
        "typer>=0.6",
        "psutil>=5.9",
        "fastapi>=0.85",
        "uvicorn[standard]>=0.18",
        "websockets>=10.4",
        "requests>=2.28",
        "web3>=6.0",
        "docker>=6.0",
        "pydantic>=2.0",
        "pydantic-settings>=2.0",
        "python-jose[cryptography]>=3.3.0",
        "passlib[bcrypt]>=1.7.4",
        "python-multipart>=0.0.5",
        "PyJWT>=2.8.0",
    ],
    extras_require={
        "dev": [
            "pytest>=7.0",
            "pytest-cov>=4.0",
            "black>=22.0",
            "isort>=5.0",
            "mypy>=1.0",
            "ruff>=0.1.0",
        ],
        "docs": [
            "mkdocs>=1.4",
            "mkdocs-material>=9.0",
        ],
    },
    python_requires=">=3.10",
    classifiers=[
        "Development Status :: 4 - Beta",
        "Intended Audience :: Science/Research",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Programming Language :: Python :: 3.12",
        "Topic :: Scientific/Engineering :: Artificial Intelligence",
    ],
    project_urls={
        "Documentation": "https://coexum.org/docs",
        "Source": "https://github.com/potiguarailab/coexum",
        "Issues": "https://github.com/potiguarailab/coexum/issues",
    },
)
