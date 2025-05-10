# Requirements
## Github rest API perms
- "Contents" repository permissions (read)

# Development
1. create logic app with github rest token in Authorization headers of http methods
1. deploy function app on flex consumption, linux, python 3.11 with vscode function app extension defaults
1. switch from storage v1 to v2 (non-essential but easier to work with)
1. assign storage blob contributor to managed identity of function app
1. copy function URL, paste in logic app in the Uri field of the "sendToApiGenerator" step
1. merge a PR in IAC -> logic app triggers -> function app triggers 

# TODO:
- [ ] IAC everything
    - [ ] use app settings and IAC outputs for repo urls and connection strings and whatnot
    - [ ] API management
        - [ ] Proper API versioning
        - [ ] API endpoint authorization
- [ ] secrets management
- [ ] retry logic
- [ ] load balancing/queueing
- [ ] docs
- [ ] deprecation

# Notes
some incompatibility with oryx (build system used in python function apps) and linux flex consumption means the default CICD provided by azure doesnt work
