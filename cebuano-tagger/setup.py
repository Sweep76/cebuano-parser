from setuptools import setup

setup(
  name = 'cebpostagger',
  packages = ['cebpostagger'],
  version = '1.1',
  description = "Rule-Based Cebuano POS Tagger Using Constraint-Based Grammar and Affixing Rules",
  author = 'Arjemariel Requina',
  author_email = 'rjrequina@gmail.com',
  url = 'https://github.com/ajrequina/Cebuano-POS-Tagger',
  download_url = 'https://github.com/ajrequina/Cebuano-POS-Tagger/archive/1.0.tar.gz',
  keywords = ['pos-tagger', 'cebuano-pos-tagger'],
  classifiers = [],
  include_package_data=True,
  install_requires=[
    'cebstemmer @ git+https://github.com/NoodleSushi/Cebuano-Stemmer.git',
    'nltk'
  ],
)