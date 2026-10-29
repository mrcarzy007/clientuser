pipeline{
    agent any
    tools{
       jdk "jdk21"
    }
    stages{
        stage("Docker Build"){
           steps{
             echo "This is Docker Build"
             sh "docker build -t devopsaditya123/clientapp:v1 ."
           }
        }

        stage("Docker push"){
            steps {
                withCredentials([usernamePassword(credentialsId: "docker-cred" , usernameVariable: "USER" , passwordVariable: "PASS")]){
                sh "echo $PASS | docker login -u $USER --password-stdin"
                sh "docker push devopsaditya123/clientapp:v1"
            }

            }
        }
    }
}