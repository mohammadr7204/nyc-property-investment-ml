from setuptools import setup, find_packages
import os

# Read README for long description
with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

# Read requirements
with open("requirements.txt", "r", encoding="utf-8") as fh:
    requirements = [line.strip() for line in fh if line.strip() and not line.startswith("#")]

# Read version from src/__init__.py
def get_version():
    version_file = os.path.join("src", "__init__.py")
    with open(version_file, "r", encoding="utf-8") as f:
        for line in f:
            if line.startswith("__version__"):
                return line.split('"')[1]
    return "1.0.0"

setup(
    name="nyc-property-investment-ml",
    version=get_version(),
    author="Mohammad R",
    author_email="mohammadr7204@gmail.com",
    description="AI-powered NYC property investment analysis with ML-based rental revenue prediction",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/mohammadr7204/nyc-property-investment-ml",
    project_urls={
        "Bug Tracker": "https://github.com/mohammadr7204/nyc-property-investment-ml/issues",
        "Documentation": "https://github.com/mohammadr7204/nyc-property-investment-ml#readme",
        "Source Code": "https://github.com/mohammadr7204/nyc-property-investment-ml",
    },
    packages=find_packages(),
    classifiers=[
        "Development Status :: 4 - Beta",
        "Intended Audience :: Financial and Insurance Industry",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Topic :: Office/Business :: Financial :: Investment",
        "Topic :: Scientific/Engineering :: Artificial Intelligence",
        "Topic :: Software Development :: Libraries :: Python Modules",
    ],
    python_requires=">=3.8",
    install_requires=requirements,
    extras_require={
        "dev": [
            "pytest>=7.4.0",
            "pytest-cov>=4.1.0",
            "black>=23.0.0",
            "flake8>=6.0.0",
            "isort>=5.12.0",
            "bandit>=1.7.5",
            "safety>=2.3.0",
        ],
        "notebook": [
            "jupyter>=1.0.0",
            "ipykernel>=6.25.0",
            "notebook>=7.0.0",
        ],
        "web": [
            "flask>=2.3.0",
            "fastapi>=0.103.0",
            "uvicorn>=0.23.0",
            "streamlit>=1.25.0",
        ],
        "viz": [
            "plotly>=5.17.0",
            "folium>=0.14.0",
            "dash>=2.14.0",
        ],
    },
    entry_points={
        "console_scripts": [
            "nyc-property-analyze=scripts.run_analysis:main",
            "nyc-property-setup=scripts.setup_project:main",
            "nyc-property-test=scripts.test_system:main",
        ],
    },
    package_data={
        "src": ["*.py"],
        "scripts": ["*.py"],
    },
    include_package_data=True,
    zip_safe=False,
    keywords=[
        "real-estate", "machine-learning", "investment", "nyc", 
        "rental-prediction", "property-analysis", "ai", "finance"
    ],
)
