#!/bin/bash

# Test script for Dell EMC Unisphere Mock API
# This script replicates the API interactions from the real API interaction record


# Create output directory if it doesn't exist



# Configuration
HOST="http://localhost:8000"
USERNAME="admin"
PASSWORD="Password123!"
COOKIE_JAR="cookie.jar"
OUTPUT_DIR="test_results"
OUTPUT_DIR="$(dirname "$(readlink -f "$0")")/$OUTPUT_DIR"
REPORT_FILE="$OUTPUT_DIR/test_report.md"
UPGRADE_FILE="$OUTPUT_DIR/test_upgrade.bin"

# Create output directory if it doesn't exist
mkdir -p $OUTPUT_DIR

# Initialize markdown report
echo "# API Test Report" > $REPORT_FILE
echo "Generated: $(date)" >> $REPORT_FILE
echo -e "\n---\n" >> $REPORT_FILE

# Colors for output
GREEN='\033[0;32m'
RED='\033[0;31m'
YELLOW='\033[0;33m'
NC='\033[0m' # No Color

# Function to print section headers
print_header() {
    echo -e "\n${YELLOW}=== $1 ===${NC}\n"
    echo -e "\n## $1\n" >> $REPORT_FILE
}

# Function to check if the API is running
check_api() {
    print_header "Checking if API is running"
    if curl -s -o /dev/null -w "%{http_code}" $HOST > /dev/null; then
        echo -e "${GREEN}API is running at $HOST${NC}"
        echo "API is running at $HOST" >> $REPORT_FILE
    else
        echo -e "${RED}API is not running at $HOST${NC}"
        echo "Please start the API server and try again"
        echo "**Error:** API is not running at $HOST" >> $REPORT_FILE
        exit 1
    fi
}

# Function to test an endpoint
test_endpoint() {
    local method=$1
    local endpoint=$2
    local auth=$3
    local description=$4
    local extra_headers=$5
    local data=$6

    print_header "$description"

    # Build the curl command
    cmd="curl -s -k -L -X $method \"$HOST$endpoint\""

    # Add authentication if needed
    if [ "$auth" = "true" ]; then
        cmd="$cmd -u \"$USERNAME:$PASSWORD\" -c $COOKIE_JAR"
    fi

    # Add the EMC REST client header
    cmd="$cmd -H \"X-EMC-REST-CLIENT: true\""

    # Add extra headers if provided
    if [ -n "$extra_headers" ]; then
        cmd="$cmd $extra_headers"
    fi

    # Add data if provided
    if [ -n "$data" ]; then
        cmd="$cmd -d '$data'"
    fi

    # Execute the command and capture output
    echo "Executing: $cmd"
    echo "### Request" >> $REPORT_FILE
    echo '```bash' >> $REPORT_FILE
    echo "$cmd" >> $REPORT_FILE
    echo '```' >> $REPORT_FILE

    # For login endpoint, capture headers to extract CSRF token
    if [[ "$endpoint" == "/api/types/loginSessionInfo/instances" ]]; then
        # Capture headers directly into a variable without creating files
        headers_and_response=$(eval "$cmd -i")
        # Extract headers and response
        headers=$(echo "$headers_and_response" | awk 'BEGIN{RS="\r\n\r\n"} NR==1')
        response=$(echo "$headers_and_response" | awk 'BEGIN{RS="\r\n\r\n"} NR==2')
        # Store CSRF token in a global variable for later use
        CSRF_TOKEN=$(echo "$headers" | grep -i "EMC-CSRF-TOKEN:" | cut -d' ' -f2 | tr -d '\r\n')
        if [ -n "$CSRF_TOKEN" ]; then
            echo -e "${GREEN}Got CSRF token: $CSRF_TOKEN${NC}"
            echo "Got CSRF token: $CSRF_TOKEN" >> $REPORT_FILE
        fi
    else
        # For other endpoints, just capture the response
        response=$(eval "$cmd")
    fi

    # Format the output with Python's json.tool
    if [ -n "$response" ]; then
        formatted_response=$(echo "$response" | python3 -m json.tool)
        echo -e "${GREEN}Received valid response${NC}"
        echo "### Response" >> $REPORT_FILE
        echo '```json' >> $REPORT_FILE
        echo "${formatted_response}" >> $REPORT_FILE
        echo '```' >> $REPORT_FILE
    else
        echo -e "${RED}Empty response received${NC}"
        echo "### Response" >> $REPORT_FILE
        echo "Empty response received" >> $REPORT_FILE
    fi
}

# Function to extract CSRF token from cookie jar
get_csrf_token() {
    # If we already have the CSRF token from the login request, use it
    if [ -n "$CSRF_TOKEN" ]; then
        echo $CSRF_TOKEN
        return
    fi

    # Otherwise, try to get it from the cookie jar as a fallback
    if [ -f "$COOKIE_JAR" ]; then
        TOKEN=$(grep -oP 'EMC-CSRF-TOKEN\s+\K[^\s]+' $COOKIE_JAR)
        echo $TOKEN
    else
        echo ""
    fi
}

# Function to create a dummy upgrade file
create_dummy_upgrade_file() {
    print_header "Creating dummy upgrade file"

    # Log to the report file
    echo "## Creating dummy upgrade file" >> $REPORT_FILE
    echo "Creating a 10MB dummy file for testing software upload" >> $REPORT_FILE

    # Create the file and capture output directly
    output=$(dd if=/dev/urandom of=$UPGRADE_FILE bs=1M count=10 2>&1)

    # Log the output to the report file
    echo '```' >> $REPORT_FILE
    echo "$output" >> $REPORT_FILE
    echo "File created: $UPGRADE_FILE (10MB)" >> $REPORT_FILE
    echo '```' >> $REPORT_FILE

    echo -e "${GREEN}Created dummy upgrade file: $UPGRADE_FILE (10MB)${NC}"
}

