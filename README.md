# Lung Cancer Screening

This service is a digital version Lung Cancer Screening questionnaire and risk calculator.

## Table of Contents

- [Lung Cancer Screening](#lung-cancer-screening)
  - [Table of Contents](#table-of-contents)
  - [Prerequisites](#prerequisites)
  - [Setup](#setup)
  - [Running the app locally](#running-the-app-locally)
  - [Testing](#testing)
  - [Contributing](#contributing)
  - [Licence](#licence)

## Prerequisites

The following software packages, or their equivalents, are expected to be installed and configured:

- [Docker](https://www.docker.com/) container runtime or a compatible tool, e.g. [Podman](https://podman.io/),
- [GNU make](https://www.gnu.org/software/make/) 3.82 or later
- [asdf](https://asdf-vm.com/) version manager for managing tool versions (ensure asdf is configured in your shell)

## Setup

1. Copy the environment file:

   ```shell
   cp .env.example .env
   ```

1. Setup the pre-commit hooks and install dependencies:

   ```shell
   make config
   ```

   Note: If you encounter Python installation issues on macOS, you may need to install Python with SSL flags:

   ```shell
   CFLAGS="-I$(brew --prefix openssl@3)/include" \
   LDFLAGS="-L$(brew --prefix openssl@3)/lib" \
   PKG_CONFIG_PATH="$(brew --prefix openssl@3)/lib/pkgconfig" \
   asdf install python 3.13.7
   ```

## Running the app locally

The project runs locally inside docker. Please ensure you have docker installed.

You can run the application by running:

```shell
make dev-run
```

After starting the application, apply the database migrations:

```shell
make dev-migrate
```

## Testing

There are `make` tasks for you to configure to run your tests.  Run `make test` to see how they work.  You should be able to use the same entry points for local development as in your CI pipeline.

## Contributing

- Make sure you have pre-commit running so that pre-commit hooks run automatically when you commit - this should have been set up automatically when you ran `make config`.
- Consider switching on format-on-save in your editor (e.g. [Black](https://github.com/psf/black) for Python)

## Licence

Unless stated otherwise, the codebase is released under the MIT License. This covers both the codebase and any sample code in the documentation. See [LICENCE.md](./LICENCE.md).

Any HTML or Markdown documentation is [© Crown Copyright](https://www.nationalarchives.gov.uk/information-management/re-using-public-sector-information/uk-government-licensing-framework/crown-copyright/) and available under the terms of the [Open Government Licence v3.0](https://www.nationalarchives.gov.uk/doc/open-government-licence/version/3/).
