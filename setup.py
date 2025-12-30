from setuptools import setup, find_packages

setup(
    name="sify-langfuse-sdk",
    version="0.1.0",
    description="Standalone Langfuse SDK for manual, model-agnostic observability",
    long_description=open("README.md", encoding="utf-8").read(),
    long_description_content_type="text/markdown",
    author="Sify Technologies",
    author_email="engineering@sify.com",
    url="https://github.com/<org-or-user>/sify-langfuse-sdk",
    packages=find_packages(exclude=("tests", "examples")),
    python_requires=">=3.9",
    install_requires=[
       "langfuse>=2.0.0",
       "python-dotenv>=1.0.0",
   ],

    classifiers=[
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "License :: Other/Proprietary License",
        "Operating System :: OS Independent",
    ],
    keywords=[
        "langfuse",
        "observability",
        "llm",
        "tracing",
        "monitoring",
    ],
    include_package_data=True,
)
