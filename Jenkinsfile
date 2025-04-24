pipeline{
    agent any

    environment {
        VENV_DIR = 'venv'
    }

    stages{
        stage('Cloning Github Repo to Jenkins'){
            steps{
                script{
                    echo 'Cloning Github Repo to Jenkins'
                    checkout scmGit(branches: [[name: '*/main']], extensions: [], userRemoteConfigs: [[credentialsId: 'github-token-hotel-project', url: 'https://github.com/Kabyik-Kayal/Hotel-Bookings-Cancellation-Predictor.git']])
                }
            }
        }
        stage('Creating Virtual Environment'){
            steps{
                script{
                    echo 'Creating Virtual Environment'
                    sh '''
                    python -m venv $VENV_DIR
                    . ${VENV_DIR}/bin/activate
                    pip install --upgrade pip
                    pip install -e .
                    '''
                }
            }
        }
    }
}