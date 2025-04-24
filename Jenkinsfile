pipeline{
    agent any

    stages{
        stage('Cloning Github Repo to Jenkins'){
            steps{
                script{
                    echo 'Cloning Github Repo to Jenkins'
                    checkout scmGit(branches: [[name: '*/main']], extensions: [], userRemoteConfigs: [[credentialsId: 'github-token-hotel-project', url: 'https://github.com/Kabyik-Kayal/Hotel-Bookings-Cancellation-Predictor.git']])
                }
            }
        }
    }
}