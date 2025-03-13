# X-EMC-REST-CLIENT Header Validation Test Report
Generated: Thu Mar 13 09:16:53 AM EET 2025

---


## Testing X-EMC-REST-CLIENT Header Validation


## Testing GET /api/types/basicSystemInfo/instances

### Test 1: Missing header
```bash
curl -s -k -L -X GET "http://localhost:8000/api/types/basicSystemInfo/instances" -o /dev/null -w "%{http_code}"
```
Result: ✅ Passed - Received expected status code 401

### Test 2: Incorrect header value
```bash
curl -s -k -L -X GET "http://localhost:8000/api/types/basicSystemInfo/instances" -H "X-EMC-REST-CLIENT: false" -o /dev/null -w "%{http_code}"
```
Result: ✅ Passed - Received expected status code 401

### Test 3: Correct header value (control test)
```bash
curl -s -k -L -X GET "http://localhost:8000/api/types/basicSystemInfo/instances" -H "X-EMC-REST-CLIENT: true" -o /dev/null -w "%{http_code}"
```
Result: ✅ Passed - Received status code 200 (not 401)

## Testing Authentication with GET /api/types/loginSessionInfo/instances

### Test 1: Missing header
```bash
curl -s -k -L -X GET "http://localhost:8000/api/types/loginSessionInfo/instances" -o /dev/null -w "%{http_code}"
```
Result: ✅ Passed - Received expected status code 401

### Test 2: Incorrect header value
```bash
curl -s -k -L -X GET "http://localhost:8000/api/types/loginSessionInfo/instances" -H "X-EMC-REST-CLIENT: false" -o /dev/null -w "%{http_code}"
```
Result: ✅ Passed - Received expected status code 401

### Test 3: Correct header value (control test)
```bash
curl -s -k -L -X GET "http://localhost:8000/api/types/loginSessionInfo/instances" -u "admin:Password123!" -H "X-EMC-REST-CLIENT: true" -o /dev/null -w "%{http_code}"
```
Result: ✅ Passed - Received status code 200 (not 401)

## Test Summary


## Test Summary

All header validation tests completed. Check the results above for details.
