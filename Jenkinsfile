pipeline {
    agent any

    stages {

        stage('Validate') {
            steps {
                echo 'Checking project files...'

                sh 'test -f index.html'
                sh 'test -f Dockerfile'
                sh 'test -f Jenkinsfile'
                sh 'test -f test-results/test-report.xml'

                echo 'Validation completed successfully!'
            }
        }

        stage('Test') {
            steps {
                echo 'Running website tests...'

                sh 'test -f index.html'
                sh 'test -f Dockerfile'
                sh 'test -f Jenkinsfile'
                sh 'grep -q "DevOps" index.html'

                echo 'All website tests passed!'
            }

            post {
                always {
                    junit 'test-results/test-report.xml'
                }
            }
        }

        stage('Build Docker Image') {
            steps {
                echo 'Building Docker image...'

                sh 'docker build -t my-devops-website .'

                echo 'Docker image built successfully!'
            }
        }

        stage('Deploy') {
            steps {
                echo 'Deploying website container...'

                sh 'docker stop my-website || true'
                sh 'docker rm my-website || true'

                sh 'docker run -d -p 8081:80 --name my-website my-devops-website'

                echo 'Website deployed successfully!'
            }
        }

        stage('Health Check') {
            steps {
                echo 'Checking website health...'

                sh 'sleep 3'
                sh 'curl -f http://localhost:8081'

                echo 'Health check passed!'
            }
        }
    }

    post {
        success {
            echo '======================================'
            echo 'CI/CD PIPELINE COMPLETED SUCCESSFULLY!'
            echo 'Website: http://localhost:8081'
            echo '======================================'
        }

        failure {
            echo 'CI/CD PIPELINE FAILED!'
        }
    }
}
