from setuptools import setup, find_packages
import pathlib

# The directory containing this file
HERE = pathlib.Path(__file__).parent

# The text of the README file
README = (HERE / "README.md").read_text()

setup(
    name='pygame-texteditor',
    packages=['pygame_texteditor'],
    package_data={'pygame_texteditor': ['pygame_texteditor/elements/graphics/*.png', 'pygame_texteditor/elements/fonts/.ttf', 'pygame_texteditor/elements/colorstyles/*.yml']},
    include_package_data=True,
    license='MIT',
    description='A WYSIWYG-texteditor based on pygame.',
    long_description=README,
    long_description_content_type='text/markdown',
    version='0.6',
    python_requires=">=3.6",
    author='CribberSix',
    author_email='cribbersix@gmail.com',
    install_requires=['pygame==1.9.6', 'pyyaml >= 5.3.1', 'pygments >= 2.6.1', 'pyperclip >= 1.8.1'],
    classifiers=[
        'Development Status :: 4 - Beta',
        # 'Development Status :: 5 - Production/Stable',
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
)

