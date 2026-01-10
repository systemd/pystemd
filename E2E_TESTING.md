# pystemd E2E Testing Setup

## Overview

This setup provides comprehensive end-to-end testing for pystemd using mkosi. Tests run in a real systemd environment to ensure accurate testing of systemd integration.

## Quick Start

```bash
# Install mkosi (one-time setup)
sudo dnf install mkosi  # Fedora/RHEL
# or
sudo apt install mkosi  # Debian/Ubuntu

# Run all E2E tests
make e2e-test

# Or manually
sudo mkosi
```

## What Was Created

### Configuration Files

1. **`mkosi.conf`** - Main mkosi configuration
   - Defines Fedora 41 test environment
   - Installs Python 3, systemd, and dependencies
   - Configures build and test setup

2. **`mkosi.build`** - Build script
   - Builds pystemd from source
   - Installs into test image
   - Installs test dependencies (pytest, psutil)

3. **`mkosi.postinst`** - Post-installation script
   - Sets up test environment
   - Configures systemd

### Test Suite

**`mkosi.files/e2e-tests/test_e2e.py`** - Comprehensive E2E tests covering:

#### pystemd.run Tests (10+ tests)
- Simple command execution
- Commands with args, env vars, custom cwd
- User switching (requires root)
- Wait modes (wait vs wait_for_activation)
- Error handling (raise_on_fail)
- Timeouts (runtime_max_sec)
- Service types
- Stop commands

#### Manager Tests
- Version and architecture queries
- Listing units and unit files
- Getting units by name

#### Unit Tests
- Property reading
- Start/stop/restart operations
- Process management

#### Transient Unit Tests
- Creating via Manager API
- Setting dependencies

#### D-Bus Tests
- System bus connections
- User bus connections

### Infrastructure

4. **`mkosi.files/e2e-tests/run-tests.sh`** - Test runner
   - Executes pytest in mkosi environment
   - Reports results

5. **`Makefile`** - Convenience targets
   - `make e2e-test` - Build and run tests
   - `make e2e-shell` - Enter test environment
   - `make e2e-clean` - Clean artifacts

6. **`.github/workflows/e2e-tests.yml`** - CI integration
   - Runs on push/PR
   - Uses Ubuntu runners
   - Uploads test results

7. **`mkosi.files/e2e-tests/README.md`** - Detailed documentation

## Usage Examples

### Run tests locally
```bash
make e2e-test
```

### Debug a test failure
```bash
# Enter the test environment
make e2e-shell

# Inside the environment
cd /e2e-tests
python3 -m pytest test_e2e.py::TestPystemdRun::test_simple_command -v
```

### Run without rebuilding (faster iteration)
```bash
make e2e-test-quick
```

### Add a new test

Edit `mkosi.files/e2e-tests/test_e2e.py`:

```python
def test_my_feature(self):
    """Test my new feature"""
    unit = pystemd.run([b'/bin/echo', b'hello'], wait=True)
    assert unit.Service.ExecMainStatus == 0
```

Then run:
```bash
make e2e-test
```

## Architecture

```
┌─────────────────┐
│   Host System   │
│                 │
│  make e2e-test  │
└────────┬────────┘
         │
         v
┌─────────────────────────────────┐
│         mkosi                   │
│                                 │
│  ┌──────────────────────────┐  │
│  │   Fedora 41 Image        │  │
│  │                          │  │
│  │  - systemd running       │  │
│  │  - pystemd installed     │  │
│  │  - pytest + tests        │  │
│  │                          │  │
│  │  Run: /e2e-tests/        │  │
│  │       run-tests.sh       │  │
│  └──────────────────────────┘  │
│                                 │
│  Isolated systemd environment   │
└─────────────────────────────────┘
```

## Benefits

✓ **Real systemd environment** - Not containerized, no quirks
✓ **Isolated testing** - Clean environment each run
✓ **Fast** - Directory format, no VM overhead
✓ **CI ready** - GitHub Actions integration included
✓ **Example-based** - Tests derived from real usage examples

## CI/CD Integration

The GitHub Actions workflow (`.github/workflows/e2e-tests.yml`) automatically:
- Runs on every push to main/develop
- Runs on all pull requests
- Installs mkosi
- Builds test image
- Runs all E2E tests
- Uploads test artifacts

## Troubleshooting

### mkosi not found
```bash
sudo dnf install mkosi  # or apt install mkosi
```

### Permission denied
```bash
# mkosi requires root
sudo mkosi
```

### Tests fail locally but pass in examples
```bash
# Check if you're running as root (many tests require it)
sudo make e2e-test
```

### Want to modify the test environment
Edit `mkosi.conf` to add packages, change OS version, etc.

## Next Steps

- Add more test cases based on additional examples
- Test more edge cases
- Add performance benchmarks
- Test on different systemd versions
