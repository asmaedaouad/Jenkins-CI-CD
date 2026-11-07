pipeline {
    agent any

    environment {
        VENV_DIR   = ".venv"
        HOST       = "0.0.0.0"
        PORT       = "5000"
        APP_MODULE = "app:app"
    }

    triggers {
        cron('H/5 * * * *')
        githubPush()
    }

    stages {

        stage('Checkout') {
            steps {
                git branch: 'main',
                    url: 'https://github.com/asmaedaouad/Jenkins-CI-CD.git',
                    credentialsId: 'github-token-user'
            }
        }

        stage('Setup Virtual Environment') {
            steps {
                sh '''
                    python3 -m venv ${VENV_DIR}
                    . ${VENV_DIR}/bin/activate
                    python --version
                    pip install --upgrade pip
                    pip install -r requirements.txt
                    pip install pytest-cov
                '''
            }
        }

        stage('Run Tests') {
            when {
                not {
                    changeset "README.md"
                }
            }
            parallel {
                stage('Test File 1') {
                    steps {
                        sh '''
                            . ${VENV_DIR}/bin/activate
                            COVERAGE_FILE=.coverage.1 python -m pytest test_app.py -v --cov=app --cov-report=term
                        '''
                    }
                }
                stage('Test File 2') {
                    steps {
                        sh '''
                            . ${VENV_DIR}/bin/activate
                            COVERAGE_FILE=.coverage.2 python -m pytest test_app_2.py -v --cov=app --cov-report=term
                        '''
                    }
                }
            }
        }

        stage('Deploy') {
            steps {
                echo 'Starting Flask app locally using Gunicorn...'
                sh '''#!/bin/bash
                    . ${VENV_DIR}/bin/activate

                    if [ -f gunicorn.pid ]; then
                        kill $(cat gunicorn.pid) 2>/dev/null || true
                        sleep 2
                    fi

                    JENKINS_NODE_COOKIE=dontKillMe nohup gunicorn --bind ${HOST}:${PORT} ${APP_MODULE} --pid gunicorn.pid > gunicorn.log 2>&1 &

                    sleep 3
                    echo "Gunicorn started on http://${HOST}:${PORT}"
                '''
            }
        }
    }

    post {
        success {
            echo "SUCCESS: ${env.JOB_NAME} #${env.BUILD_NUMBER}"
        }
        failure {
            echo "FAILURE: ${env.JOB_NAME} #${env.BUILD_NUMBER}"
        }
    }
}
