pipeline {
    agent any

    environment {
        DOCKER_IMAGE_NAME = "wikipedia"
        DOCKER_TAG = "latest"
    }

    stages {
        stage('Checkout') {
            steps {
                checkout scm
            }
        }

        stage('Build Docker Image') {
            steps {
                script {
                    // You may include additional build steps or customizations here
                    sh "docker build -t ${DOCKER_IMAGE_NAME}:${DOCKER_TAG} ."
                }
            }
        }

        stage('Deploy Locally') {
            steps {
                script {
                    // Stop and remove the existing container if it exists
                    sh "docker stop ${DOCKER_IMAGE_NAME} || true"
                    sh "docker rm ${DOCKER_IMAGE_NAME} || true"

                    // Run the new container
                    sh "docker run -d --name ${DOCKER_IMAGE_NAME} -p 8080:80 ${DOCKER_IMAGE_NAME}:${DOCKER_TAG}"
                }
            }
        }
    }

    post {
        success {
            echo "Docker image build and deployment successful!"
        }
        failure {
            echo "Build or deployment failed. Check the Jenkins logs for details."
        }
    }
}
