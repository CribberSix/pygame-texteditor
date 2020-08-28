from setuptools import setup
from os import path

this_directory = path.abspath(path.dirname(__file__))
with open(path.join(this_directory, 'README.md'), encoding='utf-8') as f:
    long_description = f.read()

setup(
    name='pygametexteditor',
    packages=['pygametexteditor'],
    license='MIT',
    description='A simple WYSIWYG-texteditor based on pygame.',
    long_description=long_description,
    long_description_content_type='text/markdown',
    version='0.0.46',
    python_requires=">=3.6",
    author='CribberSix',
    author_email='cribbersix@gmail.com',
    install_requires=['pygame', 'math', 'os', 'sys'],
    classifiers=[
        # Trove classifiers
        # (https://pypi.python.org/pypi?%3Aaction=list_classifiers)
        'Development Status :: 3 - Alpha',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python',
        'Programming Language :: Python :: 3.6',
        'Topic :: Software Development :: Libraries',
        'Topic :: Software Development :: Libraries :: Python Modules',
        'Intended Audience :: Developers',
        'Natural Language :: English',
        'Topic :: Software Development',
    ],
    keywords=['pygame', 'texteditor', 'text', 'editor'],
    package_data={'pygametexteditor': ['pygametexteditor/elements/*.png', 'pygametexteditor/elements/*.ttf']},
    include_package_data=True,
)

