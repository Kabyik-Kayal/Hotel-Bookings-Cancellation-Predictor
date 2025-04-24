pipeline{
    agent any

    environment {
        VENV_DIR = 'venv'
        GCP_PROJECT = "carbide-datum-457415-j1"
        GCLOUD_PATH = "/var/jenkins_home/google-cloud-sdk/bin"
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

        stage('Building and Pushing Docker Image to GCR'){
            steps{
                withCredentials([file(credentialsId : 'GCP-Hotel-Key', variable : 'GOOGLE_APPLICATION_CREDENTIALS')]){
                    script{
                        echo 'Building and Pushing Docker Image to Google Cloud'
                        sh '''
                        export PATH=$PATH:${GCLOUD_PATH}
                        gcloud auth activate-service-account --key-file=${GOOGLE_APPLICATION_CREDENTIALS}
                        gcloud config set project ${GCP_PROJECT}
                        gcloud auth configure-docker --quiet
                        docker build -t gcr.io/${GCP_PROJECT}/hotel-bookings-cancellation-predictor:latest .
                        docker push gcr.io/${GCP_PROJECT}/hotel-bookings-cancellation-predictor:latest
                        '''
                    }
                }
            }
        }
    }
}