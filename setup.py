from setuptools import setup

setup(
    name='pygametexteditor',
    packages=['pygametexteditor'],
    license='MIT',
    description='A simple WYSIWYG-texteditor based on pygame.',
    version='0.0.41',
    python_requires=">=3.5",
    url='https://github.com/CribberSix/pygame-texteditor',
    author='CribberSix',
    author_email='cribbersix@gmail.com',
    install_requires=['pygame'],
    classifiers=[
        # Trove classifiers
        # (https://pypi.python.org/pypi?%3Aaction=list_classifiers)
        'Development Status :: 4 - Beta',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python',
        'Programming Language :: Python :: 3.6',
        'Topic :: Software Development :: Libraries',
        'Topic :: Software Development :: Libraries :: Python Modules',
        'Intended Audience :: Developers',
    ],
    keywords=['pygame','texteditor'],
    package_data={'pygametexteditor': ['pygametexteditor/elements/*.png', 'pygametexteditor/elements/*.ttf']},
    include_package_data=True,
)

