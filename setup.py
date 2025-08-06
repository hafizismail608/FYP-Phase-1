from setuptools import setup, find_packages

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setup(
    name="translearn-lms",
    version="1.0.0",
    author="TransLearn Team",
    author_email="support@translearn.com",
    description="An AI-powered Learning Management System",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/yourusername/translearn-lms",
    packages=find_packages(),
    include_package_data=True,
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Framework :: Flask",
        "Intended Audience :: Education",
        "Topic :: Education",
    ],
    python_requires=">=3.8",
    install_requires=[
        "flask>=2.0.0",
        "flask-login>=0.5.0",
        "flask-sqlalchemy>=2.5.0",
        "flask-wtf>=1.0.0",
        "flask-migrate>=3.0.0",
        "email_validator>=1.1.0",
        "flask-seasurf>=1.0.0",
        "flask-talisman>=1.0.0",
        "passlib>=1.7.0",
        "pyjwt>=2.0.0",
        "python-dotenv>=0.19.0",
        "pillow>=8.0.0",
        "numpy>=1.20.0",
        "google-generativeai>=0.1.0",
    ],
    entry_points={
        "console_scripts": [
            "translearn=run:main",
        ],
    },
)