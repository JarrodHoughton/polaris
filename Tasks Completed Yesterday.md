Tasks Completed Yesterday:
- Implemented Postgres deployment for Polaris on Kubernetes
    - which pulls in secrets to create the admin user
- Implemented Polaris deployment on Kubernetes
    - also uses secrets for AWS credentials and docker-registry secret for a custom polaris image I've been builind and using
- Added code to the Polaris repository to implement dynamic environment variables for the database connection of Eclipse Link
    - Currently still debugging and definitely a blocker at the moment
- Implemented Init-Container for Polaris to automate the creation of a catalog + namespace + setup the S3 warehouse location + polaris IAM Role ARN