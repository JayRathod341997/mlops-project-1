pipeline {
    agent any

    environment {
        VENV_DIR = 'venv'
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
        stage('Run Application') {
            steps {
                sh """
                    . $VENV_DIR/bin/activate
                    python application.py  # Or your main script
                """
            }
        }
    }
}