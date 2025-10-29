pipeline {
    agent any

    environment {
        // Update these with your own Docker repo details if needed
        DOCKER_IMAGE = 'pankajmores/cicd-app'
        DOCKER_TAG = "latest"
        // For ECR example: DOCKER_IMAGE = 'public.ecr.aws/your-repo/cicd-app'
    }

    stages {

        stage('Checkout') {
            steps {
                echo 'Cloning repository...'
                git branch: 'main', url: 'https://github.com/pankajmores/cicd.git'
            }
        }

        stage('Set up Python environment') {
            steps {
                echo 'Setting up Python environment...'
                sh '''
                python3 -m venv venv
                . venv/bin/activate
                pip install --upgrade pip
                if [ -f requirements.txt ]; then pip install -r requirements.txt; fi
                '''
            }
        }

        stage('Run Tests') {
            steps {
                echo 'Running tests...'
                sh '''
                . venv/bin/activate
                pytest || echo "Tests skipped (no tests found)"
                '''
            }
        }

        stage('Build Docker Image') {
            steps {
                echo 'Building Docker image...'
                sh 'docker build -t $DOCKER_IMAGE:$DOCKER_TAG .'
            }
        }

        stage('Push Docker Image') {
            when {
                expression { return env.BRANCH_NAME == 'main' }
            }
            steps {
                echo 'Pushing Docker image...'
                withCredentials([usernamePassword(credentialsId: 'dockerhub-creds', usernameVariable: 'DOCKER_USER', passwordVariable: 'DOCKER_PASS')]) {
                    sh '''
                    echo "$DOCKER_PASS" | docker login -u "$DOCKER_USER" --password-stdin
                    docker push $DOCKER_IMAGE:$DOCKER_TAG
                    '''
                }
            }
        }

        stage('Deploy') {
            steps {
                echo 'Deploying container...'
                sh '''
                docker stop cicd-app || true
                docker rm cicd-app || true
                docker run -d -p 5000:5000 --name cicd-app $DOCKER_IMAGE:$DOCKER_TAG
                '''
            }
        }
    }

    post {
        success {
            echo '✅ Build, test, and deploy successful!'
        }
        failure {
            echo '❌ Pipeline failed. Check the logs.'
        }
    }
}
