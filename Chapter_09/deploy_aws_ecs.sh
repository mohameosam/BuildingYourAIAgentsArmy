#!/bin/bash
# File: deploy_aws_ecs.sh
# Chapter 9: Deploying AI Agents on AWS ECS
# This script deploys the AI agents to AWS ECS using Docker.

# Set variables
CLUSTER_NAME="ai-agent-cluster"
SERVICE_NAME="ai-agent-service"
TASK_DEF="ai-agent-task"

# Create ECS cluster
echo "Creating ECS cluster..."
aws ecs create-cluster --cluster-name $CLUSTER_NAME

# Register task definition
echo "Registering task definition..."
aws ecs register-task-definition --cli-input-json file://task-definition.json

# Create service
echo "Creating ECS service..."
aws ecs create-service \
    --cluster $CLUSTER_NAME \
    --service-name $SERVICE_NAME \
    --task-definition $TASK_DEF \
    --desired-count 1 \
    --launch-type FARGATE

# Wait for service to stabilize
echo "Waiting for service to stabilize..."
aws ecs wait services-stable --cluster $CLUSTER_NAME --services $SERVICE_NAME

echo "Deployment complete."