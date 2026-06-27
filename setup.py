from setuptools import setup

setup(
    name="hellhound-spider",
    version="13.16",
    description="Autonomous web crawler and recon engine for security testing — SPA + Non-SPA crawling, header analysis, subdomain enumeration, and intelligence classification",
    author="Sree Danush S",
    author_email="lazzer@gmail.com",
    url="https://github.com/project-hellhound-org/hellhound-spider",
    py_modules=["spider"],
    data_files=[
        ("share/man/man1", ["man/spider.1"]),
    ],
    python_requires=">=3.10",
    install_requires=[
        "aiohttp>=3.9.0",
        "beautifulsoup4>=4.12.0",
        "lxml>=5.0.0",
    ],
    extras_require={
        "spa": [
            "playwright>=1.40.0",
            "playwright-stealth>=1.0.6",
            "patchright>=0.5.0",
        ],
    },
    entry_points={
        "console_scripts": [
            "spider=spider:main",
        ],
    },
    classifiers=[
        "Programming Language :: Python :: 3",
        "Intended Audience :: Information Technology",
        "Topic :: Security",
        "Operating System :: OS Independent",
    ],
)
