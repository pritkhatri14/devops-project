pipeline {
    agent any

    options {
        timestamps()
    }

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
                echo 'All required files are present.'
            }
        }

        stage('Test Source Files') {
            steps {
                echo '========== TESTING SOURCE FILES =========='
                sh 'grep -qi "<html" index.html'
                sh 'grep -qi "</html>" index.html'
                sh 'grep -qi "DevOps" index.html'
                sh 'grep -qi "Staging Environment" staging.html'
                sh 'grep -qi "Production Environment" production.html'
                echo 'All source-file tests passed.'
            }
        }

        stage('Build Development Image') {
            steps {
                echo '========== BUILDING DEVELOPMENT IMAGE =========='
                sh 'docker build -t my-devops-website -f Dockerfile .'
            }
        }

        stage('Build Staging Image') {
            steps {
                echo '========== BUILDING STAGING IMAGE =========='
                sh 'docker build -t my-devops-staging -f Dockerfile.staging .'
            }
        }

        stage('Build Production Image') {
            steps {
                echo '========== BUILDING PRODUCTION IMAGE =========='
                sh 'docker build -t my-devops-production -f Dockerfile.production .'
            }
        }

        stage('Deploy Development') {
            steps {
                echo '========== DEPLOYING DEVELOPMENT ON PORT 8081 =========='

                // Remove only known website containers that could conflict.
                sh 'docker rm -f my-website dev-website 2>/dev/null || true'

                sh 'docker run -d --restart unless-stopped --name dev-website -p 8081:80 my-devops-website'

                echo 'Development deployment started.'
            }
        }

        stage('Test Development') {
            steps {
                echo '========== TESTING DEVELOPMENT =========='
                sh 'sleep 3'
                sh 'curl -fsS http://localhost:8081/ -o /tmp/dev-test.html'
                sh 'grep -qi "DevOps" /tmp/dev-test.html'
                echo 'Development health check passed.'
            }
        }

        stage('Deploy Staging') {
            steps {
                echo '========== DEPLOYING STAGING ON PORT 8082 =========='

                // Release port 8082 from the previous website containers.
                sh 'docker rm -f my-website-staging staging-website 2>/dev/null || true'

                sh 'docker run -d --restart unless-stopped --name staging-website -p 8082:80 my-devops-staging'

                echo 'Staging deployment started.'
            }
        }

        stage('Test Staging') {
            steps {
                echo '========== TESTING STAGING =========='
                sh 'sleep 3'
                sh 'curl -fsS http://localhost:8082/ -o /tmp/staging-test.html'
                sh 'grep -qi "Staging Environment" /tmp/staging-test.html'
                echo 'Staging health check passed.'
            }
        }

        stage('Deploy Production') {
            steps {
                echo '========== DEPLOYING PRODUCTION ON PORT 8083 =========='

                // Release port 8083 and the old production port 8085.
                // Do not touch the dashboard on port 8084.
                sh 'docker rm -f my-website-production production-website 2>/dev/null || true'

                sh 'docker run -d --restart unless-stopped --name production-website -p 8083:80 my-devops-production'

                echo 'Production deployment started.'
            }
        }

        stage('Test Production') {
            steps {
                echo '========== TESTING PRODUCTION =========='
                sh 'sleep 3'
                sh 'curl -fsS http://localhost:8083/ -o /tmp/production-test.html'
                sh 'grep -qi "Production Environment" /tmp/production-test.html'
                echo 'Production health check passed.'
            }
        }
    }

    post {
        success {
            echo '''
            ==========================================
            MULTI-ENVIRONMENT CI/CD PIPELINE SUCCESS!
            ==========================================
            Development: http://localhost:8081
            Staging:     http://localhost:8082
            Production:  http://localhost:8083
            Dashboard:   http://localhost:8084
            Error Center will use port 8085.
            Troubleshooting will use port 8086.
            Deployment History will use port 8087.
            Project Summary will use port 8090.
            ==========================================
            '''
        }

        failure {
            echo '''
            ==========================================
            CI/CD PIPELINE FAILED
            Check the Console Output for the failed stage.
            ==========================================
            '''
        }
    }
}
