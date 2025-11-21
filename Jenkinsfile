pipeline{
    agent any 

    environment{
        REPO_URL = 'https://github.com/saiganesh74/devops-flask-mysql.git'
        BRANCH = 'main'
        IMAGE_NAME = 'flask-app'
        CONTAINER_NAME = 'flask-container'
        PORT = '5000'
    }
    stages{
        stage('Clone Repo'){
            steps{
                git branch: BRANCH , url : REPO_URL
            }
        }
        stage("Build Docker Image"){
            steps{
                sh 'docker build -t ${IMAGE_NAME}:latest .'
            }
        }
        stage("Running container"){
            steps{
                sh 'docker rm -f ${CONTAINER_NAME} || true'
                sh 'docker run -d -p ${PORT}:${PORT} --name ${CONTAINER_NAME} ${IMAGE_NAME}:latest'
            }
        }
        stage("Running tests"){
            steps{
                sh "echo "Running tests for Jenkins build " "
            }
        }
    }
}