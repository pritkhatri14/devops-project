pipeline {
    agent any

    stages {

        stage('Validate') {
            steps {
                echo '========== VALIDATING PROJECT FILES =========='

                sh 'test -s index.html'
                sh 'test -s staging.html'
                sh 'test -s production.html'

                sh 'test -f Dockerfile'
                sh 'test -f Dockerfile.staging'
                sh 'test -f Dockerfile.production'
                sh 'test -f Jenkinsfile'

                echo 'All required project files are present!'
            }
        }

        stage('Test Source Files') {
            steps {
                echo '========== TESTING WEBSITE SOURCE FILES =========='

                sh 'grep -qi "<html" index.html'
                sh 'grep -qi "</html>" index.html'
                sh 'grep -qi "DevOps" index.html'

                sh 'grep -qi "Staging Environment" staging.html'
                sh 'grep -qi "Production Environment" production.html'

                echo 'All source file tests passed!'
            }
        }

        stage('Build Development Image') {
            steps {
                echo '========== BUILDING DEVELOPMENT IMAGE =========='
                sh 'docker build -t my-devops-website .'
            }
        }

        stage('Build Staging Image') {
            steps {
                echo '========== BUILDING STAGING IMAGE =========='
                sh 'docker build -f Dockerfile.staging -t my-devops-staging .'
            }
        }

        stage('Build Production Image') {
            steps {
                echo '========== BUILDING PRODUCTION IMAGE =========='
                sh 'docker build -f Dockerfile.production -t my-devops-production .'
            }
        }

        stage('Deploy Development') {
            steps {
                echo '========== DEPLOYING DEVELOPMENT ON PORT 8082 =========='

                sh 'docker rm -f dev-website || true'
                sh 'docker run -d --name dev-website -p 8082:80 my-devops-website'
            }
        }

        stage('Test Development') {
            steps {
                echo '========== TESTING DEVELOPMENT =========='

                sh 'sleep 3'
                sh 'curl -fsS http://localhost:8082 | grep -qi "DevOps"'

                echo 'Development health check passed!'
            }
        }

        stage('Deploy Staging') {
            steps {
                echo '========== DEPLOYING STAGING ON PORT 8083 =========='

                sh 'docker rm -f staging-website || true'
                sh 'docker run -d --name staging-website -p 8083:80 my-devops-staging'
            }
        }

        stage('Test Staging') {
            steps {
                echo '========== TESTING STAGING =========='

                sh 'sleep 3'
                sh 'curl -fsS http://localhost:8083 | grep -qi "Staging Environment"'

                echo 'Staging health check passed!'
            }
        }

        stage('Deploy Production') {
            steps {
                echo '========== DEPLOYING PRODUCTION ON PORT 8085 =========='

                sh 'docker rm -f production-website || true'
                sh 'docker run -d --name production-website -p 8085:80 my-devops-production'
            }
        }

        stage('Test Production') {
            steps {
                echo '========== TESTING PRODUCTION =========='

                sh 'sleep 3'
                sh 'curl -fsS http://localhost:8085 | grep -qi "Production Environment"'

                echo 'Production health check passed!'
            }
        }
    }

    post {
        success {
            echo '=========================================='
            echo 'MULTI-ENVIRONMENT CI/CD COMPLETED!'
            echo 'All automated tests passed!'
            echo 'Development: http://localhost:8082'
            echo 'Staging:     http://localhost:8083'
            echo 'Production:  http://localhost:8085'
            echo 'Dashboard:   http://localhost:8084'
            echo '=========================================='
        }

        failure {
            echo '=========================================='
            echo 'MULTI-ENVIRONMENT CI/CD PIPELINE FAILED!'
            echo 'Check the stage logs for the error.'
            echo '=========================================='
        }
    }
}
