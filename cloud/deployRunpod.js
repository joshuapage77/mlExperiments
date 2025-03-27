// deploy/deploy_runpod.js
import fs from 'fs'
import path from 'path'
import { execSync } from 'child_process'
import yaml from 'js-yaml'
import fetch from 'node-fetch'
import dotenv from 'dotenv'

dotenv.config()

const baseDir = path.resolve(path.dirname(new URL(import.meta.url).pathname))
const registryConfig = yaml.load(fs.readFileSync(path.join(baseDir, 'registry.yaml'), 'utf8'))
const runpodConfig = yaml.load(fs.readFileSync(path.join(baseDir, 'runpod.yaml'), 'utf8'))

const fullImage = `${registryConfig.url}/${registryConfig.namespace}/${registryConfig.image}:${registryConfig.tag}`

console.log(`\n🔧 Building image: ${fullImage}`)
execSync(`docker build -f Dockerfile.app.deploy -t ${fullImage} ..`, { stdio: 'inherit' })

console.log('\n🔐 Logging into registry...')
const password = process.env[registryConfig.password_env_var]
execSync(`echo ${password} | docker login ${registryConfig.url} -u ${registryConfig.username} --password-stdin`, { stdio: 'inherit' })

console.log('\n📤 Pushing image...')
execSync(`docker push ${fullImage}`, { stdio: 'inherit' })

console.log('\n🚀 Deploying to RunPod...')
const query = {
   query: `
    mutation DeployPod($input: PodFindAndDeployOnDemandInput!) {
      podFindAndDeployOnDemand(input: $input) {
        id
        name
        imageName
        status
      }
    }
  `,
   variables: {
      input: {
         cloudType: runpodConfig.cloudType,
         gpuTypeId: runpodConfig.gpuTypeId,
         imageName: fullImage,
         containerDiskInGb: runpodConfig.containerDiskInGb,
         volumeInGb: runpodConfig.volumeInGb,
         minNumGpus: runpodConfig.minNumGpus,
         maxNumGpus: runpodConfig.maxNumGpus,
         name: runpodConfig.name,
         dockerArgs: runpodConfig.dockerArgs
      }
   }
}

const response = await fetch('https://api.runpod.io/graphql', {
   method: 'POST',
   headers: {
      'Content-Type': 'application/json',
      'Authorization': `Bearer ${process.env.RUNPOD_API_KEY}`
   },
   body: JSON.stringify(query)
})

const result = await response.json()
console.log('\n📬 RunPod response:')
console.log(JSON.stringify(result, null, 2))
