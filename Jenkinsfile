pipeline{
    agent any
    tools{
       jdk : "jdk21"
    }
    stages{
        stage("Docker Build"){
           steps{
             echo "This is Docker Build"
             sh "docker build -t devopsaditya123/clientapp:v1 ."
           }
        }

        stage("Docker push to Docker Hub"){
            echo "This time to push docker hub"
            withCreadentials([usernamePassword(creadentialsId: "docker-cred" , usernameVariable: "USER" , passwordVariable: "PASS")]){
                sh "echo $PASS | docker login -u $USER --password-stdin"
                sh "docker push devopsaditya123/v1"
            }

        }
    }
}