#!/bin/bash

# Test script for version history tracking
# This script tests the upgrade and downgrade functionality and verifies that
# version history is properly tracked in the JSON database.

# Set the base URL
BASE_URL="http://localhost:8000"

# Colors for output
GREEN='\033[0;32m'
RED='\033[0;31m'
YELLOW='\033[0;33m'
NC='\033[0m' # No Color

# Function to print colored output
print_status() {
  if [ "$1" = "PASS" ]; then
    echo -e "${GREEN}[PASS]${NC} $2"
  elif [ "$1" = "FAIL" ]; then
    echo -e "${RED}[FAIL]${NC} $2"
  else
    echo -e "${YELLOW}[$1]${NC} $2"
  fi
}

# Function to check if jq is installed
check_jq() {
  if ! command -v jq &> /dev/null; then
    print_status "FAIL" "jq is not installed. Please install jq to run this test."
    exit 1
  fi
}

# Function to authenticate and get CSRF token
authenticate() {
  print_status "INFO" "Authenticating..."

  # Make login request
  response=$(curl -s -X POST "$BASE_URL/api/types/loginSessionInfo/instances" \
    -H "X-EMC-REST-CLIENT: true" \
    -H "Content-Type: application/json" \
    -u "admin:Password123!" \
    -c cookie.txt)

  # Extract CSRF token from response headers
  csrf_token=$(grep -i "EMC-CSRF-TOKEN" headers.txt | cut -d' ' -f2 | tr -d '\r')

  if [ -z "$csrf_token" ]; then
    print_status "FAIL" "Failed to get CSRF token"
    exit 1
  else
    print_status "PASS" "Authentication successful, got CSRF token: $csrf_token"
  fi
}

# Function to get current system version
get_system_version() {
  print_status "INFO" "Getting current system version..."

  response=$(curl -s -X GET "$BASE_URL/api/types/basicSystemInfo/instances" \
    -H "X-EMC-REST-CLIENT: true" \
    -b cookie.txt)

  # Extract version from response
  version=$(echo "$response" | jq -r '.entries[0].content.softwareVersion')

  if [ -z "$version" ] || [ "$version" = "null" ]; then
    print_status "FAIL" "Failed to get system version"
    exit 1
  else
    print_status "PASS" "Current system version: $version"
    echo "$version"
  fi
}

# Function to get version history
get_version_history() {
  print_status "INFO" "Getting version history..."

  response=$(curl -s -X GET "$BASE_URL/api/types/versionHistory/instances" \
    -H "X-EMC-REST-CLIENT: true" \
    -b cookie.txt)

  # Print version history
  echo "$response" | jq '.entries[].content'

  # Count entries
  count=$(echo "$response" | jq '.entries | length')
  print_status "INFO" "Version history has $count entries"

  echo "$count"
}

