#!/bin/bash

# ECR 리포지토리 이름 설정
IMAGE_NAME=lambda_emtion_anaylsis_function
TAG=latest
AWS_REGION=ap-northeast-2
ECR_URL=891376935022.dkr.ecr.$AWS_REGION.amazonaws.com/$IMAGE_NAME:$TAG

# aws 인증
aws ecr get-login-password --region $AWS_REGION | docker login --username AWS --password-stdin $ECR_URL

# Docker 이미지 빌드
docker build -t $IMAGE_NAME .

#이미지 태그 지정하여 푸쉬 준비
docker tag $IMAGE_NAME:$TAG $ECR_URL

# Docker 이미지 푸시
docker push $ECR_URL

# ECR 리포지토리 URL 출력
echo "ECR Repository URL: $ECR_URL"

