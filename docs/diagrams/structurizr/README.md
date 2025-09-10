## Introduction

Just a README file ...

## Repository Structure

- `/structurizr/current`: Contains DSL for current (as-is) Lung Cancer Health Check state
- `/structurizr/pilot`: Contains DSL for Pilot (interim to-be) Lung Cancer Health Check state

## Getting Started

### 1. Lung Health Check Models (Structurizr)

To work with the models, you'll need to run Structurizr Lite locally. This requires Docker installation.

#### Prerequisites

- Docker installed from [https://www.docker.com/get-started/](https://www.docker.com/get-started/)

#### Running Structurizr

First, pull the latest Structurizr lite image:

```bash
docker pull structurizr/lite
```

Then run the container (commands vary by operating system):

##### MacOS and Linux

```bash
cd structurizr/pilot
docker run -it --rm -p 8080:8080 -v ./:/usr/local/structurizr structurizr/lite
```

Note: For MacOS Sequoia 15.2 and later, use this command instead to avoid sigterm exceptions:

```bash
cd pilot
docker run --rm -e JAVA_TOOL_OPTIONS="-XX:UseSVE=0" -p 8080:8080 -v ./:/usr/local/structurizr structurizr/lite
```

##### Windows

```bash
cd pilot
docker run -it --rm -p 8080:8080 -v %cd%:/usr/local/structurizr structurizr/lite
```

Once running, access the live view at http://localhost:8080
