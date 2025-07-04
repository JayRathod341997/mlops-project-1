# Hotel Booking Prediction MLOps Pipeline

[![Python Version](https://img.shields.io/badge/python-3.7%2B-blue)](https://www.python.org/)
[![License](https://img.shields.io/badge/license-MIT-green)](LICENSE)
[![Docker](https://img.shields.io/badge/Docker-Enabled-blue)](https://www.docker.com/)
[![Jenkins](https://img.shields.io/badge/Jenkins-CI/CD-orange)](https://www.jenkins.io/)

An end-to-end MLOps pipeline for predicting hotel booking cancellations, featuring:
- Automated model training and deployment
- Jenkins CI/CD integration
- Docker containerization
- Google Cloud integration

## Table of Contents
- [Project Overview](#project-overview)
- [Dataset Description](#dataset-description)
- [System Requirements](#system-requirements)
- [Setup Instructions](#setup-instructions)
  - [Docker Installation](#1-docker-installation)
  - [Jenkins Setup](#2-jenkins-setup)
  - [Project Setup](#3-project-setup)
  - [Google Cloud Integration](#4-google-cloud-integration)
- [Running the Pipeline](#running-the-pipeline)
- [Accessing Services](#accessing-services)
- [Project Structure](#project-structure)
- [Troubleshooting](#troubleshooting)
- [License](#license)

## Project Overview

This project implements a complete MLOps pipeline for predicting hotel booking cancellations using machine learning. The system includes:

- Data ingestion and preprocessing
- Model training and evaluation
- Flask-based prediction API
- Jenkins CI/CD pipeline
- Docker containerization
- Google Cloud integration

## Dataset Description

The dataset contains hotel booking information with the following columns:

| Column Name | Description |
|-------------|-------------|
| Booking_ID | Unique booking identifier |
| no_of_adults | Number of adults |
| no_of_children | Number of children |
| no_of_weekend_nights | Weekend nights stayed |
| no_of_week_nights | Week nights stayed |
| type_of_meal_plan | Meal plan type |
| required_car_parking_space | If parking required |
| room_type_reserved | Room type booked |
| lead_time | Days between booking and arrival |
| arrival_year/month/date | Arrival date components |
| market_segment_type | Booking channel |
| repeated_guest | Is guest repeated |
| no_of_previous_cancellations | Past cancellations |
| no_of_previous_bookings_not_canceled | Past successful bookings |
| avg_price_per_room | Average room price |
| no_of_special_requests | Special requests made |
| booking_status | Target variable (canceled/not canceled) |

## System Requirements

- Docker Desktop
- 4GB+ RAM
- Python 3.7+
- Google Cloud account (optional)

## Setup Instructions

### 1. Docker Installation

```bash
# Download and install Docker Desktop from:
# https://www.docker.com/products/docker-desktop
```
### 2. Jenkins Setup

```bash
mkdir custom_jenkins
cd custom_jenkins
docker build -t jenkins-dind .
docker run -d --name jenkins-dind \
  --privileged \
  -p 8080:8080 -p 50000:50000 \
  -v //var/run/docker.sock:/var/run/docker.sock \
  -v jenkins_home:/var/jenkins_home \
  jenkins-dind
```

### 3. Project Setup
```bash
docker build -t booking-predictor .
docker run -d -p 5000:5000 booking-predictor
```


