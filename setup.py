from setuptools import setup, find_packages

setup(
    name="coexum",
    version="0.1.0",
    description="Rede descentralizada de IA - Potiguar AI Lab",
    packages=find_packages(exclude=['tests', 'docs']),
    entry_points={
        'console_scripts': [
            'coexum=agent.cli:main',
        ],
    },
    install_requires=[
        'typer>=0.6',
        'psutil>=5.9',
        'fastapi>=0.85',
        'uvicorn>=0.18',
        'websockets>=10.4',
        'requests>=2.28',
        'web3>=6.0',
        'docker>=6.0',
        'pydantic>=1.10'
    ],
    python_requires='>=3.10',
)
