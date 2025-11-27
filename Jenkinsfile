pipeline {
    agent any

    environment {
        LABS = credentials('labcred')

        // EC2 Java setup
        JAVA_HOME = '/usr/lib/jvm/java-21-openjdk'
        PATH = "${env.JAVA_HOME}/bin:/usr/bin:/bin:${env.PATH}"

        VENV = 'retail_pipeline_venv'
    }

    stages {

        stage('Setup Virtual Environment') {
            steps {
                sh '''
                    # Remove only old venv if exists
                    if [ -d "${VENV}" ]; then
                        rm -rf ${VENV}
                    fi

                    python3 -m venv ${VENV}
                    ./${VENV}/bin/pip install --upgrade pip
                    ./${VENV}/bin/pip install pipenv
                '''
            }
        }

        stage('Install Dependencies') {
            steps {
                sh './${VENV}/bin/pipenv install --dev'
            }
        }

        stage('Test') {
            steps {
                sh '''
                    echo "JAVA_HOME=$JAVA_HOME"
                    echo "PATH=$PATH"
                    ./${VENV}/bin/pipenv run pytest
                '''
            }
        }

        stage('Package') {
            steps {
                sh '''
                    zip -r retailproject.zip . \
                    -x "${VENV}/*" \
                    -x ".git/*"

                '''
            }
        }

        stage('Deploy') {
            steps {
                sh '''
                    sshpass -p "$LABS_PSW" scp -o StrictHostKeyChecking=no \
                    retailproject.zip $LABS_USR@g01.itversity.com:/home/itv022735/retailproject
                '''
            }
        }
    }
}