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
        sshagent(['ubuntu']) {
            sh '''
                ssh -o StrictHostKeyChecking=no ubuntu@13.60.174.168 "
                    docker ps -q --filter 'publish=5000' | xargs -r docker stop &&
                    docker ps -aq --filter 'publish=5000' | xargs -r docker rm &&
                    docker pull saiganesh74/flask-app:latest &&
                    docker run -d -p 5000:5000 --name flask-app saiganesh74/flask-app:latest
                "
            '''
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
