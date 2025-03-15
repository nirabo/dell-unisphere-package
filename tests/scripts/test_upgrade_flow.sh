#!/bin/bash

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[0;33m'
CYAN='\033[0;36m'
NC='\033[0m' # No Color

# Configuration
HOST="http://localhost:8000"
USERNAME="admin"
PASSWORD="Password123!"
COOKIE_JAR="cookie.jar"
REPORT_DIR="./tests/scripts/test_results"
REPORT_FILE="$REPORT_DIR/test_upgrade_flow_report.md"
UPGRADE_FILE="$REPORT_DIR/test_upgrade.bin"

# Create report directory if it doesn't exist
mkdir -p "$REPORT_DIR"

# Initialize report file
echo "# Dell Unisphere Mock API - Upgrade Flow Test Report" > $REPORT_FILE
echo "Generated on: $(date)" >> $REPORT_FILE
echo "" >> $REPORT_FILE

# Function to print a header
print_header() {
    echo -e "\n${YELLOW}=== $1 ===${NC}"
    echo -e "\n## $1" >> $REPORT_FILE
}

# Function to check if API is running
check_api() {
    print_header "Checking if API is running"

    if curl -s "$HOST/docs" > /dev/null; then
        echo -e "${GREEN}API is running at $HOST${NC}"
        echo "API is running at $HOST" >> $REPORT_FILE
        return 0
    else
        echo -e "${RED}API is not running at $HOST${NC}"
        echo "API is not running at $HOST" >> $REPORT_FILE
        return 1
    fi
}

# Function to get CSRF token from cookie jar
get_csrf_token() {
    if [ -f "$COOKIE_JAR" ]; then
        CSRF_TOKEN=$(grep -oP 'EMC-CSRF-TOKEN\s+\K[^\s]+' "$COOKIE_JAR" | head -1)
        if [ -n "$CSRF_TOKEN" ]; then
            echo "$CSRF_TOKEN"
            return 0
        fi
    fi

    # If no token found in cookie jar, get it from login
    LOGIN_CMD="curl -s -k -L -X GET \"$HOST/api/types/loginSessionInfo/instances\" \
        -u \"$USERNAME:$PASSWORD\" \
        -c $COOKIE_JAR \
        -H \"X-EMC-REST-CLIENT: true\""

    LOGIN_RESPONSE=$(eval "$LOGIN_CMD")

    # Extract CSRF token from response or cookie jar
    CSRF_TOKEN=$(grep -oP 'EMC-CSRF-TOKEN\s+\K[^\s]+' "$COOKIE_JAR" | head -1)

    if [ -z "$CSRF_TOKEN" ]; then
        echo -e "${RED}Failed to get CSRF token${NC}"
        return 1
    fi

    echo "$CSRF_TOKEN"
}

# Function to create a dummy upgrade file
create_dummy_upgrade_file() {
    print_header "Creating dummy upgrade file"
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

# Function to test the complete upgrade flow
test_upgrade_flow() {
    print_header "Testing Complete Upgrade Flow"
    echo "This test will create an upgrade session and monitor it until completion" >> $REPORT_FILE

    # Get CSRF token
    CSRF_TOKEN=$(get_csrf_token)
    if [ -z "$CSRF_TOKEN" ]; then
        echo -e "${RED}Failed to get CSRF token${NC}"
        echo "**Error:** Failed to get CSRF token" >> $REPORT_FILE
        return 1
    fi

    echo -e "${GREEN}Got CSRF token: $CSRF_TOKEN${NC}"
    echo "Got CSRF token: $CSRF_TOKEN" >> $REPORT_FILE

    # 1. Create a dummy upgrade file
    echo -e "\n${YELLOW}Step 1: Creating dummy upgrade file${NC}"
    echo "### Step 1: Creating dummy upgrade file" >> $REPORT_FILE

    create_dummy_upgrade_file

    # 2. Upload the file to create a candidate software version
    echo -e "\n${YELLOW}Step 2: Uploading software package${NC}"
    echo "### Step 2: Uploading software package" >> $REPORT_FILE

    UPLOAD_CMD="curl -s -k -L -X POST \"$HOST/upload/files/types/candidateSoftwareVersion\" \\
        -u \"$USERNAME:$PASSWORD\" \\
        -b $COOKIE_JAR \\
        -H \"X-EMC-REST-CLIENT: true\" \\
        -H \"EMC-CSRF-TOKEN: $CSRF_TOKEN\" \\
        -F \"file=@$UPGRADE_FILE\""

    echo "Request:" >> $REPORT_FILE
    echo '```bash' >> $REPORT_FILE
    echo "$UPLOAD_CMD" >> $REPORT_FILE
    echo '```' >> $REPORT_FILE

    UPLOAD_RESPONSE=$(eval "$UPLOAD_CMD")
    FORMATTED_UPLOAD=$(echo "$UPLOAD_RESPONSE" | python3 -m json.tool)

    echo "Response:" >> $REPORT_FILE
    echo '```json' >> $REPORT_FILE
    echo "$FORMATTED_UPLOAD" >> $REPORT_FILE
    echo '```' >> $REPORT_FILE

    # Extract the file ID
    FILE_ID=$(echo "$UPLOAD_RESPONSE" | python3 -c "
import sys, json
try:
    data = json.load(sys.stdin)
    if 'id' in data:
        print(data['id'])
except Exception as e:
    pass
")

    if [ -z "$FILE_ID" ]; then
        echo -e "${RED}Failed to upload software package${NC}"
        echo "**Error:** Failed to upload software package" >> $REPORT_FILE
        return 1
    fi

    echo -e "${GREEN}Uploaded software package: $FILE_ID${NC}"
    echo "Uploaded software package: $FILE_ID" >> $REPORT_FILE

    # 3. Prepare the software
    echo -e "\n${YELLOW}Step 3: Preparing software${NC}"
    echo "### Step 3: Preparing software" >> $REPORT_FILE

    PREPARE_CMD="curl -s -k -L -X POST \"$HOST/api/types/candidateSoftwareVersion/action/prepare\" \\
        -u \"$USERNAME:$PASSWORD\" \\
        -b $COOKIE_JAR \\
        -H \"X-EMC-REST-CLIENT: true\" \\
        -H \"EMC-CSRF-TOKEN: $CSRF_TOKEN\" \\
        -H \"Content-Type: application/json\" \\
        -d '{\"filename\":\"$FILE_ID\"}'"

    echo "Request:" >> $REPORT_FILE
    echo '```bash' >> $REPORT_FILE
    echo "$PREPARE_CMD" >> $REPORT_FILE
    echo '```' >> $REPORT_FILE

    PREPARE_RESPONSE=$(eval "$PREPARE_CMD")
    FORMATTED_PREPARE=$(echo "$PREPARE_RESPONSE" | python3 -m json.tool)

    echo "Response:" >> $REPORT_FILE
    echo '```json' >> $REPORT_FILE
    echo "$FORMATTED_PREPARE" >> $REPORT_FILE
    echo '```' >> $REPORT_FILE

    # 4. Get candidate software versions
    echo -e "\n${YELLOW}Step 4: Getting candidate software versions${NC}"
    echo "### Step 4: Getting candidate software versions" >> $REPORT_FILE

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

    # Extract the first candidate ID using Python for better JSON handling
    CANDIDATE_ID=$(echo "$CANDIDATE_RESPONSE" | python3 -c "
import sys, json
try:
    data = json.load(sys.stdin)
    if 'entries' in data and len(data['entries']) > 0:
        for entry in data['entries']:
            if 'content' in entry and 'id' in entry['content']:
                print(entry['content']['id'])
                break
except Exception as e:
    pass
")

    # Fallback to grep if Python extraction fails
    if [ -z "$CANDIDATE_ID" ]; then
        CANDIDATE_ID=$(echo "$CANDIDATE_RESPONSE" | grep -o '"id":"[^"]*"' | head -1 | sed 's/"id":"\([^"]*\)"/\1/')
    fi

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

    # First, check if there are any existing sessions with the same name
    # and delete them to avoid conflicts
    SESSIONS_CMD="curl -s -k -L -X GET \"$HOST/api/types/upgradeSession/instances\" \
        -u \"$USERNAME:$PASSWORD\" \
        -b $COOKIE_JAR \
        -H \"X-EMC-REST-CLIENT: true\" \
        -H \"EMC-CSRF-TOKEN: $CSRF_TOKEN\""

    SESSIONS_RESPONSE=$(eval "$SESSIONS_CMD")

    # Create the upgrade session
    CREATE_SESSION_DATA="{\"candidate\": \"$CANDIDATE_ID\"}"
    CREATE_SESSION_CMD="curl -s -k -L -X POST \"$HOST/api/types/upgradeSession/instances\" \
        -u \"$USERNAME:$PASSWORD\" \
        -b $COOKIE_JAR \
        -H \"X-EMC-REST-CLIENT: true\" \
        -H \"EMC-CSRF-TOKEN: $CSRF_TOKEN\" \
        -d \"$CREATE_SESSION_DATA\""

    # Execute the command to create the upgrade session
    CREATE_SESSION_RESPONSE=$(eval "$CREATE_SESSION_CMD")

    # Check if the session was created successfully
    if [[ $? -ne 0 ]]; then
        echo -e "${RED}Failed to create upgrade session${NC}"
        echo "**Error:** Failed to create upgrade session" >> $REPORT_FILE
        return 1
    fi

    # Extract the session ID from the response
    SESSION_ID=$(echo "$CREATE_SESSION_RESPONSE" | python3 -c "import sys, json; data = json.load(sys.stdin); print(data['id'])")

    if [ -z "$SESSION_ID" ]; then
        echo -e "${RED}Failed to extract session ID${NC}"
        echo "**Error:** Failed to extract session ID" >> $REPORT_FILE
        return 1
    fi

    echo -e "${GREEN}Created upgrade session: $SESSION_ID${NC}"

    # 3. Monitor the upgrade progress
    echo -e "\n${YELLOW}Step 3: Monitoring upgrade progress${NC}"
    echo "### Step 3: Monitoring upgrade progress" >> $REPORT_FILE
    echo "Monitoring the upgrade session until completion" >> $REPORT_FILE

    # Create a table header for task status tracking
    echo -e "\n| Time | Status | Progress | Task States |" >> $REPORT_FILE
    echo -e "|------|--------|----------|------------|" >> $REPORT_FILE

    # Initialize variables for tracking
    COMPLETED=false
    MAX_WAIT_TIME=120  # Maximum wait time in seconds
    START_TIME=$(date +%s)
    LAST_TASK_STATUS=""
    LAST_TASK_DETAILS=""

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
        GET_STATUS_CMD="curl -s -k -L -X GET \"$HOST/api/instances/upgradeSession/$SESSION_ID?fields=id,status,percentComplete,tasks,messages\" \
            -u \"$USERNAME:$PASSWORD\" \
            -b $COOKIE_JAR \
            -H \"X-EMC-REST-CLIENT: true\" \
            -H \"EMC-CSRF-TOKEN: $CSRF_TOKEN\""

        STATUS_RESPONSE=$(eval "$GET_STATUS_CMD")

        # Process the response with Python for better JSON handling
        SESSION_INFO=$(echo "$STATUS_RESPONSE" | python3 -c "
import sys, json

try:
    data = json.load(sys.stdin)

    # Extract content from the Dell Unisphere API response structure
    if 'content' in data:
        # We're dealing with a single session response
        content = data['content']
    elif 'entries' in data and len(data['entries']) > 0 and 'content' in data['entries'][0]:
        # We're dealing with a list response, get the first entry's content
        content = data['entries'][0]['content']
    else:
        # Fallback to the original data
        content = data

    # Get session info
    status = content.get('status', 0)
    progress = content.get('percentComplete', 0)

    # Status mapping
    status_map = {0: 'PENDING', 1: 'IN_PROGRESS', 2: 'COMPLETED', 3: 'FAILED', 4: 'PAUSED'}
    status_text = status_map.get(status, status)

    # Get task statuses
    task_statuses = []
    task_details = []
    for task in content.get('tasks', []):
        task_caption = task.get('caption', 'Unknown')
        task_status = task.get('status', 0)
        task_status_text = status_map.get(task_status, task_status)
        task_statuses.append(f'{task_caption}: {task_status_text}')

        # Add more details for the report
        task_details.append({
            'caption': task_caption,
            'status': task_status,
            'status_text': task_status_text,
            'type': task.get('type', ''),
            'creationTime': task.get('creationTime', ''),
            'startTime': task.get('startTime', ''),
            'endTime': task.get('endTime', '')
        })

    # Format as JSON for easy parsing
    output = {
        'status': status,
        'status_text': status_text,
        'progress': progress,
        'task_statuses': task_statuses,
        'task_details': task_details
    }
    print(json.dumps(output))
except Exception as e:
    print('{}')")

        # Parse the session info
        if [ -n "$SESSION_INFO" ] && [ "$SESSION_INFO" != "{}" ]; then
            STATUS=$(echo "$SESSION_INFO" | python3 -c "import sys, json; data=json.load(sys.stdin); print(data.get('status', 0))")
            STATUS_TEXT=$(echo "$SESSION_INFO" | python3 -c "import sys, json; data=json.load(sys.stdin); print(data.get('status_text', 'UNKNOWN'))")
            PROGRESS=$(echo "$SESSION_INFO" | python3 -c "import sys, json; data=json.load(sys.stdin); print(data.get('progress', 0))")
            TASK_STATUSES=$(echo "$SESSION_INFO" | python3 -c "import sys, json; data=json.load(sys.stdin); print('\n'.join(data.get('task_statuses', [])))")
            TASK_DETAILS=$(echo "$SESSION_INFO" | python3 -c "import sys, json; data=json.load(sys.stdin); print(json.dumps(data.get('task_details', [])))")

            # Format the current time
            CURRENT_TIME_FMT=$(date +"%H:%M:%S")

            # Print progress to console
            echo -e "${YELLOW}[$CURRENT_TIME_FMT] Status: $STATUS_TEXT, Progress: $PROGRESS%${NC}"
            if [ -n "$TASK_STATUSES" ]; then
                echo -e "${CYAN}Tasks:${NC}"
                echo -e "$TASK_STATUSES" | while read -r TASK; do
                    if [ -n "$TASK" ]; then
                        echo -e "  ${CYAN}$TASK${NC}"
                    fi
                done
            fi

            # Add to report if task status changed
            if [ "$TASK_DETAILS" != "$LAST_TASK_DETAILS" ]; then
                TASK_STATUS_FORMATTED=$(echo "$TASK_STATUSES" | tr '\n' ', ' | sed 's/,$//')
                echo -e "| $CURRENT_TIME_FMT | $STATUS_TEXT | $PROGRESS% | $TASK_STATUS_FORMATTED |" >> $REPORT_FILE
                LAST_TASK_DETAILS="$TASK_DETAILS"

                # Log state changes in detail
                echo -e "\n#### Task State Changes at $CURRENT_TIME_FMT" >> $REPORT_FILE
                echo -e "| Task | Status |" >> $REPORT_FILE
                echo -e "|------|--------|" >> $REPORT_FILE

                echo "$TASK_DETAILS" | python3 -c "
import sys, json
tasks = json.load(sys.stdin)
for task in tasks:
    print(f\"| {task.get('caption', 'Unknown')} | {task.get('status_text', 'UNKNOWN')} |\")
" >> $REPORT_FILE
            fi

            # Check if upgrade is completed
            if [ "$STATUS" = "2" ] || [ "$STATUS_TEXT" = "COMPLETED" ]; then
                COMPLETED=true
                echo -e "${GREEN}Upgrade completed successfully!${NC}"
                echo "**Success:** Upgrade completed successfully!" >> $REPORT_FILE
                break
            fi

            # Check if upgrade failed
            if [ "$STATUS" = "3" ] || [ "$STATUS_TEXT" = "FAILED" ]; then
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

    # 4. Get final session details
    echo -e "\n${YELLOW}Step 4: Getting final session details${NC}"
    echo "### Step 4: Getting final session details" >> $REPORT_FILE

    FINAL_STATUS_CMD="curl -s -k -L -X GET \"$HOST/api/instances/upgradeSession/$SESSION_ID?fields=id,status,percentComplete,tasks,messages\" \
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

    # Extract and display task completion summary using Python for better JSON handling
    echo -e "\n${YELLOW}Task Completion Summary:${NC}"
    echo "### Task Completion Summary" >> $REPORT_FILE
    echo "| Task Name | Status | Duration |" >> $REPORT_FILE
    echo "|-----------|--------|----------|" >> $REPORT_FILE

    # Process the final status with Python
    TASK_SUMMARY=$(echo "$FINAL_STATUS_RESPONSE" | python3 -c "
import sys, json

try:
    data = json.load(sys.stdin)

    # Status mapping
    status_map = {0: 'PENDING', 1: 'IN_PROGRESS', 2: 'COMPLETED', 3: 'FAILED', 4: 'PAUSED'}

    for task in data.get('tasks', []):
        caption = task.get('caption', 'Unknown')
        status = task.get('status', 0)
        status_text = status_map.get(status, status)

        start_time = task.get('startTime', '')
        end_time = task.get('endTime', '')

        duration = 'N/A'
        if start_time and end_time:
            duration = 'Completed'
        elif start_time:
            duration = 'In progress'

        print(f'| {caption} | {status_text} | {duration} |')
except Exception as e:
    print(f'| Error processing tasks: {str(e)} | N/A | N/A |')
")

    echo "$TASK_SUMMARY" >> $REPORT_FILE
    echo -e "$TASK_SUMMARY"

    return 0
}

# Function to clean up
cleanup() {
    # Remove the dummy upgrade file
    rm -f "$UPGRADE_FILE"
    # Remove the cookie jar
    rm -f "$COOKIE_JAR"
}

# Main execution
check_api || exit 1
test_upgrade_flow
cleanup
