from distutils.core import setup
setup(
  name = 'django_amqp_consumer',
  packages = ['django_amqp_consumer'], # this must be the same as the name above
  version = '0.1',
  description = 'A django command to consume amqp queues',
  author = 'Rafael Gonçalves',
  author_email = 'rafagonc77@yahoo.com.br',
  url = 'https://github.com/rafagonc/django_amqp_consumer', # use the URL to the github repo
  download_url = 'https://github.com/rafagonc/django_amqp_consumer/archive/0.1.tar.gz', # I'll explain this in a second
  keywords = ['amqp', 'queues', 'consumer'], # arbitrary keywords
  classifiers = [],
)