pipeline {
    agent any

    environment {
        VENV_DIR = 'venv'
        GCP_PROJECT = "mlops-project-1-464610"
        GCLOUD_PATH = "/var/jenkins_home/google-cloud-sdk/bin"
    }

    stages {
        stage('Cloning Github repo to Jenkins') {
            steps {
                script {
                    echo 'Cloning Github repo to Jenkins............'
                    checkout scmGit(branches: [[name: '*/main']], extensions: [], userRemoteConfigs: [[credentialsId: 'github-token', url: 'https://github.com/JayRathod341997/mlops-project-1.git']])
                }
            }
        }
        stage('Setup Virtual Environment') {
            steps {
                sh """
                    # Create venv (force re-create if broken)
                    python3 -m venv $VENV_DIR || rm -rf $VENV_DIR && python3 -m venv $VENV_DIR
                    # Activate and install dependencies
                    . $VENV_DIR/bin/activate
                    pip install --upgrade pip
                    pip install -e .
                """
            }
        }

        stage('Building and Pushing Docker Image to GCR') {
                steps {
                    withCredentials([file(credentialsId: 'gcp-key', variable: 'GOOGLE_APPLICATION_CREDENTIALS')]) {
                        script {
                            echo 'Building and Pushing Docker Image to GCR.............'
                            sh """
                                # Ensure gcloud is in PATH (if not already set globally)
                                export PATH=$PATH:${GCLOUD_PATH}

                                # Authenticate with GCP
                                gcloud auth activate-service-account --key-file=${GOOGLE_APPLICATION_CREDENTIALS}

                                # Set the GCP project
                                gcloud config set project ${GCP_PROJECT}

                                # Configure Docker to use GCR
                                gcloud auth configure-docker gcr.io --quiet

                                # Build the Docker image
                                docker build -t gcr.io/${GCP_PROJECT}/ml-project:latest .

                                # Push the Docker image to GCR
                                docker push gcr.io/${GCP_PROJECT}/ml-project:latest
                            """
                        }
                    }
                }
            }
        
    }
   
}