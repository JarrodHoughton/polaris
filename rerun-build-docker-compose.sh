# Bring down any currently running container in the docker-compose-jupyter.yml file
docker compose -f docker-compose-jupyter.yml down

# Delete the polaris-polaris image and it's caches
docker rmi -f polaris-polaris

# Start docker compose up again
docker compose -f docker-compose-jupyter.yml up
