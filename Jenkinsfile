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

                echo 'All required project files are present!'
            }
        }

        stage('Test') {
            steps {
                echo '======================================'
                echo 'RUNNING AUTOMATED WEBSITE TESTS'
                echo '======================================'

                echo 'Test 1: Checking HTML file...'
                sh 'test -s index.html'

                echo 'Test 2: Checking HTML structure...'
                sh 'grep -q "<html>" index.html'
                sh 'grep -q "</html>" index.html'

                echo 'Test 3: Checking website title...'
                sh 'grep -q "<title>" index.html'

                echo 'Test 4: Checking DevOps content...'
                sh 'grep -q "DevOps" index.html'

                echo 'Test 5: Checking website heading...'
                sh 'grep -q "<h1>" index.html'

                echo '======================================'
                echo 'ALL AUTOMATED TESTS PASSED!'
                echo '======================================'
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

                echo 'Staging environment deployed!'
            }
        }

        stage('Test Staging') {
            steps {
                echo '======================================'
                echo 'TESTING STAGING ENVIRONMENT'
                echo '======================================'

                sh 'sleep 3'
                sh 'curl -f http://localhost:8082'

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

                echo 'Production environment deployed!'
            }
        }

        stage('Test Production') {
            steps {
                echo '======================================'
                echo 'TESTING PRODUCTION ENVIRONMENT'
                echo '======================================'

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
