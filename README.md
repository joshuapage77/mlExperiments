# Handwritten Letter Classifier (PyTorch + MLOps)

This project is a modular, production-style machine learning pipeline for classifying handwritten letters using the EMNIST dataset and **PyTorch**. It's designed as a learning and demonstration project for:

- PyTorch model training and evaluation
- MLflow for experiment and model tracking
- DVC for data versioning
- Docker for reproducible environments
- GPU acceleration with NVIDIA runtime
- Clean CI/CD with GitHub Actions + `ruff` + `pytest`

---

## 🚀 Project Goals

- Learn and compare deep learning workflows in PyTorch and (later) TensorFlow
- Practice real-world MLOps structure using modern tools
- Build a portable, shareable, and extensible ML training pipeline

---

## ⚙️ Local System Requirements

This project **requires GPU support** for the default Docker setup.

| Component                     | Required | Notes                                                                 |
|------------------------------|----------|-----------------------------------------------------------------------|
| [Docker](https://docs.docker.com/get-docker/)                    | ✅       | Ensure recent version (20.10+)                                        |
| [Docker Compose](https://docs.docker.com/compose/install/)       | ✅       | Compose V2 is recommended (integrated into Docker CLI)                |
| [NVIDIA GPU + Drivers]        | ✅       | Required for training via CUDA                                        |
| [NVIDIA Container Toolkit](https://docs.nvidia.com/datacenter/cloud-native/container-toolkit/install-guide.html) | ✅       | Required to expose GPU to Docker                                      |

## 🧠 GPU Setup for Docker (Required)

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

## 🐳 Running the Project
### Build the containers

```bash
docker compose build
```

### Start the services

```bash
docker compose up -d
```

This will start:
- `app` – the training container (will run `train.py`)
- `mlflow` – MLflow Tracking Server (http://localhost:5000)
- `minio` – local S3-compatible storage for MLflow artifacts

### View the MLflow UI

Open your browser:
```
http://localhost:5000
```

You’ll see runs, parameters, metrics, and (eventually) saved models.

---

## 🧪 CI / Automation

This project includes:
- GitHub Actions for testing + linting
- Linter: [`ruff`](https://docs.astral.sh/ruff/)
- Unit tests via [`pytest`](https://docs.pytest.org/)

---

## 🧊 Data Versioning (Coming Soon)

DVC will be configured to track:
- Raw EMNIST data
- Preprocessed training/test splits
- Optional remote backend using MinIO

---


## 📄 License

MIT License — use freely, contribute if you'd like!