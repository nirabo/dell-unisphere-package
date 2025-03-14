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

# Function to extract value from JSON response
extract_json_value() {
    local json="$1"
    local path="$2"
    local value

    # Use jq if available, otherwise fallback to grep and sed
    if command -v jq &> /dev/null; then
        value=$(echo "$json" | jq -r "$path" 2>/dev/null)
    else
        # Simple fallback for basic JSON extraction
        # This is a very basic implementation and won't work for complex JSON
        value=$(echo "$json" | grep -o "\"$path\":[^,}]*" | sed 's/.*:\s*"\?\([^,}"]*\)"\?.*/\1/')
    fi

    echo "$value"
}

# Function to test the complete upgrade flow
test_upgrade_flow() {
    print_header "Testing Complete Upgrade Flow"
    echo "## Testing Complete Upgrade Flow" >> $REPORT_FILE
    echo "This test will create an upgrade session and monitor it until completion" >> $REPORT_FILE

    # 1. Get candidate software versions
    echo -e "\n${YELLOW}Step 1: Getting candidate software versions${NC}"
    echo "### Step 1: Getting candidate software versions" >> $REPORT_FILE

    CANDIDATE_CMD="curl -s -k -L -X GET \"$HOST/api/types/candidateSoftwareVersion/instances\" \
        -u \"$USERNAME:$PASSWORD\" \
        -b $COOKIE_JAR \
        -H \"X-EMC-REST-CLIENT: true\" \
        -H \"EMC-CSRF-TOKEN: $CSRF_TOKEN\""

    echo "Request:" >> $REPORT_FILE
    echo '```bash' >> $REPORT_FILE
    echo "$CANDIDATE_CMD" >> $REPORT_FILE
    echo '```' >> $REPORT_FILE

    CANDIDATE_RESPONSE=$(eval "$CANDIDATE_CMD")
    FORMATTED_CANDIDATE=$(echo "$CANDIDATE_RESPONSE" | python3 -m json.tool)

    echo "Response:" >> $REPORT_FILE
    echo '```json' >> $REPORT_FILE
    echo "$FORMATTED_CANDIDATE" >> $REPORT_FILE
    echo '```' >> $REPORT_FILE

    # Extract the first candidate ID using grep and sed
    CANDIDATE_ID=$(echo "$CANDIDATE_RESPONSE" | grep -o '"id":"[^"]*"' | head -1 | sed 's/"id":"\([^"]*\)"/\1/')

    if [ -z "$CANDIDATE_ID" ]; then
        echo -e "${RED}No candidate software versions found${NC}"
        echo "**Error:** No candidate software versions found" >> $REPORT_FILE
        return 1
    fi

    echo -e "${GREEN}Found candidate ID: $CANDIDATE_ID${NC}"
    echo "Found candidate ID: $CANDIDATE_ID" >> $REPORT_FILE

    # 2. Create an upgrade session
    echo -e "\n${YELLOW}Step 2: Creating upgrade session${NC}"
    echo "### Step 2: Creating upgrade session" >> $REPORT_FILE

    CREATE_SESSION_DATA="{\"candidate\": \"$CANDIDATE_ID\"}"
    CREATE_SESSION_CMD="curl -s -k -L -X POST \"$HOST/api/types/upgradeSession/instances\" \
        -u \"$USERNAME:$PASSWORD\" \
        -b $COOKIE_JAR \
        -H \"X-EMC-REST-CLIENT: true\" \
        -H \"EMC-CSRF-TOKEN: $CSRF_TOKEN\" \
        -H \"Content-Type: application/json\" \
        -d '$CREATE_SESSION_DATA'"

    echo "Request:" >> $REPORT_FILE
    echo '```bash' >> $REPORT_FILE
    echo "$CREATE_SESSION_CMD" >> $REPORT_FILE
    echo '```' >> $REPORT_FILE

    CREATE_SESSION_RESPONSE=$(eval "$CREATE_SESSION_CMD")
    FORMATTED_SESSION=$(echo "$CREATE_SESSION_RESPONSE" | python3 -m json.tool)

    echo "Response:" >> $REPORT_FILE
    echo '```json' >> $REPORT_FILE
    echo "$FORMATTED_SESSION" >> $REPORT_FILE
    echo '```' >> $REPORT_FILE

    # Extract the session ID using grep and sed
    SESSION_ID=$(echo "$CREATE_SESSION_RESPONSE" | grep -o '"id":"[^"]*"' | head -1 | sed 's/"id":"\([^"]*\)"/\1/')

    if [ -z "$SESSION_ID" ]; then
        echo -e "${RED}Failed to create upgrade session${NC}"
        echo "**Error:** Failed to create upgrade session" >> $REPORT_FILE
        return 1
    fi

    echo -e "${GREEN}Created upgrade session: $SESSION_ID${NC}"
    echo "Created upgrade session: $SESSION_ID" >> $REPORT_FILE

    # 3. Monitor the upgrade progress
    echo -e "\n${YELLOW}Step 3: Monitoring upgrade progress${NC}"
    echo "### Step 3: Monitoring upgrade progress" >> $REPORT_FILE
    echo "Monitoring the upgrade session until completion" >> $REPORT_FILE

    # Create a table header for task status tracking
    echo -e "\n| Time | Status | Progress | Task States |" >> $REPORT_FILE
    echo -e "|------|--------|----------|------------|" >> $REPORT_FILE

    # Initialize variables for tracking
    COMPLETED=false
    MAX_WAIT_TIME=60  # Maximum wait time in seconds
    START_TIME=$(date +%s)
    LAST_TASK_STATUS=""

    # Monitor loop
    while [ "$COMPLETED" = "false" ]; do
        # Check if we've exceeded the maximum wait time
        CURRENT_TIME=$(date +%s)
        ELAPSED_TIME=$((CURRENT_TIME - START_TIME))

        if [ $ELAPSED_TIME -gt $MAX_WAIT_TIME ]; then
            echo -e "${RED}Upgrade did not complete within $MAX_WAIT_TIME seconds${NC}"
            echo "**Error:** Upgrade did not complete within $MAX_WAIT_TIME seconds" >> $REPORT_FILE
            break
        fi

        # Get current session status
        GET_STATUS_CMD="curl -s -k -L -X GET \"$HOST/api/types/upgradeSession/instances?fields=id,status,percentComplete,tasks,messages\" \
            -u \"$USERNAME:$PASSWORD\" \
            -b $COOKIE_JAR \
            -H \"X-EMC-REST-CLIENT: true\" \
            -H \"EMC-CSRF-TOKEN: $CSRF_TOKEN\""

        STATUS_RESPONSE=$(eval "$GET_STATUS_CMD")

        # Find our session in the response using grep and awk
        SESSION_BLOCK=$(echo "$STATUS_RESPONSE" | awk -v RS='{' -v FS='}' '{for(i=1;i<=NF;i++) if($i ~ /"id":"'$SESSION_ID'"/) print "{"$i"}"}' | head -1)

        if [ -n "$SESSION_BLOCK" ]; then
            # Extract status, progress, and tasks using grep and sed
            STATUS=$(echo "$SESSION_BLOCK" | grep -o '"status":"[^"]*"' | sed 's/"status":"\([^"]*\)"/\1/')
            PROGRESS=$(echo "$SESSION_BLOCK" | grep -o '"percentComplete":[0-9]*' | sed 's/"percentComplete":\([0-9]*\)/\1/')

            # Extract tasks information
            TASKS_BLOCK=$(echo "$SESSION_BLOCK" | awk -v RS='"tasks":\[' -v FS='\]' '{print $1}')
            TASK_STATUSES=""

            # Process each task
            while read -r TASK; do
                if [ -n "$TASK" ]; then
                    TASK_NAME=$(echo "$TASK" | grep -o '"name":"[^"]*"' | sed 's/"name":"\([^"]*\)"/\1/')
                    TASK_STATUS=$(echo "$TASK" | grep -o '"status":"[^"]*"' | sed 's/"status":"\([^"]*\)"/\1/')

                    if [ -n "$TASK_NAME" ] && [ -n "$TASK_STATUS" ]; then
                        if [ -n "$TASK_STATUSES" ]; then
                            TASK_STATUSES="$TASK_STATUSES, "
                        fi
                        TASK_STATUSES="$TASK_STATUSES$TASK_NAME: $TASK_STATUS"
                    fi
                fi
            done < <(echo "$TASKS_BLOCK" | sed 's/},{/}\n{/g')

            # Format the current time
            CURRENT_TIME_FMT=$(date +"%H:%M:%S")

            # Print progress to console
            echo -e "${YELLOW}[$CURRENT_TIME_FMT] Status: $STATUS, Progress: $PROGRESS%, Tasks: $TASK_STATUSES${NC}"

            # Add to report if task status changed
            if [ "$TASK_STATUSES" != "$LAST_TASK_STATUS" ]; then
                echo -e "| $CURRENT_TIME_FMT | $STATUS | $PROGRESS% | $TASK_STATUSES |" >> $REPORT_FILE
                LAST_TASK_STATUS="$TASK_STATUSES"
            fi

            # Check if upgrade is completed
            if [ "$STATUS" = "COMPLETED" ]; then
                COMPLETED=true
                echo -e "${GREEN}Upgrade completed successfully!${NC}"
                echo "**Success:** Upgrade completed successfully!" >> $REPORT_FILE
                break
            fi

            # Check if upgrade failed
            if [ "$STATUS" = "FAILED" ]; then
                echo -e "${RED}Upgrade failed${NC}"
                echo "**Error:** Upgrade failed" >> $REPORT_FILE
                break
            fi
        else
            echo -e "${RED}Failed to get session status${NC}"
            echo "Failed to get session status" >> $REPORT_FILE
        fi

        # Wait before checking again
        sleep 2
    done

    # 4. Get final session status
    echo -e "\n${YELLOW}Step 4: Getting final session details${NC}"
    echo "### Step 4: Getting final session details" >> $REPORT_FILE

    FINAL_STATUS_CMD="curl -s -k -L -X GET \"$HOST/api/types/upgradeSession/instances?fields=id,status,percentComplete,tasks,messages\" \
        -u \"$USERNAME:$PASSWORD\" \
        -b $COOKIE_JAR \
        -H \"X-EMC-REST-CLIENT: true\" \
        -H \"EMC-CSRF-TOKEN: $CSRF_TOKEN\""

    FINAL_STATUS_RESPONSE=$(eval "$FINAL_STATUS_CMD")
    FORMATTED_FINAL_STATUS=$(echo "$FINAL_STATUS_RESPONSE" | python3 -m json.tool)

    echo "Final Status Response:" >> $REPORT_FILE
    echo '```json' >> $REPORT_FILE
    echo "$FORMATTED_FINAL_STATUS" >> $REPORT_FILE
    echo '```' >> $REPORT_FILE

    # Extract and display task completion summary
    echo -e "\n${YELLOW}Task Completion Summary:${NC}"
    echo "### Task Completion Summary" >> $REPORT_FILE
    echo "| Task Name | Status | Duration |" >> $REPORT_FILE
    echo "|-----------|--------|----------|" >> $REPORT_FILE

    # Find our session in the response
    SESSION_BLOCK=$(echo "$FINAL_STATUS_RESPONSE" | awk -v RS='{' -v FS='}' '{for(i=1;i<=NF;i++) if($i ~ /"id":"'$SESSION_ID'"/) print "{"$i"}"}' | head -1)

    if [ -n "$SESSION_BLOCK" ]; then
        # Extract tasks information
        TASKS_BLOCK=$(echo "$SESSION_BLOCK" | awk -v RS='"tasks":\[' -v FS='\]' '{print $1}')

        # Process each task
        while read -r TASK; do
            if [ -n "$TASK" ]; then
                TASK_NAME=$(echo "$TASK" | grep -o '"name":"[^"]*"' | sed 's/"name":"\([^"]*\)"/\1/')
                TASK_STATUS=$(echo "$TASK" | grep -o '"status":"[^"]*"' | sed 's/"status":"\([^"]*\)"/\1/')
                START_TIME=$(echo "$TASK" | grep -o '"startTime":"[^"]*"' | sed 's/"startTime":"\([^"]*\)"/\1/')
                END_TIME=$(echo "$TASK" | grep -o '"endTime":"[^"]*"' | sed 's/"endTime":"\([^"]*\)"/\1/')

                DURATION="N/A"
                if [ -n "$START_TIME" ] && [ -n "$END_TIME" ]; then
                    DURATION="Completed"
                elif [ -n "$START_TIME" ]; then
                    DURATION="In progress"
                fi

                echo "| $TASK_NAME | $TASK_STATUS | $DURATION |" >> $REPORT_FILE
                echo -e "| $TASK_NAME | $TASK_STATUS | $DURATION |"
            fi
        done < <(echo "$TASKS_BLOCK" | sed 's/},{/}\n{/g')
    else
        echo "No detailed task information available" >> $REPORT_FILE
        echo -e "${RED}No detailed task information available${NC}"
    fi

    return 0
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

    # Test 5: Get installed software versions
    test_endpoint "GET" "/api/types/installedSoftwareVersion/instances" "true" "Getting Installed Software Versions"

    # Test 6: Get specific installed software version
    test_endpoint "GET" "/api/instances/installedSoftwareVersion/0" "true" "Getting Specific Installed Software Version"

    # Test 7: Test complete upgrade flow
    test_upgrade_flow

    # Test 7: Get candidate software versions
    test_endpoint "GET" "/api/types/candidateSoftwareVersion/instances" "true" "Getting Candidate Software Versions"

    # Test 8: Get upgrade sessions
    test_endpoint "GET" "/api/types/upgradeSession/instances" "true" "Getting Upgrade Sessions"

    # Test 9: Get upgrade sessions with fields
    test_endpoint "GET" "/api/types/upgradeSession/instances?fields=status,caption,percentComplete,tasks" "true" "Getting Upgrade Sessions with Fields"

    # Test 10: Verify upgrade eligibility
    test_endpoint "POST" "/api/types/upgradeSession/action/verifyUpgradeEligibility" "true" "Verifying Upgrade Eligibility" "$CSRF_HEADER"

    # Create dummy upgrade file
    create_dummy_upgrade_file

# Test 11: Upload software package (if endpoint is implemented)
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

    # Test 12: Prepare software (if endpoint is implemented)
    test_endpoint "POST" "/api/types/candidateSoftwareVersion/action/prepare" "true" "prepare_software.json" "Preparing Software" "$CSRF_HEADER" "{\"filename\":\"$UPGRADE_FILE\"}"

    # Test 13: Create upgrade session (if endpoint is implemented)
    test_endpoint "POST" "/api/types/upgradeSession/instances" "true" "create_upgrade_session.json" "Creating Upgrade Session" "$CSRF_HEADER" "{\"candidate\":\"candidate_1\",\"pauseBeforeReboot\":true}"

    # Test 14: Resume upgrade session (if endpoint is implemented)
    test_endpoint "POST" "/api/instances/upgradeSession/Upgrade_5.3.0.120/action/resume" "true" "resume_upgrade_session.json" "Resuming Upgrade Session" "$CSRF_HEADER"

    # Test 15: Logout
    test_endpoint "POST" "/api/types/loginSessionInfo/action/logout" "true" "logout_response.json" "Logging Out" "$CSRF_HEADER" "{\"localCleanupOnly\":true}"

    print_header "Test Summary"
    echo -e "${GREEN}All tests completed. Results saved in $OUTPUT_DIR directory${NC}"
    echo "Please check the output files for details."
}

# Run the main function
main

# Cleanup
cleanup
