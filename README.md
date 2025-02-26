# ML API Microservices

This project demonstrates a microservices approach to machine learning API deployment. It separates concerns between API handling, model serving, and data storage for a more scalable and maintainable architecture.

## Architecture Components

- **API Service**: FastAPI-based backend that handles HTTP requests ([ml_api](ml_api))
- **Model Service**: Dedicated container for machine learning models and inference ([model_service](model_service))
- **Redis**: Message broker for inter-service communication
- **PostgreSQL**: Database for storing prediction history

## Getting Started

### Prerequisites
- Docker and Docker Compose
- Git

### Setup and Deployment

1. Create the shared Docker network:
```
docker network create shared_network
```

2. Start all services:
```
docker compose up
```

For Mac M1 users, the project includes a specialized Dockerfile (`Dockerfile.M1`) that ensures compatibility with ARM architecture.

## API Endpoints

- **[GET] /**: Hello world of the API
- **[POST] /predict**: Submit data for model prediction
  - Expects a JSON object containing a sample as described in [ml_api/routes/model_routes.py](ml_api/routes/model_routes.py)
  - Returns the prediction result from the model
- **[GET] /predictions**: Retrieve historical predictions stored in the database

## Web Interface

A user-friendly web interface is available at `http://localhost:9090` for submitting prediction requests through a form.

## API Documentation

FastAPI automatically generates comprehensive API documentation:
- Swagger UI: `http://localhost:8000/docs`

## Architecture Details

The project implements a message queue pattern:
1. API service receives prediction requests
2. Requests are serialized and sent to Redis
3. Model service processes requests and returns predictions
4. Results are stored in PostgreSQL for future reference

This design allows for independent scaling of the API and model components as needed.

## Development

### Testing

Each service includes its own test suite that can be run individually:
```
# For API service
docker build -t api_test --target test ./api

# For Model service
docker build -t model_test --target test ./model
```



