#!/bin/bash

API_URL="http://localhost:8000"

echo "=========================================="
echo "AI Content Crew API - Complete Test Flow"
echo "=========================================="

# Step 1: Sign up
echo -e "\n📝 Step 1: Signing up..."
SIGNUP_RESPONSE=$(curl -s -X POST "$API_URL/signup" \
  -H "Content-Type: application/json" \
  -d '{"email": "test_'$(date +%s)'@example.com"}')

echo "$SIGNUP_RESPONSE" | jq '.'

API_KEY=$(echo "$SIGNUP_RESPONSE" | jq -r '.api_key')
echo "✅ Got API Key: $API_KEY"

# Step 2: Generate content
echo -e "\n🚀 Step 2: Starting content generation..."
GENERATE_RESPONSE=$(curl -s -X POST "$API_URL/generate" \
  -H "Content-Type: application/json" \
  -H "X-API-Key: $API_KEY" \
  -d '{"topic": "Future of Artificial Intelligence"}')

echo "$GENERATE_RESPONSE" | jq '.'

JOB_ID=$(echo "$GENERATE_RESPONSE" | jq -r '.job_id')
echo "✅ Got Job ID: $JOB_ID"

# Step 3: Check status (poll every 5 seconds)
echo -e "\n⏳ Step 3: Waiting for completion..."
MAX_WAIT=180  # 3 minutes
ELAPSED=0

while [ $ELAPSED -lt $MAX_WAIT ]; do
    STATUS_RESPONSE=$(curl -s -X GET "$API_URL/status/$JOB_ID" \
      -H "X-API-Key: $API_KEY")
    
    STATUS=$(echo "$STATUS_RESPONSE" | jq -r '.status')
    
    echo -n "   Status: $STATUS (${ELAPSED}s elapsed)    "
    
    if [ "$STATUS" == "completed" ]; then
        echo -e "\n✅ Generation completed!"
        echo "$STATUS_RESPONSE" | jq '.'
        
        echo -e "\n📄 Files created:"
        echo "$STATUS_RESPONSE" | jq -r '.result.report'
        echo "$STATUS_RESPONSE" | jq -r '.result.blog'
        break
    elif [ "$STATUS" == "failed" ]; then
        echo -e "\n❌ Generation failed!"
        echo "$STATUS_RESPONSE" | jq '.'
        break
    fi
    
    sleep 5
    ELAPSED=$((ELAPSED + 5))
done

if [ $ELAPSED -ge $MAX_WAIT ]; then
    echo -e "\n⏱️  Timeout: Job did not complete in ${MAX_WAIT} seconds"
fi

# Step 4: Check usage
echo -e "\n📊 Step 4: Checking usage statistics..."
curl -s -X GET "$API_URL/usage" \
  -H "X-API-Key: $API_KEY" | jq '.'

echo -e "\n=========================================="
echo "Test completed!"
echo "=========================================="