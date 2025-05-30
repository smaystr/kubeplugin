# Kubernetes Resource Statistics Plugin

A kubectl plugin for displaying resource statistics in a user-friendly format.

## Project Status

**Last Updated:** 2024-03-19

### Recent Changes
- Implemented advanced plugin architecture with multi-language support
- Added Python-based resource analysis module
- Added Go-based export functionality
- Created comprehensive documentation for advanced plugin architecture
- Fixed and refactored the base plugin implementation

### Current Focus
- Advanced plugin architecture with modular design
- Multi-language support (Bash, Python, Go)
- Resource analysis and export capabilities

### Files Changed
- `scripts/kubectl-kubeplugin-advanced` - New wrapper plugin
- `scripts/kubeplugin-modules/analyze.py` - Python analysis module
- `scripts/kubeplugin-modules/export.go` - Go export module
- `scripts/ADVANCED_PLUGIN_ARCHITECTURE.md` - Architecture documentation

### Next Steps
1. Implement report generation module
2. Add automated testing
3. Create installation script
4. Add more export formats
5. Implement parallel execution support

## Advanced Plugin Architecture

### Overview
The advanced plugin (`kubectl-kubeplugin-advanced`) implements a modular architecture that allows for multi-language support and extensible functionality. This design enables the use of different programming languages for specific tasks while maintaining a unified interface.

### Key Components

#### 1. Wrapper Plugin (`kubectl-kubeplugin-advanced`)
- Written in Bash
- Acts as the main entry point
- Handles subcommand routing
- Manages module discovery and execution
- Provides consistent interface for all functionality

#### 2. Analysis Module (`analyze.py`)
- Written in Python
- Provides detailed resource usage analysis
- Features:
  - Resource usage pattern detection
  - Threshold-based warnings
  - Usage recommendations
  - Multiple output formats (JSON, table)
  - Configurable thresholds for CPU and memory

#### 3. Export Module (`export.go`)
- Written in Go
- Handles data export functionality
- Features:
  - Multiple export formats (CSV, JSON)
  - High-performance data processing
  - Resource type filtering
  - Namespace-specific exports

### Usage Examples

```bash
# Basic metrics (using original plugin)
kubectl kubeplugin pod -n kube-system

# Advanced analysis (Python module)
kubectl kubeplugin-advanced analyze pod -n kube-system --format json

# Export data (Go module)
kubectl kubeplugin-advanced export -type pod -n kube-system -format csv

# Generate reports (Python module)
kubectl kubeplugin-advanced report --period daily --namespace production
```

### Module Dependencies

#### Python Module Requirements
- Python 3.6+
- Required packages:
  - argparse
  - json
  - subprocess
  - typing

#### Go Module Requirements
- Go 1.16+
- Standard library packages:
  - encoding/csv
  - encoding/json
  - flag
  - os
  - os/exec

### Benefits of This Architecture

1. **Language-Specific Optimization**
   - Python for data analysis and reporting
   - Go for high-performance data processing
   - Bash for orchestration and system integration

2. **Modularity**
   - Each module can be developed independently
   - Easy to add new functionality
   - Simple to maintain and update

3. **Extensibility**
   - New modules can be added without modifying existing code
   - Support for additional languages
   - Flexible output formats

4. **Performance**
   - Optimized for each specific task
   - Parallel execution support
   - Efficient resource usage

### Installation

1. Clone the repository:
```bash
git clone https://github.com/yourusername/kubeplugin.git
cd kubeplugin
```

2. Make the plugins executable:
```bash
chmod +x scripts/kubectl-kubeplugin
chmod +x scripts/kubectl-kubeplugin-advanced
```

3. Compile the Go module:
```bash
cd scripts/kubeplugin-modules
go build -o export export.go
```

4. Install Python dependencies:
```bash
pip install -r requirements.txt
```

### Contributing

1. Fork the repository
2. Create a feature branch
3. Implement your changes
4. Add tests if applicable
5. Submit a pull request

### License

This project is licensed under the MIT License - see the LICENSE file for details. 