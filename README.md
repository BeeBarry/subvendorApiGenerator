# Requirements
## Github rest API perms
- "Contents" repository permissions (read)

# Development
1. create logic app with github rest token in Authorization headers of http methods
1. deploy function app with basic, secrets based authentication and python 3.11
1. copy function URL, paste in logic app in the Uri field of the "sendToApiGenerator" step
1. merge a PR in IAC -> logic app triggers -> function app triggers 

# TODO:
- [ ] IAC
    - [ ] use app settings and IAC outputs for repo urls and connection strings and whatnot
    - [ ] API management
        - [ ] Proper API versioning
        - [ ] API endpoint authorization
- [ ] handle sensitive variables
- [ ] retry logic
-   [ ] load balancing
-   [ ] docs
-   [ ] pin API versions

