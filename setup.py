import pathlib
from setuptools import setup

# The directory containing this file
HERE = pathlib.Path(__file__).parent

# The text of the README file
README = (HERE / "README.md").read_text()

# This call to setup() does all the work
setup(
    name="av-tweet-ingestion",
    version="1.0.2",
    description="Ingests tweets using Twitter's RecentAPI.",
    long_description=README,
    long_description_content_type="text/markdown",
    url="https://github.com/andreveit/av-tweet-ingestion",
    author="Andre Veit",
    author_email="andrev.veit@gmail.com",
    license="MIT",
    classifiers=[
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.10",
    ],
    packages=['ingestion'
                ],
    include_package_data=True,
    install_requires=["feedparser", "html2text",
                'requests'
                ,'botocore'
                ,'backoff'
                ,'boto3'
                ,'python-dotenv'
                ,'ratelimit']
)
