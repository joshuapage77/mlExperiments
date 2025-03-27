# MLOps Platform for experimentation

## Project Goals

- Create a platform that can be used to run training experiments and track results
- Support multiple training frameworks
- Build a portable, shareable, and extensible ML training pipeline
- Support pushing training to cloud compute providers

---

## ⚙️ Local System Requirements

This project **requires GPU support** for the default Docker setup.

| Component                     | Required | Notes                                                                 |
|------------------------------|----------|-----------------------------------------------------------------------|
| [Docker](https://docs.docker.com/get-docker/)                    | ✅       | Ensure recent version (20.10+)                                        |
| [Docker Compose](https://docs.docker.com/compose/install/)       | ✅       | Compose V2 is recommended (integrated into Docker CLI)                |
| [NVIDIA GPU + Drivers]        | ✅       | Required for training via CUDA                                        |
| [NVIDIA Container Toolkit](https://docs.nvidia.com/datacenter/cloud-native/container-toolkit/install-guide.html) | ✅       | Required to expose GPU to Docker                                      |

## GPU Setup for Docker (Required)

This project requires a GPU and uses the NVIDIA Container Toolkit.

### 1. Install NVIDIA Container Toolkit

Follow the official guide:  
https://docs.nvidia.com/datacenter/cloud-native/container-toolkit/install-guide.html

For Ubuntu:

```bash
sudo apt install -y nvidia-container-toolkit
sudo nvidia-ctk runtime configure --runtime=docker
sudo systemctl restart docker
```

### 2. Test your setup
```bash
docker run --rm --gpus all nvidia/cuda:11.8.0-base-ubuntu22.04 nvidia-smi
```

You should see your GPU listed. If that fails, the project won’t run.

---
## Configuration
This platform supports multiple, isolated projects under the `projects` folder. A toy project called pt_handwritten_classifier to understand the setup and test your install.
### Docker
`docker/.env` has a setting for ACTIVE_PROJECT that is used during image builds, container starts and platform scripts.
### Projects
* Each project folder should be created under `projects`
* Individual projects could have their own repos
* folder config holds base configurations and sweep configurations
#### config.yaml
If multiple models are used, each should be defined under `models` under a reference key (`default` in the toy project)
* name - name for the model once registered
* class_path - dot path to model Class

`train` - configurations here define a single training
* Any of these parameters can be overriden by the sweep config
* `model` should hold the key for the model to be trained
* This allows multiple models to be trained and compared with sweep config
#### sweep.yaml
The sweep config defines the search space and strategy for your hyperparameter sweep — like what values to try for learning rate, batch size, epochs, etc., and how to explore them (e.g., Optuna with TPE).
* `n_trials` - controls maximum number of trials
* `params` - parameters to include in sweep. Anything not included will use values defined in config.yaml

## Running the Project (Containers)
### Build the containers
Dockerfile.project is used for executing experiments, but needs to be manually built:
* The first time
* When requirements.txt changes
* Any time you change the active project

The image for mlflow will build the first time the project is brought up
```bash
docker $ docker compose build project
```

### Start the services
```bash
docker $ docker compose up -d
```
This will start:
- `mlflow` – MLflow Tracking Server (http://localhost:5000)
- `minio` – local S3-compatible storage for MLflow artifacts

### Train a model
To train a model using the settings in config.yaml, use the `train.sh` script in the `scripts` folder
```
scripts $ ./train.sh
```
### Train a model - sweep hyperparameters
To train a model using the sweep configuration in sweep.yaml, use the multirun flag `-m`
```
scripts $ ./train.sh -m
```

### View the MLflow UI
Open your browser:
```
http://localhost:5000
```

You’ll see runs, parameters, metrics, and saved models.

### View Minio Object Sore
```
http://localhost:9001
```

---

## 🧊 Data Versioning (Coming Soon)

DVC will be configured to track:
- Raw EMNIST data
- Preprocessed training/test splits
- Optional remote backend using MinIO

---


## 📄 License

MIT License — use freely, contribute if you'd like!