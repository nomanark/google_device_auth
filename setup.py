from setuptools import setup, find_packages

setup(
    name="google_device_auth",
    version="0.1.0",
    author="nomanaark",
    author_email="nomanaark@gmail.com",
    description="A lightweight tool for Google OAuth2 Device Flow on limited-input devices.",
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
    url="https://github.com/nomanark/google-device-auth-python",
    packages=find_packages(),
    install_requires=[
        "requests>=2.25.1",
    ],
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
)
