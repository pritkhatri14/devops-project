pipeline {
    agent any

    stages {

        stage('Validate') {
            steps {
                echo 'Checking project files...'
                sh 'test -f index.html'
                sh 'test -f Dockerfile'
                sh 'test -f Jenkinsfile'
                echo 'Validation completed successfully!'
            }
        }

        stage('Test') {
            steps {
                echo 'Running website tests...'
                sh 'grep -q "DevOps" index.html'
                echo 'Website test passed!'
            }
        }

        stage('Build Docker Image') {
            steps {
                echo 'Building Docker image...'
                sh 'docker build -t my-devops-website .'
                echo 'Docker image built successfully!'
            }
        }

        stage('Deploy Development') {
            steps {
                echo 'Deploying Development environment on port 8081...'
                sh 'docker stop my-website || true'
                sh 'docker rm my-website || true'
                sh 'docker run -d -p 8081:80 --name my-website my-devops-website'
                echo 'Development environment deployed!'
            }
        }

        stage('Test Development') {
            steps {
                echo 'Testing Development environment...'
                sh 'sleep 3'
                sh 'curl -f http://localhost:8081'
                echo 'Development health check passed!'
            }
        }

        stage('Deploy Staging') {
            steps {
                echo 'Deploying Staging environment on port 8082...'
                sh 'docker stop my-website-staging || true'
                sh 'docker rm my-website-staging || true'
                sh 'docker run -d -p 8082:80 --name my-website-staging my-devops-website'
                echo 'Staging environment deployed!'
            }
        }

        stage('Test Staging') {
            steps {
                echo 'Testing Staging environment...'
                sh 'sleep 3'
                sh 'curl -f http://localhost:8082'
                echo 'Staging health check passed!'
            }
        }

        stage('Deploy Production') {
            steps {
                echo 'Deploying Production environment on port 8083...'
                sh 'docker stop my-website-production || true'
                sh 'docker rm my-website-production || true'
                sh 'docker run -d -p 8083:80 --name my-website-production my-devops-website'
                echo 'Production environment deployed!'
            }
        }

        stage('Test Production') {
            steps {
                echo 'Testing Production environment...'
                sh 'sleep 3'
                sh 'curl -f http://localhost:8083'
                echo 'Production health check passed!'
            }
        }
    }

    post {
        success {
            echo '=========================================='
            echo 'MULTI-ENVIRONMENT CI/CD COMPLETED!'
            echo 'Development : http://localhost:8081'
            echo 'Staging     : http://localhost:8082'
            echo 'Production  : http://localhost:8083'
            echo '=========================================='
        }

        failure {
            echo 'MULTI-ENVIRONMENT CI/CD PIPELINE FAILED!'
        }
    }
}
