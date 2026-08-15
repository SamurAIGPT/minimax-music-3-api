from setuptools import setup

setup(
    name="minimax-music-3-api",
    version="0.1.0",
    author="Anil Matcha",
    description="Python wrapper for MuAPI's MiniMax Music 3.0 text-to-music API.",
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
    py_modules=["minimax_music_3_api"],
    install_requires=[
        "requests",
        "python-dotenv",
    ],
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.7',
)
