from setuptools import setup, find_packages

setup(
    name="monte-carlo-decision-engine",
    version="1.0.0",
    description="Asistente de Toma de Decisiones Empresariales con Simulaciones Monte Carlo",
    author="Sistema de IA",
    packages=find_packages(),
    install_requires=[
        "numpy>=1.24.3",
        "scipy>=1.11.1", 
        "pandas>=2.0.3",
        "matplotlib>=3.7.2",
        "seaborn>=0.12.2",
        "flask>=2.3.2",
        "plotly>=5.15.0",
        "dash>=2.11.1",
        "dash-bootstrap-components>=1.4.1"
    ],
    python_requires=">=3.8",
    entry_points={
        'console_scripts': [
            'monte-carlo-engine=main:main',
        ],
    },
    classifiers=[
        "Development Status :: 4 - Beta",
        "Intended Audience :: End Users/Desktop",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
    ],
)