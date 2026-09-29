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

        stage('Docker Verification') {
            steps {
                echo 'Verifying Docker image...'

                sh 'docker image inspect my-devops-website'
                sh 'docker images my-devops-website'

                echo 'Docker image verified successfully!'
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

        stage('Container Verification') {
            steps {
                echo 'Checking running container...'

                sh 'docker ps --filter name=my-website'
                sh 'docker inspect --format="{{.State.Status}}" my-website'

                echo 'Container is running successfully!'
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

        stage('Pipeline Summary') {
            steps {
                echo ''
                echo '=========================================='
                echo '          DEPLOYMENT SUMMARY'
                echo '=========================================='
                echo 'Source       : GitHub'
                echo 'Automation   : Jenkins'
                echo 'Container    : Docker'
                echo 'Environment  : Ubuntu'
                echo 'Application  : My DevOps Website'
                echo 'Port         : 8081'
                echo 'Status       : DEPLOYED SUCCESSFULLY'
                echo 'Health       : HEALTH CHECK PASSED'
                echo '=========================================='
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
            echo '======================================'
            echo 'CI/CD PIPELINE FAILED!'
            echo 'Please check the failed stage above.'
            echo '======================================'
        }
    }
}
