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
        
        stage('Install Python venv package') {
            steps {
                script {
                    echo 'Ensuring python3-venv is installed............'
                    sh '''
                    sudo apt-get update
                    sudo apt-get install -y python3-venv
                    '''
                }
            }
        }
        
        stage('Setting up Virtual Environment and Installing dependencies') {
            steps {
                script {
                    echo 'Setting up our Virtual Environment and Installing dependencies............'
                    sh '''
                    python3 -m venv ${VENV_DIR}
                    . ${VENV_DIR}/bin/activate
                    pip install --upgrade pip
                    pip install -e .
                    '''
                }
            }
        }
    }
}