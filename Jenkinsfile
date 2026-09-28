pipeline {
    agent any

    stages {
        stage('Build Docker Image') {
            steps {
                sh 'docker build -t my-devops-website .'
            }
        }

        stage('Run Website') {
            steps {
                sh 'docker stop my-website || true'
                sh 'docker rm my-website || true'
                sh 'docker run -d -p 8081:80 --name my-website my-devops-website'
            }
        }
    }
}
