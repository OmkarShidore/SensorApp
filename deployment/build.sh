docker build --build-arg REGION_ARG=$REGION --build-arg SECRET_ARN_ARG=$SECRET_ARN --build-arg DB_IDENTIFIER_ARG=$DB_IDENTIFIER --build-arg DB_NAME_ARG=$DB_NAME --build-arg DB_RESOURCE_ARN_ARG=$DB_RESOURCE_ARN -t $IMAGE_NAME -f deployment/dockerfile .
aws ecr get-login-password --region $REGION | docker login --username AWS --password-stdin $REPO_DOMAIN
docker tag $IMAGE_NAME:latest $REPO_DOMAIN/$IMAGE_NAME:latest
docker push $REPO_DOMAIN/$IMAGE_NAME:latest