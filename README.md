# pymicro
An easy to use python3 package to create and use microservices.

## Installation

```
pip install pymicro
```

## Example

[HTTP and RabbitMQ protocols ping-pong example](examples)

## Dev Commands
Once .pypirc is properly setup type in order to deploy a new version:

- Create a new tag on github
- Update setup.py
- Upload the new version:
```
python setup.py sdist upload -r pypi
```