cleanup(){
    # Remove the dummy upgrade file
    rm -f "$UPGRADE_FILE"
    # Remove the cookie jar
    rm -f "$COOKIE_JAR"
}

# Main test sequence
main() {
    check_api

    # Test 1: Get basic system info (no auth required)
    test_endpoint "GET" "/api/types/basicSystemInfo/instances" "false" "Getting Basic System Info"

    # Test 2: Authenticate and get login session info
    test_endpoint "GET" "/api/types/loginSessionInfo/instances" "true" "Getting Login Session Info"

    # Test 3: Get auth token
    test_endpoint "POST" "/api/auth" "true" "Getting Auth Token"

    # Get the CSRF token for subsequent requests
    CSRF_TOKEN=$(get_csrf_token)
    if [ -n "$CSRF_TOKEN" ]; then
        echo -e "${GREEN}Got CSRF token: $CSRF_TOKEN${NC}"
        CSRF_HEADER="-H \"EMC-CSRF-TOKEN: $CSRF_TOKEN\""
    else
        echo -e "${RED}Failed to get CSRF token${NC}"
        CSRF_HEADER=""
    fi

    # Test 4: Get user info
    test_endpoint "GET" "/api/types/user/instances" "true" "Getting User Info"

    # Test 5: Get candidate software versions
    test_endpoint "GET" "/api/types/candidateSoftwareVersion/instances" "true" "Getting Candidate Software Versions"

    # Test 6: Get upgrade sessions
    test_endpoint "GET" "/api/types/upgradeSession/instances" "true" "Getting Upgrade Sessions"

    # Test 7: Get upgrade sessions with fields
    test_endpoint "GET" "/api/types/upgradeSession/instances?fields=status,caption,percentComplete,tasks" "true" "Getting Upgrade Sessions with Fields"

    # Test 8: Verify upgrade eligibility
    test_endpoint "POST" "/api/types/upgradeSession/action/verifyUpgradeEligibility" "true" "Verifying Upgrade Eligibility" "$CSRF_HEADER"

    # Create dummy upgrade file
    create_dummy_upgrade_file

# Test 9: Upload software package (if endpoint is implemented)
print_header "Uploading Software Package"
if [ -n "$CSRF_TOKEN" ]; then
    cmd="curl -s -k -L -X POST \"$HOST/upload/files/types/candidateSoftwareVersion\" -u \"$USERNAME:$PASSWORD\" -b $COOKIE_JAR -H \"X-EMC-REST-CLIENT: true\" -H \"EMC-CSRF-TOKEN: $CSRF_TOKEN\" -F \"file=@$UPGRADE_FILE\""
    echo "Executing: $cmd"

    # Log the request to the report file
    echo "### Request" >> $REPORT_FILE
    echo '```bash' >> $REPORT_FILE
    echo "$cmd" >> $REPORT_FILE
    echo '```' >> $REPORT_FILE

    # Execute the command and capture response directly
    upload_response=$(eval "$cmd")

    if [ -n "$upload_response" ]; then
        # Format the response directly
        formatted_response=$(echo "$upload_response" | python3 -m json.tool)
        echo -e "${GREEN}Received valid response${NC}"

        # Log the response to the report file
        echo "### Response" >> $REPORT_FILE
        echo '```json' >> $REPORT_FILE
        echo "$formatted_response" >> $REPORT_FILE
        echo '```' >> $REPORT_FILE

        echo -e "\nResponse preview:"
        echo "$formatted_response"
    else
        echo -e "${RED}Empty response received${NC}"

        # Log the empty response to the report file
        echo "### Response" >> $REPORT_FILE
        echo "Empty response received" >> $REPORT_FILE
    fi
else
    echo -e "${RED}Skipping upload test as CSRF token is not available${NC}"

    # Log the skipped test to the report file
    echo "### Request" >> $REPORT_FILE
    echo "Skipped - CSRF token not available" >> $REPORT_FILE
    echo "### Response" >> $REPORT_FILE
    echo "Skipped - CSRF token not available" >> $REPORT_FILE
fi

    # Test 10: Prepare software (if endpoint is implemented)
    test_endpoint "POST" "/api/types/candidateSoftwareVersion/action/prepare" "true" "prepare_software.json" "Preparing Software" "$CSRF_HEADER" "{\"filename\":\"$UPGRADE_FILE\"}"

    # Test 11: Create upgrade session (if endpoint is implemented)
    test_endpoint "POST" "/api/types/upgradeSession/instances" "true" "create_upgrade_session.json" "Creating Upgrade Session" "$CSRF_HEADER" "{\"candidate\":\"candidate_1\",\"pauseBeforeReboot\":true}"

    # Test 12: Resume upgrade session (if endpoint is implemented)
    test_endpoint "POST" "/api/instances/upgradeSession/Upgrade_5.3.0.120/action/resume" "true" "resume_upgrade_session.json" "Resuming Upgrade Session" "$CSRF_HEADER"

    # Test 13: Logout
    test_endpoint "POST" "/api/types/loginSessionInfo/action/logout" "true" "logout_response.json" "Logging Out" "$CSRF_HEADER" "{\"localCleanupOnly\":true}"

    print_header "Test Summary"
    echo -e "${GREEN}All tests completed. Results saved in $OUTPUT_DIR directory${NC}"
    echo "Please check the output files for details."
}

# Run the main function
main

# Cleanup
cleanup
