pipeline {
    agent any

    environment {
        DOCKER_IMAGE_NAME = "testapp"
        DOCKER_TAG = "latest"
    }

    stages {
        stage('Clone repository') {
            steps {
                checkout scm
            }
        }

        stage('Build image') {
            steps {
                script {
                    // This builds the actual image
                    docker.build(DOCKER_IMAGE_NAME)
                }
            }
        }

        stage('Test image') {
            steps {
                script {
                    // Run tests using a Node.js testing framework (e.g., Mocha or Jest)
                    docker.image(DOCKER_IMAGE_NAME).inside {
                        sh 'npm install' // Install dependencies
                        sh 'npm test'     // Run tests
                    }
                }
            }
        }

        stage('Push image') {
            steps {
                script {
                    // Push the image with two tags
                    docker.withRegistry('https://registry.hub.docker.com', 'docker-hub-credentials') {
                        docker.image(DOCKER_IMAGE_NAME).push("${env.BUILD_NUMBER}")
                        docker.image(DOCKER_IMAGE_NAME).push("latest")
                    }
                }
            }
        }
    }

    post {
        success {
            echo "Docker image build, test, and push successful!"
        }
        failure {
            echo "Build, test, or push failed. Check the Jenkins logs for details."
        }
    }
}
