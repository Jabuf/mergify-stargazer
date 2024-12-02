# API versioning
API_VERSION = "/v1"

# Resources
RESOURCE_REPOS = "/repos"
RESOURCE_STARNEIGHBOURS = "/starneighbours"

# Complete endpoints
ROUTE_STARNEIGHBOURS = f"{RESOURCE_REPOS}/{{user}}/{{repo}}{RESOURCE_STARNEIGHBOURS}"
