# Corsair
Python wrapper for some NSOC tools.  Corsair aims to implement RESTful wrappers for different tools commonly used by Network and Security Operations Centers (NSOC).

The main idea behind Corsair is to provide a method to access different APIs to facilitate the task of integrating tools.  So far, each tool has 3 kinds of classes:

* `Api`: the higher level of abstraction, which connects to the API.
* `Endpoint`: connects to certain endpoint inside an API.
* `Request`: execute actions in a given API endpoint or resource.

It's a project decision to return almost "raw" data from API, so the consumer must treat this data.  This is done because at this point of the project, it'll take a lot of time to understand all resources provided by each API and organize the way they will output data.


## Tests
Run tests with:

```
$ python -m unittest tests.test_prime_api
$ python -m unittest tests.test_netbox_api
```
