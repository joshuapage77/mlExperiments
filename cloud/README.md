# RunPod Deployment for Experiments
This folder contains scripts and configurations to package and deploy self-contained ML training experiments to [RunPod.io](https://runpod.io), using a private container registry and the RunPod GraphQL API.

---
## Why JavaScript?
We chose Node.js (JavaScript) over Python or Bash for the deployment tooling because:
- ✅ No virtual environments or dependency sprawl (unlike Python)
- ✅ Cross-platform support (Windows, macOS, Linux)
- ✅ Simple YAML/HTTP parsing and child process handling
- ✅ Easily versioned, minimal setup (`npm install`)
---

## Setup
1. Install Node dependencies:
   ```bash
   cd deploy
   npm install
   ```
2. Create a `.env` file by copying the sample and updating values:
   ```bash
   cp .env.SAMPLE .env
   ```
3. Review and adjust:
   - `registry.yaml` → Docker image name and registry settings
   - `runpod.yaml` → RunPod-specific GPU, disk, and deployment config
   - `Dockerfile.app.deploy` → Produces a standalone experiment container
## 🚀 Deploy
Builds the image, pushes to registry, and deploys to RunPod:
```bash
npm run runpod
```
You’ll get a live deployment in seconds. The training script logs will be visible in the RunPod UI.

## 🧱 File Structure
```
deploy/
├── deploy_runpod.js         # Deployment script (Node.js)
├── Dockerfile.app.deploy    # Build standalone training container
├── registry.yaml            # Registry info (shared)
├── runpod.yaml              # RunPod-specific config
├── .env.SAMPLE              # Environment variable template
├── .env                     # Actual credentials (gitignored)
└── package.json             # Node config + scripts
```