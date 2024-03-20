from setuptools import setup

setup(
    name='PII Detector',
    version='0.1',
    install_requires=[
        'flask',
        'tf-keras',
        'tensorflow',
        'transformers',
        'pyyaml',
    ],
    entry_points={
        'console_scripts': [
            'pii-detector = backend.app'
        ]
    }
)
