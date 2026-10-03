<div align="">

# 🚀 POSTRACI

### A multi-threaded TCP port scanner in Python

[![Python 3013](https://img.shields.io/badge/Python-3.13+-blue.svg)](https://www.python.org/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Platform](https://img.shields.io/badge/Platform-Linux%20%7C%20Windows%20%7C%20macOS-lightgrey.svg)]()

**Developer:** DeBALA

## Overview

POSTRACI is a command-line security tool that automates TCP port scanning across target hosts. Developed as a Proof of Concept (POC) to demonstrate network automation capabilities, it replaces manual port-checking processes with a fast, reliable, and scriptable solution.

The project showcases practical application of Python scripting, multi-threading, TCP/IP networking, and security research methodologies.

## Key Features

- **Automated Multi-threaded Scanning**: Concurrent port checks using Python's `threading` module, reducing scan time from minutes to seconds
- **Flexible Input Parsing**: Custom logic to handle port ranges (`1-1024`), comma-separated lists (`22,80,443`), and mixed formats (`22,80,100-200`)
- **Configurable Performance**: Adjustable worker threads and connection timeouts for different network conditions
- **Thread-Safe Execution**: Implements `Lock` and `Semaphore` to prevent race conditions and resource exhaustion
- **Performance Tracking**: Built-in execution timer for measuring and optimizing scan duration
- **Cross-Platform Compatibility**: Works on Linux/Unix, Windows, and virtual environments without modification
- **Zero Dependencies**: 100% Python standard library implementation for easy deployment

## Requirements

- Python 3.12 or higher
- No external packages required
- Compatible with:
  - Linux/Unix systems (Kali, Ubuntu, CentOS, etc.)
  - Windows 10/11
  - Virtual environments (VMware, VirtualBox, WSL)
  - Docker containers

## Installation

```bash

# Run the scanner
python POSTRACI.py -h