# Function to perform an upgrade
perform_upgrade() {
  print_status "INFO" "Preparing software for upgrade..."

  # Prepare software
  response=$(curl -s -X POST "$BASE_URL/api/types/candidateSoftwareVersion/action/prepare" \
    -H "X-EMC-REST-CLIENT: true" \
    -H "EMC-CSRF-TOKEN: $csrf_token" \
    -H "Content-Type: application/json" \
    -b cookie.txt)

  candidate_id=$(echo "$response" | jq -r '.id')

  if [ -z "$candidate_id" ] || [ "$candidate_id" = "null" ]; then
    print_status "FAIL" "Failed to prepare software"
    exit 1
  else
    print_status "PASS" "Software prepared, candidate ID: $candidate_id"
  fi

  print_status "INFO" "Creating upgrade session..."

  # Create upgrade session
  response=$(curl -s -X POST "$BASE_URL/api/types/upgradeSession/instances" \
    -H "X-EMC-REST-CLIENT: true" \
    -H "EMC-CSRF-TOKEN: $csrf_token" \
    -H "Content-Type: application/json" \
    -d "{\"candidate\": \"$candidate_id\"}" \
    -b cookie.txt)

  session_id=$(echo "$response" | jq -r '.id')

  if [ -z "$session_id" ] || [ "$session_id" = "null" ]; then
    print_status "FAIL" "Failed to create upgrade session"
    exit 1
  else
    print_status "PASS" "Upgrade session created, ID: $session_id"
  fi

  # Wait for upgrade to complete
  print_status "INFO" "Waiting for upgrade to complete..."
  status="IN_PROGRESS"

  while [ "$status" = "IN_PROGRESS" ]; do
    sleep 2
    response=$(curl -s -X GET "$BASE_URL/api/instances/upgradeSession/$session_id" \
      -H "X-EMC-REST-CLIENT: true" \
      -b cookie.txt)

    status=$(echo "$response" | jq -r '.content.status')
    percent=$(echo "$response" | jq -r '.content.percentComplete')

    print_status "INFO" "Upgrade progress: $percent% (status: $status)"

    if [ "$status" = "COMPLETED" ]; then
      print_status "PASS" "Upgrade completed successfully"
      break
    elif [ "$status" = "FAILED" ] || [ "$status" = "CANCELLED" ]; then
      print_status "FAIL" "Upgrade failed with status: $status"
      exit 1
    fi
  done
}

# Function to perform a downgrade
perform_downgrade() {
  print_status "INFO" "Performing downgrade..."

  # Create upgrade session for downgrade
  response=$(curl -s -X POST "$BASE_URL/api/types/upgradeSession/instances" \
    -H "X-EMC-REST-CLIENT: true" \
    -H "EMC-CSRF-TOKEN: $csrf_token" \
    -H "Content-Type: application/json" \
    -b cookie.txt)

  session_id=$(echo "$response" | jq -r '.id')

  if [ -z "$session_id" ] || [ "$session_id" = "null" ]; then
    print_status "FAIL" "Failed to create upgrade session for downgrade"
    exit 1
  else
    print_status "PASS" "Downgrade completed using upgrade session, ID: $session_id"
  fi
}

# Main test function
run_test() {
  check_jq

  print_status "INFO" "Starting version history test..."

  # Create output files
  curl -s -D headers.txt > /dev/null

  # Authenticate
  authenticate

  # Get initial version
  initial_version=$(get_system_version)

  # Get initial history count
  initial_history_count=$(get_version_history)

  # Perform upgrade
  perform_upgrade

  # Get version after upgrade
  upgraded_version=$(get_system_version)

  # Check if version changed
  if [ "$initial_version" = "$upgraded_version" ]; then
    print_status "FAIL" "Version did not change after upgrade"
  else
    print_status "PASS" "Version changed from $initial_version to $upgraded_version"
  fi

  # Get history after upgrade
  upgrade_history_count=$(get_version_history)

  # Check if history was updated
  if [ "$initial_history_count" = "$upgrade_history_count" ]; then
    print_status "FAIL" "Version history was not updated after upgrade"
  else
    print_status "PASS" "Version history was updated after upgrade"
  fi

  # Perform downgrade
  perform_downgrade

  # Get version after downgrade
  downgraded_version=$(get_system_version)

  # Check if version changed
  if [ "$upgraded_version" = "$downgraded_version" ]; then
    print_status "FAIL" "Version did not change after downgrade"
  else
    print_status "PASS" "Version changed from $upgraded_version to $downgraded_version"
  fi

  # Get history after downgrade
  final_history_count=$(get_version_history)

  # Check if history was updated
  if [ "$upgrade_history_count" = "$final_history_count" ]; then
    print_status "FAIL" "Version history was not updated after downgrade"
  else
    print_status "PASS" "Version history was updated after downgrade"
  fi

  # Clean up
  rm -f cookie.txt headers.txt

  print_status "INFO" "Version history test completed"
}

# Run the test
run_test
