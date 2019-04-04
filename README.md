# Corsair
Python wrapper for some NSOC tools.  Corsair aims to implement [RESTFul](https://en.wikipedia.org/wiki/Representational_state_transfer) wrappers for different tools commonly used by Network and Security Operations Centers (NSOC).

The main idea behind Corsair is to provide a method to access different APIs to facilitate the task of integrating tools.  So far, each tool has at least three kinds of classes:

* `Api`: the higher level of abstraction, which connects to the API.
* `Endpoint`: uses endpoints to connect to certain API resources, by using [CRUD](https://en.wikipedia.org/wiki/Create,_read,_update_and_delete) methods.
* `Request`: execute actions in a given API endpoint or resource, using [HTTP methods](https://developer.mozilla.org/en-US/docs/Web/HTTP/Methods).

It's a project decision to return almost "raw" data from API, so the consumer must treat this data.  This is done because at this point of the project, it'll take a lot of time to understand all resources provided by each API and organize the way they will output data.


## Tests
Run tests with:

```
$ python -m unittest tests.test_prime_api
$ python -m unittest tests.test_netbox_api
$ python -m unittest tests.test_qradar_api
```
