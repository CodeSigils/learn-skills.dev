---
name: aws-lambda
description: "Design, build, and deploy serverless event-driven functions using AWS Lambda."
---

# AWS Lambda Development

## Overview
AWS Lambda allows you to run code without provisioning or managing servers, executing only when triggered by events. This skill should be invoked when building microservices, event-driven architectures, background jobs, or API backends that require rapid scaling. 

## Core Principles
- **Statelessness**: Lambda functions are ephemeral. Any persistent state must be stored in external services (like DynamoDB, S3, or RDS).
- **Event-Driven**: Functions should be designed to react to specific triggers (API Gateway requests, S3 bucket uploads, SQS messages).
- **Fast Execution**: AWS charges based on execution time and memory. Optimize code for fast startup and quick processing.
- **Least Privilege**: Grant the Lambda execution role only the specific AWS permissions required to perform its task.

## Preparation Checklist
- [ ] Determine the trigger source (e.g., API Gateway, EventBridge, SQS).
- [ ] Select the appropriate runtime (Node.js, Python, Go, etc.) based on team expertise and performance needs.
- [ ] Identify dependencies and plan how they will be packaged (e.g., Lambda Layers, bundling with Webpack/esbuild).

## Step-by-Step Process
1. **Define the Handler**: Write the core function signature `handler(event, context)` ensuring it correctly parses the incoming `event` payload.
2. **Implement Business Logic**: Separate the core logic from the handler. The handler should only deal with event parsing and response formatting.
3. **Manage Configuration**: Use Environment Variables for dynamic configuration (database strings, API keys).
4. **Local Testing**: Mock the specific AWS event payload locally to test the logic before deployment.
5. **Optimize Cold Starts**: 
   - Move database connections or heavy initializations outside the handler function (in the global scope) so they are reused in warm invocations.
   - Keep the deployment package size small.
6. **Deployment & Logging**: Deploy via IaC tools (AWS SAM, Serverless Framework, CDK, or Terraform). Ensure robust logging using `console.log` or a structured logger to CloudWatch.

## Do's and Don'ts
- ✅ **Do** use proper error handling to ensure visibility into failures and to correctly trigger DLQs (Dead Letter Queues) if needed.
- ✅ **Do** configure concurrency limits and timeouts appropriately to control costs and prevent runaway processes.
- ❌ **Don't** store sensitive secrets in plain text environment variables; use AWS Secrets Manager or Parameter Store.
- ❌ **Don't** build massive "monolithic" Lambda functions that route dozens of different endpoints internally.

## Anti-Patterns
- **The Recursive Loop**: A Lambda function that triggers itself (e.g., reading from an S3 bucket and writing back to it, which triggers the function again), leading to massive bills.
- **Timeouts**: Setting a 3-second timeout for a function that calls a slow third-party API, causing constant failures.
- **Heavy Frameworks**: Using heavy web frameworks (like full Spring Boot) inside a Lambda, causing multi-second cold starts.
