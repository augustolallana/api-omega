# Omega REST API

This is a Fastapi project that connects with Google AppSheets.

## Steps to deploy
1. Clone the repository
2. Download [uv](https://docs.astral.sh/uv/) if necessary.
3. Run `uv sync` to download the dependencies.
4. Run `make prod` to deploy the server. The terminal will show the host and port.


## Before commiting to main

Make sure to test in development mode. To do so run `make dev`. 
Once the changes are sufficient format your files with `make format`. 

In the near future pull requests will be a must before merging to main. 