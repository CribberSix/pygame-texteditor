from setuptools import setup
import pathlib

# The directory containing this file
HERE = pathlib.Path(__file__).parent

# The text of the README file
README = (HERE / "README.md").read_text()

setup(
    name='pygametexteditor',
    packages=['pygametexteditor'],
    license='MIT',
    description='A WYSIWYG-texteditor based on pygame.',
    long_description=README,
    long_description_content_type='text/markdown',
    version='0.0.52.6',
    python_requires=">=3.6",
    author='CribberSix',
    author_email='cribbersix@gmail.com',
    install_requires=['pygame==1.9.6'],
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

