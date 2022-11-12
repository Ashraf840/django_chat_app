pipeline{
    agent any
    stages{
        stage('Setup Redis')
        {
            steps{
                sh '''
                chmod +x redissetup.sh
                ./redissetup.sh
                '''
            }
        }
        stage('Setup Python Virtual ENV')
        {
            steps{
                sh '''
                chmod +x envsetup.sh
                ./envsetup.sh
                '''
            }
        }
        stage('uWSGI Setup')
        {
            steps{
                sh '''
                chmod +x uwsgi.sh
                ./uwsgi.sh
                '''
            }
        }
        stage('Daphne Setup')
        {
            steps{
                sh '''
                chmod +x daphne.sh
                ./daphne.sh
                '''
            }
        }
        stage('Static File Setup')
        {
            steps{
                sh '''
                chmod +x staticfile.sh
                ./staticfile.sh
                '''
            }
        }
        stage('NGINX Setup')
        {
            steps{
                sh '''
                chmod +x nginx.sh
                ./nginx.sh
                '''
            }
        }
    }
}