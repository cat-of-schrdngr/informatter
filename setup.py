from distutils.core import setup

# Specifying Dependencies
# https://python-packaging.readthedocs.io/en/latest/dependencies.html

setup(
    name='informatter',
    version='0.1',
    description='Tool for extraction, tokenization, & ordering of scientific '
                'manuscripts using S2ORC manuscripts database and mat2vec '
                'tokenization and processing tool.',
    url='http://...',
    author='Mina',
    author_email='me@mine_address.com',
    license='...',
    packages=['corpus'],
    install_requires=['mat2vec'],
    dependency_links=['https://github.com/materialsintelligence/mat2vec.git']
)
