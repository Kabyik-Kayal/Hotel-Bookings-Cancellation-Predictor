# Hotel Booking Cancellation Predictor

## Overview

This project aims to predict whether a hotel booking will be canceled based on various features associated with the reservation. It includes a complete MLOps pipeline covering data ingestion, preprocessing, model training, evaluation, and deployment as a web application using Flask, Docker, Jenkins, and Google Cloud Platform (GCP).

The App is live on Google Cloud, you can access it [here](https://hotel-bookings-cancellation-predictor-529155836917.us-central1.run.app)


## Features

*   **Data Ingestion:** Fetches raw data from a Google Cloud Storage (GCS) bucket.
*   **Data Preprocessing:** Handles missing values, encodes categorical features, manages data imbalance using SMOTE, and performs feature selection.
*   **Model Training:** Trains a LightGBM (LGBM) classification model using Randomized Search for hyperparameter tuning.
*   **Model Evaluation:** Evaluates the model using metrics like Accuracy, Precision, Recall, and F1-score.
*   **MLflow Integration:** Tracks experiments, parameters, and metrics using MLflow.
*   **Web Application:** Provides a user-friendly interface built with Flask and HTML/CSS/JavaScript to input booking details and get cancellation predictions.
*   **API Endpoint:** Includes a `/api/predict` endpoint for programmatic predictions (currently basic).
*   **CI/CD Pipeline:** Automates the build, test, and deployment process using Jenkins, Docker, Google Container Registry (GCR), and Google Cloud Run.

## Tech Stack

| Category             | Technologies                                                     |
| :------------------- | :--------------------------------------------------------------- |
| **Core Language**    | Python 3.11                                                         |
| **Data Science**     | Pandas, NumPy, Scikit-learn, LightGBM, imbalanced-learn          |
| **Web & Deployment** | Flask, Docker, Google Cloud Platform (GCS, GCR, Cloud Run)       |
| **MLOps & Tools**    | MLflow, Jenkins, YAML                                      |

## Project Structure

```
.
├── artifacts/                # Stores outputs like processed data and trained models
│   ├── model/
│   ├── processed/
│   └── raw/
├── config/                   # Configuration files
│   ├── config.yaml           # Data processing and ingestion parameters
│   ├── model_params.py       # Model hyperparameters (if separate)
│   └── paths_config.py       # Path configurations
├── pipeline/                 # Scripts defining the ML pipeline stages
│   └── training_pipeline.py  # Orchestrates the training pipeline
├── src/                      # Source code for different modules
│   ├── __init__.py
│   ├── custom_exception.py   # Custom exception handling
│   ├── data_ingestion.py     # Data ingestion logic
│   ├── data_preprocessing.py # Data preprocessing logic
│   ├── logger.py             # Logging setup
│   └── model_training.py     # Model training and evaluation logic
├── static/                   # Static files for the web app (CSS)
│   └── style.css
├── templates/                # HTML templates for the Flask web app
│   └── index.html
├── utils/                    # Utility functions
│   ├── __init__.py
│   └── common_functions.py   # Common helper functions (e.g., read YAML)
├── .gitignore
├── app.py                    # Flask application entry point
├── Jenkinsfile               # Jenkins pipeline definition
├── Dockerfile                # Docker configuration
├── requirements.txt          # Python dependencies
├── setup.py                  # Project setup script
└── readme.md                 # Project documentation (this file)

```

## Setup and Installation (Local)

1.  **Clone the repository:**
    ```bash
    git clone https://github.com/Kabyik-Kayal/Hotel-Bookings-Cancellation-Predictor.git
    cd Hotel-Bookings-Cancellation-Predictor
    ```

2.  **Create and activate a virtual environment:**
    ```bash
    python -m venv venv
    source venv/bin/activate  # On Windows use `venv\Scripts\activate`
    ```

3.  **Install dependencies:**
    ```bash
    pip install --upgrade pip
    pip install -e . # Installs the project in editable mode
    ```

4.  **Configure GCP Credentials (if running locally with GCS):**
    *   Download your GCP service account key file.
    *   Set the environment variable:
        ```bash
        export GOOGLE_APPLICATION_CREDENTIALS="/path/to/your/keyfile.json"
        ```

## Usage

### 1. Running the Training Pipeline

This will execute the data ingestion, preprocessing, and model training steps. Artifacts (processed data, model file) will be saved in the `artifacts/` directory.

```bash
python pipeline/training_pipeline.py
```

### 2. Running the Web Application

This starts the Flask server, making the prediction interface available in your browser.

```bash
python app.py
```

Navigate to `http://127.0.0.1:8080` (or the host/port specified) in your web browser. Fill in the form with booking details and click "Predict Cancellation". The result will be shown in a modal popup.

## CI/CD Pipeline (Jenkins + Docker + GCP)

The `Jenkinsfile` defines an automated pipeline with the following stages:

1.  **Clone Github Repo:** Checks out the latest code from the main branch.
2.  **Create Virtual Environment:** Sets up a Python virtual environment and installs dependencies within the Jenkins workspace.
3.  **Build and Push Docker Image to GCR:**
    *   Builds a Docker image using the `Dockerfile`.
    *   Authenticates with Google Cloud.
    *   Pushes the built image to Google Container Registry (GCR).
4.  **Deploy to Google Cloud Run:**
    *   Authenticates with Google Cloud.
    *   Deploys the container image from GCR to Google Cloud Run, making the web application publicly accessible.

### Jenkins Setup Notes

These steps are for setting up Jenkins within a Docker container to run the pipeline.

1.  **Run Jenkins Docker-in-Docker Container:**
    ```bash
    # Ensure Docker is running on your host machine
    sudo docker run -d \
      --name jenkins-dind \
      --privileged \
      -p 8080:8080 -p 50000:50000 \
      -v /var/run/docker.sock:/var/run/docker.sock \
      -v jenkins_home:/var/jenkins_home \
      jenkins/jenkins:lts # Or a specific Jenkins image supporting Docker-in-Docker if needed
      # Note: The original used a custom 'jenkins-dind' image. Use an appropriate base image.
    ```
    *   `-v /var/run/docker.sock:/var/run/docker.sock`: Mounts the host's Docker socket to allow Jenkins to run Docker commands.
    *   `-v jenkins_home:/var/jenkins_home`: Persists Jenkins data.
    *   `--privileged`: Required for Docker-in-Docker (use with caution).

2.  **Get Initial Jenkins Admin Password:**
    ```bash
    sudo docker logs jenkins-dind
    ```
    Look for the password in the logs.

3.  **Access Jenkins:** Open `http://localhost:8080` in your browser and complete the setup using the password. Install suggested plugins.

4.  **Configure Jenkins Container (Install Python & Tools):**
    ```bash
    sudo docker exec -u root -it jenkins-dind bash

    # Inside the container:
    apt-get update && apt-get install -y python3 python3-pip python3-venv git curl gnupg
    ln -s /usr/bin/python3 /usr/bin/python # Create symlink if needed
    pip3 install --upgrade pip

    # Install Google Cloud SDK (Example - adjust if needed)
    echo "deb [signed-by=/usr/share/keyrings/cloud.google.gpg] https://packages.cloud.google.com/apt cloud-sdk main" | tee -a /etc/apt/sources.list.d/google-cloud-sdk.list
    curl https://packages.cloud.google.com/apt/doc/apt-key.gpg | apt-key --keyring /usr/share/keyrings/cloud.google.gpg add -
    apt-get update && apt-get install -y google-cloud-sdk

    exit
    ```

5.  **Restart Jenkins Container:**
    ```bash
    sudo docker restart jenkins-dind
    ```

6.  **Configure Jenkins Job:**
    *   Create a new Pipeline job in Jenkins.
    *   Configure it to use "Pipeline script from SCM".
    *   Set the SCM to Git and provide the repository URL.
    *   Specify the script path as `Jenkinsfile`.
    *   Add necessary credentials (GitHub token, GCP service account key file) in Jenkins Credentials Manager and reference them in the `Jenkinsfile`.
    * Build Now to run the pipeline and deploy the app. 

## Web Application Interface

The web application (`index.html`) provides a form to input the following features:

*   Lead Time (Days)
*   No. of Special Requests
*   Avg. Price Per Room
*   Arrival Month
*   Arrival Date
*   Market Segment Type
*   No. of Week Nights
*   No. of Weekend Nights
*   Type of Meal Plan
*   Room Type Reserved

Upon submission, the Flask backend processes the input, uses the trained model (`lgbm_model.pkl`) to predict the cancellation probability (0 for likely cancellation, 1 for likely confirmation), and displays the result.
_________________________________________________________

This project is licensed under the MIT License - see the [LICENSE](License) file for details.