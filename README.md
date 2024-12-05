# Stargazer

An API that provides information related to the Stargazers feature of GitHub.

# How to run
1. Duplicate and rename the env.template  to .env. Replace accordingly the EVs.
2. Run the application using the [Uvicorn CLI](https://www.uvicorn.org/deployment/) : 

```bash 
uvicorn main:app --reload 
```



# Development approach

We approached the development on this repository as if the end goal was to have a big application with numerous
endpoints.
As such, we prioritized implementations of solutions that are more scalable even if this is more time-consuming.

For example the use of constants, the error management or the authentication middleware are things that currently add
complexity and may make the code appear more convoluted, since we currently have only one endpoint.

# Libraries choices

## Web framework - FastAPI

Other web framework I considered :

- **Django** : We didn't need many features provided by a full-stack framework, so it didn't seem the more adapted choice
- **Flask** : Since performance seemed an important aspect from the start, I wanted to be able to easily implement
  asynchronous mechanisms

Overall I can't say I'm familiar enough with these frameworks to pretend I made the best choice, but FastAPI seemed adapted for our case (an API with a focus on performance).

## Interacting with GitHub API - PyGithub

I made the choice to use PyGithub over requesting directly the GitHub API.
The main benefits are having type hints available for GitHub objects and managing the pagination automatically.
However, it also came with limitations that I only realized later on.
For example, you can’t get the stargazers of a repo in a single request using it (you need to first to request for the
repo, then request for the stargazers).
GitHub API, on the other hand, provides an endpoint to get stargazers with a single request (
/repos/{owner}/{repo}/stargazers).
Another important limitations is that it doesn't natively support asynchronous
operations ([This is currently a top issue](https://github.com/PyGithub/PyGithub/issues/1538)).

For future developments I think mixing PyGithub with direct API call is the smartest approach.
Having PyGithub would allow us to have type hints for GitHub API and simplify operations that don't need to be
optimized.
And, when performance is an issue, we could make direct API calls to reduce the number of requests or allow asynchronous
operations.

## Authentication - PyJWT

I've considered **OAuth 2.0** and **JWT** but ended up choosing the latest primarily because I had prior experience with it.
Additionally, we didn’t need third-party authentication, which is one key advantage of OAuth.

Currently, there's features that aren't used, for example I didn't implement an endpoint to refresh the tokens.

## Testing - Unittest

Unittest was the easiest to use since it's already built in Python and provides everything we need, like mocking.

# Current issues and area of improvements

## Performance issues

Currently, even if the endpoint is working as intended, the performances are terrible for users with a lot of starred
repositories.
I also didn't test extensively, so it's possible I overlook other issues.

## Lack of knowledge about the GitHub API

While I spent time reviewing the PyGithub and GitHub API documentation, I didn’t gain expert-level knowledge overnight.
As such, it's possible that I overlooked features or endpoints that could have been more adapted in my case.
I also didn't explore other libraries ([like github3.py](https://github.com/sigmavirus24/github3.py)).

## Current limitations and weak points

- **Performance** : This was already mentioned above.
- **Testing** : Testing mostly focuses on code coverage and doesn’t include many use cases. That part could definitely be
  improved. Also, there's no integration testing.
- **Error handling** : Some errors aren’t caught, and error responses need to be formalized.
- **Logic** : We didn't do anything regarding how close projects are.

## Potentials improvements

- **CI/CD** : Nothing has been done to integrate our API with CI/CD tools. I'd like to at least use GHA here, it could run
  operations on commit/push (apply style rules and run tests), send notifications, deploy, etc.
- **Formatting** : I only used the native formatter in PyCharm. Having a common formatter is very important for
  collaborative projects (so changes made aren't obstructed by formatting).
- **Documentation** : More documentation could be added, for example how the authentication mechanism works, or a description of the endpoints available.

### Scalability

Scalability and performance is currently the biggest aspect that would need improvement, here's a few potential
mechanisms that could help (in order of pertinence) :

- Caching the results of some requests (for example the starred repos of a user).
- Mixing use of PyGithub and direct call to GiHub API.
- Making asynchronous requests (using **asyncio**) when relevant (for example when looping to get the starred repos of users).
- Switching to **GraphQL** to fetch only the required data could improve performance since GitHub API return lot of unnecessary data.
- Make use of parallel processing.
