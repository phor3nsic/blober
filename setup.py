from setuptools import setup, find_packages

setup(
    name='blober',
    version='0.1',
    packages=find_packages(),
    install_requires=[
        "azure-storage-blob",
        "boto3"
    ],  # requirements.txt
    entry_points={
        'console_scripts': [
            'blober=blober.main:main',
        ],
    },
    author='phor3nsic',
    author_email='phorensic@pm.me',
    description='Description of blober.',
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',
    url='https://github.com/phor3nsic/blober',
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: 3.9',
    ],
)
