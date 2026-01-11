/**
 * Node.js Client Example for AI Content Crew API
 * 
 * Install: npm install axios
 * Usage: node examples/nodejs_client.js
 */

const axios = require('axios');

const API_BASE_URL = 'http://localhost:8000';
let API_KEY = null;

// Helper function to delay
const sleep = (ms) => new Promise(resolve => setTimeout(resolve, ms));

// 1. Sign up and get API key
async function signup(email) {
    try {
        const response = await axios.post(`${API_BASE_URL}/signup`, {
            email: email
        });
        
        console.log('✅ Signup successful!');
        console.log(`   Email: ${response.data.email}`);
        console.log(`   API Key: ${response.data.api_key}`);
        console.log(`   Plan: ${response.data.subscription_tier}`);
        
        return response.data.api_key;
    } catch (error) {
        console.error('❌ Signup failed:', error.response?.data || error.message);
        return null;
    }
}

// 2. Generate content
async function generateContent(apiKey, topic) {
    try {
        const response = await axios.post(
            `${API_BASE_URL}/generate`,
            { topic: topic },
            { headers: { 'X-API-Key': apiKey } }
        );
        
        console.log('\n🚀 Generation started!');
        console.log(`   Job ID: ${response.data.job_id}`);
        
        return response.data.job_id;
    } catch (error) {
        console.error('❌ Generation failed:', error.response?.data || error.message);
        return null;
    }
}

// 3. Check status
async function checkStatus(apiKey, jobId) {
    try {
        const response = await axios.get(
            `${API_BASE_URL}/status/${jobId}`,
            { headers: { 'X-API-Key': apiKey } }
        );
        
        return response.data;
    } catch (error) {
        console.error('❌ Status check failed:', error.response?.data || error.message);
        return null;
    }
}

// 4. Wait for completion
async function waitForCompletion(apiKey, jobId, maxWait = 300000) {
    console.log('\n⏳ Waiting for completion...');
    const startTime = Date.now();
    
    while (Date.now() - startTime < maxWait) {
        const statusData = await checkStatus(apiKey, jobId);
        
        if (statusData) {
            process.stdout.write(`   Status: ${statusData.status}\r`);
            
            if (statusData.status === 'completed') {
                console.log('\n✅ Generation completed!');
                console.log(`   Report: ${statusData.result.report}`);
                console.log(`   Blog: ${statusData.result.blog}`);
                return statusData;
            } else if (statusData.status === 'failed') {
                console.log('\n❌ Generation failed!');
                console.log(`   Error: ${statusData.error}`);
                return statusData;
            }
        }
        
        await sleep(5000); // Check every 5 seconds
    }
    
    console.log('\n⏱️  Timeout: Job did not complete');
    return null;
}

// 5. Get usage stats
async function getUsage(apiKey) {
    try {
        const response = await axios.get(
            `${API_BASE_URL}/usage`,
            { headers: { 'X-API-Key': apiKey } }
        );
        
        console.log('\n📊 Usage Statistics:');
        console.log(`   Email: ${response.data.email}`);
        console.log(`   Plan: ${response.data.subscription_tier}`);
        console.log(`   Used: ${response.data.usage_count}/${response.data.monthly_limit}`);
        console.log(`   Remaining: ${response.data.remaining}`);
        
        return response.data;
    } catch (error) {
        console.error('❌ Usage check failed:', error.response?.data || error.message);
        return null;
    }
}

// Main workflow
async function main() {
    console.log('='.repeat(60));
    console.log('AI Content Crew API - Node.js Client Example');
    console.log('='.repeat(60));
    
    // Step 1: Sign up
    console.log('\n📝 Step 1: User Signup');
    const email = `test_${Date.now()}@example.com`;
    API_KEY = await signup(email);
    
    if (!API_KEY) {
        console.log('Signup failed. Exiting...');
        return;
    }
    
    // Step 2: Generate content
    console.log('\n📝 Step 2: Generate Content');
    const topic = 'Future of Artificial Intelligence';
    const jobId = await generateContent(API_KEY, topic);
    
    if (!jobId) {
        console.log('Generation failed. Exiting...');
        return;
    }
    
    // Step 3: Wait for completion
    await waitForCompletion(API_KEY, jobId);
    
    // Step 4: Check usage
    await getUsage(API_KEY);
    
    console.log('\n' + '='.repeat(60));
    console.log('Example completed successfully!');
    console.log('='.repeat(60));
}

// Run the example
main().catch(console.error);