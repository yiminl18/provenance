from setuptools import setup, find_packages

with open('README.md', 'r', encoding='utf-8') as fh:
    long_description = fh.read()

setup(
    name='provenance',
    version='0.1.0',
    description='A pipeline for document processing and analysis',
    long_description=long_description,
    long_description_content_type='text/markdown',
    author='Junrui Zhu',
    author_email='juneray2003@gmail.com',
    url='https://github.com/yiminl18/provenance',
    packages=find_packages(),
    install_requires=[
    ],
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
    ],
    python_requires='>=3.9',
)
