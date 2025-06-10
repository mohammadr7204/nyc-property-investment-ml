#!/bin/bash

# Check if an address was provided
if [ -z "$1" ]; then
    echo "Usage: ./analyze_property.sh \"YOUR ADDRESS HERE\""
    echo "Example: ./analyze_property.sh \"123 West 86th Street, New York, NY\""
    exit 1
fi

# Run the analysis with the provided address
PYTHONPATH=$PYTHONPATH:. python scripts/run_analysis.py --address "$1"