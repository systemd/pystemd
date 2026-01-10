# pystemd E2E Testing Setup

## Overview

This setup provides comprehensive end-to-end testing for pystemd using mkosi and systemd-nspawn. Tests run in a real systemd environment inside a container to ensure accurate testing of systemd integration.

## Quick Start

```bash
# Install dependencies (one-time setup)
sudo dnf install mkosi systemd-container  # Fedora/RHEL
# or
sudo apt install mkosi systemd-container  # Debian/Ubuntu

# generate keys if they dont exists
mkosi genkey 

# build container, there steps do not need to be run as root.
mkosi clean &&  mkosi build

# Start container
UNIT_NAME=pystemd-e2e-local.service
MACHINE_NAME=pystemd-test-local
sudo systemd-run --unit "$UNIT_NAME" --same-dir \
    systemd-nspawn \
      --machine="$MACHINE_NAME" \
      --boot \
      --directory=pystemd-test \
      --bind-ro=`pwd`/e2e:/opt/pystemd/e2e

# Run all E2E tests
sudo systemd-run \
    --machine="$MACHINE_NAME" \
    --wait \
    --pipe \
    --setenv=PYSTEMD_E2E_CONTAINER=1\
    --property=PrivateTmp=true \
    -- \
    /opt/pystemd/venv/bin/pytest \
      -o cache_dir=/tmp/pytest_cache \
      /opt/pystemd/e2e/ -v
```


## How It Works

### Manual Container Management

The E2E testing workflow uses a straightforward approach:

1. **Build the container image** using mkosi - this creates a Fedora environment with pystemd installed
2. **Boot the container** using systemd-nspawn as a background service
3. **Run tests inside the container** using `systemd-run --machine`
4. **Stop the container** when done

The container runs with `--boot` which starts a full systemd init inside, providing a realistic systemd environment for testing.

### Container Boot Command

The container is booted as a systemd service using systemd-nspawn:

```bash
UNIT_NAME=pystemd-e2e-local.service
MACHINE_NAME=pystemd-test

sudo systemd-run --unit "$UNIT_NAME" --same-dir \
    systemd-nspawn \
      --machine="$MACHINE_NAME" \
      --boot \
      --directory=pystemd-test \
      --bind-ro=`pwd`/e2e:/opt/pystemd/e2e
```

Tests are then executed inside the container using:

```bash
sudo systemd-run \
    --machine="$MACHINE_NAME" \
    --wait \
    --pipe \
    --setenv=PYSTEMD_E2E_CONTAINER=1 \
    --property=PrivateTmp=true \
    -- \
    /opt/pystemd/venv/bin/pytest \
      -o cache_dir=/tmp/pytest_cache \
      /opt/pystemd/e2e/ -v
```


## Test Suite

Tests are located in the `e2e/` directory:

- **`test_pystemd_run.py`** - Tests for `pystemd.run()`
- **`test_manager.py`** - Tests for systemd Manager API
- **`test_unit.py`** - Tests for Unit operations
- **`test_transient_units.py`** - Tests for transient unit creation
- **`test_dbus.py`** - Tests for D-Bus connections

## Adding New Tests

Create a new test file in the `e2e/` directory:

```python
# e2e/test_my_feature.py
import pystemd.run

def test_my_feature():
    """Test my new feature"""
    unit = pystemd.run([b'/bin/echo', b'hello'], wait=True)
    assert unit.Service.ExecMainStatus == 0
```

```bash
sudo systemd-run \
    --machine="$MACHINE_NAME" \
    --wait \
    --pipe \
    --setenv=PYSTEMD_E2E_CONTAINER=1 \
    --property=PrivateTmp=true \
    -- \
    /opt/pystemd/venv/bin/pytest \
      -o cache_dir=/tmp/pytest_cache \
      /opt/pystemd/e2e/test_my_feature.py -v
```


And run it using 

## CI/CD Integration

The GitHub Actions workflow (`.github/workflows/e2e-tests.yml`) automates E2E testing:

**Triggers:**
- Pushes to `main` or `develop` branches
- Pull requests targeting `main`

**Matrix Testing:**
- Tests across multiple Python versions: 3.11, 3.12, 3.13, 3.14, 3.14t (free-threaded)
- Each Python version runs in its own container instance


## Troubleshooting

### Container fails to start
```bash
# Check if another container is running
sudo machinectl list

# SSH into the container
sudo machinectl shell pystemd-test

# Terminate stale container
sudo machinectl terminate pystemd-test
```

### Image not found
```bash
# Rebuild the mkosi image
sudo mkosi --force build
```

### Tests hang
```bash
# Check container status
sudo machinectl status pystemd-test

# View container logs
sudo journalctl -M pystemd-test
```

### Building with a different Python version

By default, the container is built with Python 3.14. To build with a different Python version, set the `PYTHON_VERSION` environment variable before building:

```bash
# Build with Python 3.12
mkosi clean && mkosi -E PYTHON_VERSION=3.12 build 

# Build with Python 3.14 free-threaded
mkosi clean && mkosi-E PYTHON_VERSION=3.14t build
```

The `-E` flag passes the `PYTHON_VERSION` environment variable to mkosi, which is then used by `mkosi.build.chroot` to install the specified Python version using `uv python install`.

