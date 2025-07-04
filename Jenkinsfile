pipeline{
    agent any 

    environment {
        VENV_DIR = 'venv'
        
    }


    stages {
        stage('Cloning Github repo to Jenkins') {
            steps {
                script{
                        echo 'Cloning Github repo to Jenkins............'
                        checkout scmGit(branches: [[name: '*/main']], extensions: [], userRemoteConfigs: [[credentialsId: 'github-token', url: 'https://github.com/JayRathod341997/mlops-project-1.git']])
                }
                
            }
        }

        stage('Install System Dependencies') {
            steps {
                script {
                    echo 'Installing python3-venv...'
                    sh '''
                    apt-get update
                    apt-get install -y python3-venv
                    '''
                }
            }
        }

        stage('Setting up our Virtual Environment and Installing dependencies') {
            steps{
                script{
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