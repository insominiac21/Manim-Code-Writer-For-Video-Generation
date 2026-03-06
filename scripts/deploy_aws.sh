#!/bin/bash
# MentorBoxAI - AWS ECR/ECS Deployment Script
# Prerequisites: AWS CLI configured, Docker installed

set -e

AWS_REGION="${AWS_REGION:-ap-south-1}"
AWS_ACCOUNT_ID=$(aws sts get-caller-identity --query Account --output text)
ECR_REPO="mentorboxai-backend"
IMAGE_TAG="${1:-latest}"
ECR_URI="$AWS_ACCOUNT_ID.dkr.ecr.$AWS_REGION.amazonaws.com/$ECR_REPO"

echo "🚀 Deploying MentorBoxAI to AWS..."
echo "   Region:  $AWS_REGION"
echo "   ECR URI: $ECR_URI:$IMAGE_TAG"

# 1. Authenticate Docker to ECR
echo "🔐 Authenticating with ECR..."
aws ecr get-login-password --region $AWS_REGION | \
    docker login --username AWS --password-stdin "$AWS_ACCOUNT_ID.dkr.ecr.$AWS_REGION.amazonaws.com"

# 2. Create ECR repo if it doesn't exist
aws ecr describe-repositories --repository-names $ECR_REPO --region $AWS_REGION 2>/dev/null || \
    aws ecr create-repository --repository-name $ECR_REPO --region $AWS_REGION

# 3. Build Docker image
echo "🐳 Building Docker image..."
docker build -t $ECR_REPO:$IMAGE_TAG .

# 4. Tag and push to ECR
echo "📤 Pushing to ECR..."
docker tag $ECR_REPO:$IMAGE_TAG $ECR_URI:$IMAGE_TAG
docker push $ECR_URI:$IMAGE_TAG

echo "✅ Image pushed: $ECR_URI:$IMAGE_TAG"
echo ""
echo "Next steps:"
echo "  - Deploy to ECS: aws ecs update-service --cluster mentorboxai --service backend --force-new-deployment"
echo "  - Or run on EC2: docker pull $ECR_URI:$IMAGE_TAG && docker run -d -p 8000:8000 --env-file .env $ECR_URI:$IMAGE_TAG"
