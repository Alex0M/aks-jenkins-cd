node {
  def acr = 'devopscampdemo.azurecr.io'
  def appName = 'psrestapi'
  def imageName = "${acr}/${appName}"
  def umageTag = "${imageName}:${env.BRANCH_NAME}.${env.BUILD_NUMBER}"
  def appRepo = "devopscampdemo.azurecr.io/psrestapi:0.2.0"

  checkout scm
  
 stage('Build the Image and Push to Azure Container Registry') 
 {
   app = docker.build("${imageName}")
   withDockerRegistry([credentialsId: 'acr_auth', url: "https://${acr}"]) {
      app.push("${env.BRANCH_NAME}.${env.BUILD_NUMBER}")
                }
  }

 stage ("Deploy Application on Azure Kubernetes Service")
 {
  switch (env.BRANCH_NAME) {
    // Roll out to canary environment
    case "canary":
        // Change deployed image in canary to the one we just built
        sh("sed -i.bak 's#${appRepo}#${imageTag}@${DIGEST[2]}#' ./k8s/canary/*.yaml")
        sh("kubectl --namespace=sock-shop apply -f k8s/services/")
        sh("kubectl --namespace=sock-shop apply -f k8s/canary/")
        sh("echo http://`kubectl --namespace=sock-shop get service/${feSvcName} --output=json | jq -r '.status.loadBalancer.ingress[0].ip'` > ${feSvcName}")
        break

    // Roll out to production
    case "master":
        // Change deployed image in master to the one we just built
        sh("sed -i.bak 's#${appRepo}#${imageTag}#' ./k8s/production/*.yaml")
        sh("kubectl --namespace=psrestapi-production apply -f k8s/services/")
        sh("kubectl --namespace=psrestapi-production apply -f k8s/production/")
        sh("echo http://`kubectl --namespace=psrestapi-production get service/${appName} --output=json | jq -r '.status.loadBalancer.ingress[0].ip'` > ${appName}")
        break

    // Roll out a dev environment
    default:
        // Create namespace if it doesn't exist
        sh("kubectl get ns ${env.BRANCH_NAME} || kubectl create ns ${env.BRANCH_NAME}")
        // Don't use public load balancing for development branches
        sh("sed -i.bak 's#LoadBalancer#ClusterIP#' ./k8s/services/${feSvcName}.yaml")
        sh("sed -i.bak 's#${appRepo}#${imageTag}@${DIGEST[2]}#' ./k8s/dev/*.yaml")
        sh("kubectl --namespace=${env.BRANCH_NAME} apply -f k8s/services/")
        sh("kubectl --namespace=${env.BRANCH_NAME} apply -f k8s/dev/")
        echo 'To access your environment run `kubectl proxy`'
        echo "Then access your service via http://localhost:8001/api/v1/proxy/namespaces/${env.BRANCH_NAME}/services/${feSvcName}:80"     
    }
  }
}
