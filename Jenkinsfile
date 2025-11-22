pipeline {
    agent any

    environment {
        REPO_URL = 'https://github.com/saiganesh74/devops-flask-mysql.git'
        IMAGE_NAME = 'flask-app'
        DOCKER_HUB_IMAGE = 'saiganesh74/flask-app'
        CONTAINER_NAME = 'flask-app'
        EC2_USER = 'ubuntu'
        EC2_HOST = '13.60.174.168'
        PORT = '5000'
        BRANCH = 'main'
    }

    stages {
        stage('Clone Repo') {
            steps {
                git branch: BRANCH, url: REPO_URL
            }
        }

        stage("Build Docker Image") {
            steps {
                sh 'docker build -t ${IMAGE_NAME}:latest .'
            }
        }

        stage("Tag Docker Image") {
            steps {
                sh 'docker tag ${IMAGE_NAME}:latest ${DOCKER_HUB_IMAGE}:latest'
            }
        }

        stage("Push to Docker Hub") {
            steps {
                withCredentials([usernamePassword(
                        credentialsId: 'docker-hub-creds',
                        usernameVariable: 'DOCKER_USER',
                        passwordVariable: 'DOCKER_PASS'
                )]) {
                    sh "echo $DOCKER_PASS | docker login -u $DOCKER_USER --password-stdin"
                    sh "docker push ${DOCKER_HUB_IMAGE}:latest"
                }
            }
        }

        stage("Deploy to EC2") {
            steps {
                sshagent (credentials: ['ec2-ssh']) {
                    sh """
                        ssh -o StrictHostKeyChecking=no ${EC2_USER}@${EC2_HOST} '
                            docker pull ${DOCKER_HUB_IMAGE}:latest &&
                            docker stop ${CONTAINER_NAME} || true &&
                            docker rm ${CONTAINER_NAME} || true &&
                            docker run -d -p ${PORT}:${PORT} --name ${CONTAINER_NAME} ${DOCKER_HUB_IMAGE}:latest
                        '
                    """
                }
            }
        }
        stage("Run Tests") {
            steps {
                sh 'echo "Running tests…"'
            }
        }
    }

    post {
        success {
            echo "Build Success 🎉"
        }
        failure {
            echo "Build Failed ❌"
        }
    }
}
