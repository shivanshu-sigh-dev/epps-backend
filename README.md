# Electronic Prescription Processing System (EPPS) - Backend

## Overview

The **Electronic Prescription Processing System (EPPS)** backend is responsible for managing the core functionality of the system, including handling prescription data, patient records, and prescription image storage. The backend provides a set of RESTful APIs to interact with the frontend, process prescription images, and store structured data for easy access and retrieval.

This backend is built using **Django**, a Python web framework, and integrates several services including **Azure OCR** for text extraction and **Azure OpenAI** for parsing the extracted information.

## Features

- **Prescription Image Upload**: Upload prescription images and process them using Azure OCR to extract handwritten text.
- **Patient Management**: Create, read, update, and delete (CRUD) patient records.
- **Prescription Management**: Store and manage prescriptions, linking them to patients and prescription images.
- **Drug Information Management**: Parse extracted text to identify drug names, dosages, frequencies, and more using Azore OpenAI LLM.
- **Prescription History**: Build and retrieve a patient's prescription history over time.

## Technology Stack

- **Django (Backend Framework)**: Provides the foundation for the backend, including API management and database handling.
- **SQLite (Development)** / **PostgreSQL (Production)**: Database for storing patient, prescription, and drug information.
- **Django REST Framework (DRF)**: For building RESTful APIs.
- **Azure OCR API**: For extracting text from prescription images.
- **Azure OpenAI LLM Model**: For recognizing and structuring medical entities such as drug names, dosages, and frequencies.

## Requirements

### Hardware

- **Processor**: Multi-core processor (e.g., Intel Core i5/i7 or AMD Ryzen 5/7).
- **Memory**: Minimum 8 GB RAM (16 GB recommended for optimal performance).
- **Storage**: At least 100 GB of free storage for development.
- **Internet Connection**: Required for accessing cloud services (Azure OCR, Azure OpenAI).

### Software

- **Operating System**: Ubuntu 20.04 LTS or higher for production; Windows/macOS for development.
- **Python 3.9+**
- **Django 3.x+**
- **SQLite** (default) or **PostgreSQL** (recommended for production)
- **Azure SDK** (for OCR integration and OpenAI Model)
