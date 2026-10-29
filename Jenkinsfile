pipeline{
    agent any
    tools{
       jdk "jdk21"
    }
     environment {
        DOCKER_HUB_USER = "devopsaditya123"
        IMAGE_NAME = "${DOCKER_HUB_USER}/clientapp"
        IMAGE_TAG = "${env.GIT_COMMIT.take(8)}"
        SONAR_PROJECT_KEY = "clientapp"
     }
    stages{
        stage("Sonar Qube Scanner"){
            steps{
              script{
                def scannerHome = tool "SonarQube Scanner"
                withSonarQubeEnv("SonarQube"){
                    sh """
                   ${scannerHome}/bin/sonar-scanner \
                            -Dsonar.projectKey=${SONAR_PROJECT_KEY} \
                            -Dsonar.sources=. \
                            -Dsonar.projectName=clientapp
                        """
                }
              }
            }
        }
        stage("Quilty Gate"){
            steps {
                echo "Waiting for SonarQube Quilty check"
                timeout(time: 5 , unit: "MINUTES"){
                    waitForQualityGate abortPipeline : true
                }
            }
        }
        stage("Docker Build"){
           steps{
               echo "Building image: ${IMAGE_NAME}:${IMAGE_TAG}"
                sh "docker build -t ${IMAGE_NAME}:${IMAGE_TAG} ."
           }
        }

        stage("Docker push"){
            steps {
                withCredentials([usernamePassword(credentialsId: "docker-cred" , usernameVariable: "USER" , passwordVariable: "PASS")]){
                sh "echo $PASS | docker login -u $USER --password-stdin"
                sh "docker push ${IMAGE_NAME}:${IMAGE_TAG}"
            }

            }
        }
    }
}