#!/bin/bash
# Test script to demonstrate parametric testing of eligibility endpoint in different modes

# Set colors for output
GREEN='\033[0;32m'
RED='\033[0;31m'
YELLOW='\033[0;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Base URL for the API
BASE_URL="http://localhost:8000"

# Credentials
USERNAME="admin"
PASSWORD="Password123!"

# Output directory
OUTPUT_DIR="./tests/scripts/test_results"
mkdir -p "$OUTPUT_DIR"

# Log file
LOG_FILE="$OUTPUT_DIR/eligibility_test_$(date +%Y%m%d_%H%M%S).log"

# Function to log messages
log() {
    echo -e "${BLUE}[$(date +"%Y-%m-%d %H:%M:%S")]${NC} $1" | tee -a "$LOG_FILE"
}

# Function to execute curl commands and log them
execute_curl() {
    local description="$1"
    local command="$2"

    log "${YELLOW}=== $description ===${NC}"
    log "Executing: $command"

    # Execute the command and capture output
    local output
    output=$(eval "$command")

    # Check if output is valid JSON
    if echo "$output" | jq . >/dev/null 2>&1; then
        log "${GREEN}Received valid JSON response${NC}"
        echo "$output" | jq .
        echo "$output" | jq . >> "$LOG_FILE"
        return 0
    else
        log "${RED}Error: Invalid JSON response${NC}"
        echo "$output" >> "$LOG_FILE"
        return 1
    fi
}

# Function to get CSRF token
get_csrf_token() {
    log "${YELLOW}=== Getting CSRF Token ===${NC}"

    # Get CSRF token
    local csrf_response
    csrf_response=$(curl -s -k -L -X GET "$BASE_URL/api/types/loginSessionInfo/instances" \
        -u "$USERNAME:$PASSWORD" \
        -c cookie.jar \
        -H "X-EMC-REST-CLIENT: true")

    # Extract CSRF token from response
    local csrf_token
    csrf_token=$(echo "$csrf_response" | grep -o '"EMC-CSRF-TOKEN":"[^"]*"' | cut -d'"' -f4)

    if [ -z "$csrf_token" ]; then
        # Try to get it from cookie
        csrf_token=$(grep -o "EMC-CSRF-TOKEN\s*\w*" cookie.jar | awk '{print $2}')
    fi

    if [ -n "$csrf_token" ]; then
        log "${GREEN}Got CSRF token: $csrf_token${NC}"
        echo "$csrf_token"
        return 0
    else
        log "${RED}Failed to get CSRF token${NC}"
        return 1
    fi
}

# Main test function
run_tests() {
    log "${BLUE}Starting Eligibility Mode Tests${NC}"

    # Get CSRF token
    CSRF_TOKEN=$(get_csrf_token)
    if [ -z "$CSRF_TOKEN" ]; then
        log "${RED}Cannot proceed without CSRF token${NC}"
        exit 1
    fi

    # Set headers
    HEADERS="-H \"X-EMC-REST-CLIENT: true\" -H \"EMC-CSRF-TOKEN: $CSRF_TOKEN\""
    AUTH="-u \"$USERNAME:$PASSWORD\""

    # 1. Test default behavior (success mode)
    log "${YELLOW}=== Testing Default Behavior (Success Mode) ===${NC}"
    execute_curl "Getting current system configuration" "curl -s -k -L -X GET \"$BASE_URL/api/types/systemConfig/instances\" $AUTH $HEADERS"

    # Test eligibility endpoint in default mode
    execute_curl "Testing eligibility endpoint (default mode)" "curl -s -k -L -X POST \"$BASE_URL/api/types/upgradeSession/action/verifyUpgradeEligibility\" $AUTH $HEADERS"

    # 2. Switch to failure mode
    log "${YELLOW}=== Switching to Failure Mode ===${NC}"
    execute_curl "Setting system to failure mode" "curl -s -k -L -X POST \"$BASE_URL/api/types/systemConfig/action/update\" $AUTH $HEADERS -H \"Content-Type: application/json\" -d '{\"eligibility_status\": \"failure\"}'"

    # Test eligibility endpoint in failure mode
    execute_curl "Testing eligibility endpoint (failure mode)" "curl -s -k -L -X POST \"$BASE_URL/api/types/upgradeSession/action/verifyUpgradeEligibility\" $AUTH $HEADERS"

    # 3. Switch to auto mode with high failure probability
    log "${YELLOW}=== Switching to Auto Mode (80% Failure) ===${NC}"
    execute_curl "Setting system to auto mode with high failure probability" "curl -s -k -L -X POST \"$BASE_URL/api/types/systemConfig/action/update\" $AUTH $HEADERS -H \"Content-Type: application/json\" -d '{\"eligibility_status\": \"auto\", \"auto_failure_threshold\": 0.8}'"

    # Test eligibility endpoint multiple times in auto mode
    log "${YELLOW}=== Testing Auto Mode (Multiple Runs) ===${NC}"
    for i in {1..5}; do
        execute_curl "Auto mode test run $i" "curl -s -k -L -X POST \"$BASE_URL/api/types/upgradeSession/action/verifyUpgradeEligibility\" $AUTH $HEADERS"
    done

    # 4. Test with explicit parameter override
    log "${YELLOW}=== Testing Parameter Override ===${NC}"
    execute_curl "Testing with explicit success parameter" "curl -s -k -L -X POST \"$BASE_URL/api/types/upgradeSession/action/verifyUpgradeEligibility?fail=false\" $AUTH $HEADERS"
    execute_curl "Testing with explicit failure parameter" "curl -s -k -L -X POST \"$BASE_URL/api/types/upgradeSession/action/verifyUpgradeEligibility?fail=true\" $AUTH $HEADERS"

    # 5. Reset to success mode
    log "${YELLOW}=== Resetting to Success Mode ===${NC}"
    execute_curl "Setting system back to success mode" "curl -s -k -L -X POST \"$BASE_URL/api/types/systemConfig/action/update\" $AUTH $HEADERS -H \"Content-Type: application/json\" -d '{\"eligibility_status\": \"success\"}'"

    # Final verification
    execute_curl "Final verification" "curl -s -k -L -X POST \"$BASE_URL/api/types/upgradeSession/action/verifyUpgradeEligibility\" $AUTH $HEADERS"

    log "${GREEN}All tests completed. Results saved in $LOG_FILE${NC}"
}

# Run the tests
run_tests
