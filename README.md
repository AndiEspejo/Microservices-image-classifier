# NYC Taxi Prediction Microservices

This project implements a machine learning solution for predicting taxi fares and trip durations in New York City. It follows a microservices architecture with the following components:

- **API Service**: FastAPI-based backend that handles HTTP requests and serves predictions
- **ML Service**: Dedicated container for machine learning models and inference
- **Redis**: Message broker for inter-service communication
- **PostgreSQL**: Database for storing prediction history and analytics

## Getting Started

### Prerequisites

- Docker and Docker Compose
- Git

### Setup and Deployment

1. Create the shared Docker network:

```bash
docker network create shared_network
```

2. Start all services:

```bash
docker-compose up --build
```

For Mac M1 users, the project includes a specialized Dockerfile (`Dockerfile.M1`) that ensures compatibility with ARM architecture.

## API Endpoints

- **[GET] /**: Health check endpoint
- **[POST] /predict**: Submit trip details for fare and duration prediction
  - Expects a JSON object with pickup/dropoff locations, trip distance, etc.
  - Returns fare and duration predictions with confidence intervals
- **[GET] /predictions**: Retrieve historical predictions
  - Supports filtering and pagination

## Web Interface

A user-friendly web interface is available at `http://localhost:9090` for submitting prediction requests through a form.

## API Documentation

FastAPI automatically generates comprehensive API documentation:

- Swagger UI: `http://localhost:8000/docs`
- ReDoc: `http://localhost:8000/redoc`

## Architecture Details

The project uses a message queue architecture:

1. API service receives prediction requests
2. Requests are serialized and sent to Redis
3. ML service processes requests and returns predictions
4. Results are stored in PostgreSQL for future reference

## Development

### Testing

Each service includes its own test suite that can be run with:

```bash
# For API service
docker build -t api_test --target test ./api

# For ML service
docker build -t model_test --target test ./model
```

### Extending the Project

New features can be added by:

1. Updating model training in the ML service
2. Extending API endpoints in the FastAPI service
3. Enhancing the web interface for additional functionality

## License

This project is licensed under the MIT License.
