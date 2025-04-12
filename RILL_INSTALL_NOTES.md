# Rill Installation Notes

## Official Installation

Rill is not available as a Python package via pip. Instead, it should be installed using the official installation methods from the Rill website:

- Visit [Rill Data official website](https://www.rilldata.com/) to download the appropriate installation package
- Follow the installation instructions for your specific operating system

## Alternative Installation Methods

### Using Docker

You can run Rill using Docker:

```bash
docker pull rilldata/rill
docker run -p 9876:9876 -v $(pwd)/rill-dashboards:/project rilldata/rill
```

### Using Homebrew (macOS)

```bash
brew install rilldata/tap/rill
```

## Verifying Installation

After installation, you can verify that Rill is working by running:

```bash
rill --version
```

## Starting Rill with Our Project

Once Rill is installed, you can start it with:

```bash
cd rill-dashboards
rill start
```

## Testing without Rill Installation

Our project includes tests that validate the Rill configuration files without requiring an actual Rill installation. You can run these tests with:

```bash
python -m unittest test_rill_integration.py -v
```

These tests verify:
1. The project structure
2. MongoDB source configuration
3. SQL model definition
4. Dashboard configuration

This allows development and testing of the Rill integration without requiring the Rill application to be installed. 