#!/bin/bash

# This script manages the lifecycle of a Docker container and BigQuery dataset manipulation

# Exit immediately if a command exits with a non-zero status.
set -e

# Step 4: Build and run the Docker container
echo "Building Docker image..."
docker build -t BigEye .
echo "Docker image built successfully."

echo "Running Docker container..."
docker run -it --rm gdelt
echo "Docker container ran and removed successfully."

# Step 5: Verify the data is loaded into BigQuery
echo "Verifying data in BigQuery..."
if bq show gdelt-bq:gdeltv2.usa_events; then
    echo "Dataset verified successfully."
else
    echo "Failed to verify dataset. Dataset does not exist or other error occurred."
fi

# Step 6: Clean up
echo "Cleaning up resources..."
# Remove the BigQuery dataset
bq rm -f gdelt-bq:gdeltv2.usa_events
echo "BigQuery dataset removed successfully."

# Remove the Docker image
docker rmi gdelt
echo "Docker image removed successfully."

echo "Script completed successfully."
