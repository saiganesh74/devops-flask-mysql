pipeline {
    agent any
    environment {
        REPO_URL = 'https://github.com/saiganesh74/devops-flask-mysql.git'
        IMAGE_NAME = 'flask-app'
        DOCKER_HUB_IMAGE = 'saiganesh74/flask-app'
        CONTAINER_NAME = 'flask-app'
        EC2_USER = 'ubuntu'
        EC2_HOST = '43.204.108.234'
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
                sshagent(['ec2-ssh']) {
                    sh '''
                        ssh -o StrictHostKeyChecking=no ubuntu@${EC2_HOST}
                        docker stop flask-app || true &&
                        docker rm flask-app || true &&
                        docker pull {DOCKER_HUB_IMAGE}:latest &&
                        docker run -d -p 5000:5000 --name flask-app saiganesh74/flask-app:latest
                "
            '''
        }
    }
}
        stage("Run Tests") {
            steps {
                sh 'pytest -q --disable-warnings --maxfail=1'
            }
        }
    }
    post {
        success {
            echo "Build Success"
        }
        failure {
            echo "Build Failed"
        }
    }
}
