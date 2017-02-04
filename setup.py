from distutils.core import setup

setup(
    name = 'pymicro',
    packages = ['pymicro', 'pymicro.protocols'],
    include_package_data=True,
    version = '0.0.2',
    description = 'An easy to use python3 package to create and use microservices.',
    author = 'Daniele Maccioni',
    author_email = 'komradstudios@gmail.com',
    url = 'https://github.com/GendoIkari/pymicro',
    download_url = 'https://github.com/GendoIkari/pymicro/tarball/v0.0.2',
    keywords = ['microservices', 'rabbitmq', 'service'],
    classifiers = [],
    install_requires=['flask', 'requests', 'pika'],
)
