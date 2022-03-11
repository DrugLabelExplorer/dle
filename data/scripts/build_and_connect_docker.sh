docker build -t dle_database:v1 .
DOCKER_PS=$(docker run -dit dle_database:v1)
docker attach $DOCKER_PS
