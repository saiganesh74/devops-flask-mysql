pipeline {
    agent any 

    environment {
        REPO_URL = 'https://github.com/saiganesh74/devops-flask-mysql.git'
        IMAGE_NAME = 'flask-app'
        DOCKER_HUB_IMAGE = 'saiganesh74/flask-app'
        CONTAINER_NAME = 'flask-container'
        PORT = '5000'
        BRANCH = 'main'
    }

    stages {

        stage('Clone Repo') {
            steps {
                git branch: BRANCH, url: REPO_URL
            }
        }

        stage('Build Docker Image') {
            steps {
                sh 'docker build -t ${IMAGE_NAME}:latest .'
            }
        }

        stage('Tag Docker Image') {
            steps {
                sh 'docker tag ${IMAGE_NAME}:latest ${DOCKER_HUB_IMAGE}:latest'
            }
        }

        stage('Push to Docker Hub') {
            steps {
                withCredentials([
                    usernamePassword(
                        credentialsId: 'docker-hub-creds',
                        usernameVariable: 'DOCKER_USER',
                        passwordVariable: 'DOCKER_PASS'
                    )
                ]) {
                    sh """
                        echo "${DOCKER_PASS}" | docker login -u "${DOCKER_USER}" --password-stdin
                        docker push ${DOCKER_HUB_IMAGE}:latest
                    """
                }
            }
        }

        stage('Run Container') {
            steps {
                sh 'docker rm -f ${CONTAINER_NAME} || true'
                sh 'docker run -d -p ${PORT}:${PORT} --name ${CONTAINER_NAME} ${IMAGE_NAME}:latest'
            }
        }

        stage('Run Tests') {
            steps {
                sh 'echo "Running tests for Jenkins build"'
            }
        }
    }

    post {
        success {
            echo "Ayyyyy Build succeeded"
        }
        failure {
            echo "NAHHHHH build failed"
        }
        always {
            echo "Pipeline run is done"
        }
    }
}
