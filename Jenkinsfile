pipeline {
    agent any

    stages {

        stage('Validate') {
            steps {
                echo '======================================'
                echo 'VALIDATING PROJECT FILES'
                echo '======================================'

                sh 'test -f index.html'
                sh 'test -f Dockerfile'
                sh 'test -f Jenkinsfile'
                sh 'test -f staging.html'
                sh 'test -f production.html'

                echo 'All required project files are present!'
            }
        }

        stage('Test') {
            steps {
                echo '======================================'
                echo 'RUNNING AUTOMATED WEBSITE TESTS'
                echo '======================================'

                sh 'test -s index.html'
                sh 'grep -q "<html>" index.html'
                sh 'grep -q "</html>" index.html'
                sh 'grep -q "<title>" index.html'
                sh 'grep -q "DevOps" index.html'
                sh 'grep -q "<h1>" index.html'

                echo 'ALL AUTOMATED TESTS PASSED!'
            }
        }

        stage('Build Docker Image') {
            steps {
                echo '======================================'
                echo 'BUILDING DOCKER IMAGE'
                echo '======================================'

                sh 'docker build -t my-devops-website .'

                echo 'Docker image built successfully!'
            }
        }

        stage('Deploy Development') {
            steps {
                echo '======================================'
                echo 'DEPLOYING DEVELOPMENT ENVIRONMENT'
                echo 'Port: 8081'
                echo '======================================'

                sh 'docker stop my-website || true'
                sh 'docker rm my-website || true'

                sh 'docker run -d -p 8081:80 --name my-website my-devops-website'

                echo 'Development environment deployed!'
            }
        }

        stage('Test Development') {
            steps {
                echo '======================================'
                echo 'TESTING DEVELOPMENT ENVIRONMENT'
                echo '======================================'

                sh 'sleep 3'
                sh 'curl -f http://localhost:8081'

                echo 'Development health check passed!'
            }
        }

        stage('Deploy Staging') {
            steps {
                echo '======================================'
                echo 'DEPLOYING STAGING ENVIRONMENT'
                echo 'Port: 8082'
                echo '======================================'

                sh 'docker stop my-website-staging || true'
                sh 'docker rm my-website-staging || true'

                sh 'docker run -d -p 8082:80 --name my-website-staging my-devops-website'

                sh 'docker cp staging.html my-website-staging:/usr/share/nginx/html/index.html'

                echo 'Staging UI deployed!'
            }
        }

        stage('Test Staging') {
            steps {
                echo '======================================'
                echo 'TESTING STAGING ENVIRONMENT'
                echo '======================================'

                sh 'sleep 3'
                sh 'curl -f http://localhost:8082'
                sh 'curl -s http://localhost:8082 | grep -q "STAGING ENVIRONMENT"'

                echo 'Staging health check passed!'
            }
        }

        stage('Deploy Production') {
            steps {
                echo '======================================'
                echo 'DEPLOYING PRODUCTION ENVIRONMENT'
                echo 'Port: 8083'
                echo '======================================'

                sh 'docker stop my-website-production || true'
                sh 'docker rm my-website-production || true'

                sh 'docker run -d -p 8083:80 --name my-website-production my-devops-website'

                sh 'docker cp production.html my-website-production:/usr/share/nginx/html/index.html'

                echo 'Production UI deployed!'
            }
        }

        stage('Test Production') {
            steps {
                echo '======================================'
                echo 'TESTING PRODUCTION ENVIRONMENT'
                echo '======================================'

                sh 'sleep 3'
                sh 'curl -f http://localhost:8083'
                sh 'curl -s http://localhost:8083 | grep -q "PRODUCTION ENVIRONMENT"'

                echo 'Production health check passed!'
            }
        }
    }

    post {

        success {
            echo '=========================================='
            echo 'MULTI-ENVIRONMENT CI/CD COMPLETED!'
            echo '=========================================='
            echo 'Automated Tests: PASSED'
            echo 'Development: http://localhost:8081'
            echo 'Staging:     http://localhost:8082'
            echo 'Production:  http://localhost:8083'
            echo '=========================================='
        }

        failure {
            echo '=========================================='
            echo 'MULTI-ENVIRONMENT CI/CD PIPELINE FAILED!'
            echo '=========================================='
        }
    }
}
