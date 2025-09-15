docker build --build-arg INSTALL_DEV=true -t pokemon-app-dev backend && docker run --rm pokemon-app-dev pytest -v
