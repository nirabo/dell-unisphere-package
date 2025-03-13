#!/bin/bash

# Test script for X-EMC-REST-CLIENT header validation
# This script tests the behavior when the header is missing or not equal to "true"

# Configuration
HOST="http://localhost:8000"
USERNAME="admin"
PASSWORD="Password123!"
OUTPUT_DIR="test_results"
HEADER_TEST_REPORT="$OUTPUT_DIR/header_validation_report.md"

# Create output directory if it doesn't exist
mkdir -p $OUTPUT_DIR

# Initialize markdown report
echo "# X-EMC-REST-CLIENT Header Validation Test Report" > $HEADER_TEST_REPORT
echo "Generated: $(date)" >> $HEADER_TEST_REPORT
echo -e "\n---\n" >> $HEADER_TEST_REPORT

# Colors for output
GREEN='\033[0;32m'
RED='\033[0;31m'
YELLOW='\033[0;33m'
NC='\033[0m' # No Color

# Function to print section headers
print_header() {
    echo -e "\n${YELLOW}=== $1 ===${NC}\n"
    echo -e "\n## $1\n" >> $HEADER_TEST_REPORT
}

# Function to test an endpoint with different header configurations
test_header_validation() {
    local method=$1
    local endpoint=$2
    local description=$3
    local expected_status=$4
    local auth_required=$5

    print_header "$description"

    # Test 1: Missing header
    echo -e "${YELLOW}Testing with missing header${NC}"
    echo "### Test 1: Missing header" >> $HEADER_TEST_REPORT

    cmd="curl -s -k -L -X $method \"$HOST$endpoint\" -o /dev/null -w \"%{http_code}\""

    echo "Executing: $cmd"
    echo '```bash' >> $HEADER_TEST_REPORT
    echo "$cmd" >> $HEADER_TEST_REPORT
    echo '```' >> $HEADER_TEST_REPORT

    status_code=$(eval "$cmd")

    if [ "$status_code" -eq "$expected_status" ]; then
        echo -e "${GREEN}Test passed: Received expected status code $status_code${NC}"
        echo "Result: ✅ Passed - Received expected status code $status_code" >> $HEADER_TEST_REPORT
    else
        echo -e "${RED}Test failed: Expected status code $expected_status but got $status_code${NC}"
        echo "Result: ❌ Failed - Expected status code $expected_status but got $status_code" >> $HEADER_TEST_REPORT
    fi

    # Test 2: Header with incorrect value
    echo -e "\n${YELLOW}Testing with incorrect header value${NC}"
    echo -e "\n### Test 2: Incorrect header value" >> $HEADER_TEST_REPORT

    cmd="curl -s -k -L -X $method \"$HOST$endpoint\" -H \"X-EMC-REST-CLIENT: false\" -o /dev/null -w \"%{http_code}\""

    echo "Executing: $cmd"
    echo '```bash' >> $HEADER_TEST_REPORT
    echo "$cmd" >> $HEADER_TEST_REPORT
    echo '```' >> $HEADER_TEST_REPORT

    status_code=$(eval "$cmd")

    if [ "$status_code" -eq "$expected_status" ]; then
        echo -e "${GREEN}Test passed: Received expected status code $status_code${NC}"
        echo "Result: ✅ Passed - Received expected status code $status_code" >> $HEADER_TEST_REPORT
    else
        echo -e "${RED}Test failed: Expected status code $expected_status but got $status_code${NC}"
        echo "Result: ❌ Failed - Expected status code $expected_status but got $status_code" >> $HEADER_TEST_REPORT
    fi

    # Test 3: Header with correct value (control test)
    echo -e "\n${YELLOW}Testing with correct header value (control test)${NC}"
    echo -e "\n### Test 3: Correct header value (control test)" >> $HEADER_TEST_REPORT

    # Add authentication if required
    if [ "$auth_required" = "true" ]; then
        cmd="curl -s -k -L -X $method \"$HOST$endpoint\" -u \"$USERNAME:$PASSWORD\" -H \"X-EMC-REST-CLIENT: true\" -o /dev/null -w \"%{http_code}\""
    else
        cmd="curl -s -k -L -X $method \"$HOST$endpoint\" -H \"X-EMC-REST-CLIENT: true\" -o /dev/null -w \"%{http_code}\""
    fi

    echo "Executing: $cmd"
    echo '```bash' >> $HEADER_TEST_REPORT
    echo "$cmd" >> $HEADER_TEST_REPORT
    echo '```' >> $HEADER_TEST_REPORT

    status_code=$(eval "$cmd")

    # For the control test, we expect a successful status code (not 401)
    if [ "$status_code" -ne "$expected_status" ]; then
        echo -e "${GREEN}Control test passed: Received status code $status_code (not $expected_status)${NC}"
        echo "Result: ✅ Passed - Received status code $status_code (not $expected_status)" >> $HEADER_TEST_REPORT
    else
        echo -e "${RED}Control test failed: Received status code $status_code (expected not $expected_status)${NC}"
        echo "Result: ❌ Failed - Received status code $status_code (expected not $expected_status)" >> $HEADER_TEST_REPORT
    fi
}

# Main test sequence
main() {
    print_header "Testing X-EMC-REST-CLIENT Header Validation"

    # Test GET endpoints
    test_header_validation "GET" "/api/types/basicSystemInfo/instances" "Testing GET /api/types/basicSystemInfo/instances" 401 "false"

    # Test authentication with loginSessionInfo endpoint
    test_header_validation "GET" "/api/types/loginSessionInfo/instances" "Testing Authentication with GET /api/types/loginSessionInfo/instances" 401 "true"

    print_header "Test Summary"
    echo "Header validation tests completed. Results saved in $HEADER_TEST_REPORT"
    echo -e "\n## Test Summary\n" >> $HEADER_TEST_REPORT
    echo "All header validation tests completed. Check the results above for details." >> $HEADER_TEST_REPORT
}

# Run the main function
main
