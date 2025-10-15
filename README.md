# Airflow Local Development Environment

[![Apache Airflow](https://img.shields.io/badge/Apache%20Airflow-2.3.4-017CEE?style=flat-square&logo=Apache%20Airflow&logoColor=white)](https://airflow.apache.org/)
[![Docker](https://img.shields.io/badge/Docker-Compose-2496ED?style=flat-square&logo=docker&logoColor=white)](https://www.docker.com/)
[![Python](https://img.shields.io/badge/Python-3.7+-3776AB?style=flat-square&logo=python&logoColor=white)](https://www.python.org/)
[![License](https://img.shields.io/badge/License-Apache%202.0-blue.svg?style=flat-square)](LICENSE)
[![PostgreSQL](https://img.shields.io/badge/PostgreSQL-13-336791?style=flat-square&logo=postgresql&logoColor=white)](https://www.postgresql.org/)
[![Redis](https://img.shields.io/badge/Redis-Latest-DC382D?style=flat-square&logo=redis&logoColor=white)](https://redis.io/)

![GitHub stars](https://img.shields.io/github/stars/mbreault/airflow-local?style=flat-square)
![GitHub forks](https://img.shields.io/github/forks/mbreault/airflow-local?style=flat-square)
![GitHub issues](https://img.shields.io/github/issues/mbreault/airflow-local?style=flat-square)
![GitHub last commit](https://img.shields.io/github/last-commit/mbreault/airflow-local?style=flat-square)
[![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg?style=flat-square)](https://github.com/psf/black)
![Maintenance](https://img.shields.io/badge/Maintained%3F-yes-green.svg?style=flat-square)

A local Apache Airflow development environment using Docker Compose with CeleryExecutor, PostgreSQL, and Redis. This setup includes example DAGs and is configured for easy local development and testing.

## Features

- **Apache Airflow 2.3.4** with CeleryExecutor
- **Docker Compose** setup for easy local development
- **PostgreSQL 13** as metadata database
- **Redis** as message broker
- **Microsoft SQL Server** provider integration
- **Azure Application Insights** logging support
- **Kubernetes/Helm** configuration files for production deployment
- Example DAGs included for quick start

## Prerequisites

- Docker and Docker Compose installed
- Python 3.7+ (for standalone mode)
- At least 4GB RAM available for Docker
- At least 10GB free disk space

## Quick Start

### Using Docker Compose (Recommended)

1. **Clone the repository**
   ```bash
   git clone https://github.com/mbreault/airflow-local.git
   cd airflow-local
   ```

2. **Set environment variables** (optional)
   
   Create a `.env` file in the root directory:
   ```bash
   AIRFLOW_UID=50000
   _AIRFLOW_WWW_USER_USERNAME=airflow
   _AIRFLOW_WWW_USER_PASSWORD=airflow
   ```

3. **Start Airflow**
   ```bash
   docker-compose up -d
   ```

4. **Access the web interface**
   
   Open your browser and navigate to: `http://localhost:8080`
   
   Default credentials:
   - Username: `airflow`
   - Password: `airflow`

### Using Standalone Mode

1. **Run the start script**
   ```bash
   ./start.sh
   ```

   This will:
   - Create a virtual environment
   - Install Airflow and all required dependencies
   - Start Airflow in standalone mode

## Project Structure

```
airflow-local/
├── dags/                           # Airflow DAG definitions
│   ├── hello_world_dag.py         # Simple example DAG
│   └── mssql_example_dag.py       # MSSQL integration example
├── logs/                           # Airflow logs directory
├── kube/                           # Kubernetes-related files
│   └── login.sh                   # AKS login script
├── docker-compose.yaml            # Docker Compose configuration
├── requirements.txt               # Python dependencies
├── start.sh                       # Standalone startup script
├── values.yaml                    # Helm chart values for K8s deployment
└── LICENSE                        # License file
```

## Services

The Docker Compose setup includes the following services:

| Service | Description | Port |
|---------|-------------|------|
| **postgres** | PostgreSQL metadata database | 5432 (internal) |
| **redis** | Redis message broker | 6379 (internal) |
| **airflow-webserver** | Web UI and API server | 8080 |
| **airflow-scheduler** | DAG scheduler | - |
| **airflow-worker** | Celery worker | - |
| **airflow-triggerer** | Triggerer for deferrable tasks | - |
| **airflow-init** | Initialization service | - |

## Example DAGs

### Hello World DAG
Located at `dags/hello_world_dag.py` - A simple example that prints "Hello World!" and runs hourly.

### MSSQL Example DAG
Located at `dags/mssql_example_dag.py` - Demonstrates:
- Connecting to Microsoft SQL Server
- Using MsSqlHook to query data
- Processing data with pandas
- Azure Application Insights integration

## Configuration

### Environment Variables

You can customize the following environment variables in a `.env` file:

```bash
# Airflow image
AIRFLOW_IMAGE_NAME=apache/airflow:2.3.4

# User ID for Airflow containers
AIRFLOW_UID=50000

# Admin credentials
_AIRFLOW_WWW_USER_USERNAME=airflow
_AIRFLOW_WWW_USER_PASSWORD=airflow

# Additional pip requirements
_PIP_ADDITIONAL_REQUIREMENTS=
```

### Airflow Configuration

Key configurations in `docker-compose.yaml`:

- **Executor**: CeleryExecutor
- **Load Examples**: Disabled
- **DAGs Paused at Creation**: Enabled
- **Authentication**: Basic Auth

### Adding Connections

To add database connections (e.g., for MSSQL):

1. Open the Airflow UI at `http://localhost:8080`
2. Go to **Admin** → **Connections**
3. Click the **+** button to add a new connection
4. For MSSQL, configure:
   - Connection Id: `mssql_default`
   - Connection Type: `Microsoft SQL Server`
   - Host: `your-server-host`
   - Schema: `your-database`
   - Login: `your-username`
   - Password: `your-password`

## Development

### Adding New DAGs

1. Create a new Python file in the `dags/` directory
2. Define your DAG using the Airflow API
3. The scheduler will automatically detect and load the new DAG

Example:
```python
from airflow import DAG
from airflow.operators.python import PythonOperator
from datetime import datetime

def my_function():
    print("Hello from my DAG!")

with DAG(
    dag_id="my_new_dag",
    start_date=datetime(2021, 1, 1),
    schedule_interval="@daily",
    catchup=False
) as dag:
    task = PythonOperator(
        task_id="my_task",
        python_callable=my_function
    )
```

### Installing Additional Dependencies

Add packages to the `_PIP_ADDITIONAL_REQUIREMENTS` environment variable:

```bash
_PIP_ADDITIONAL_REQUIREMENTS=package1 package2 package3
```

## Kubernetes Deployment

For production deployment to Kubernetes, use the included `values.yaml` with the official Airflow Helm chart:

```bash
# Login to AKS (if using Azure)
./kube/login.sh

# Install Airflow using Helm
helm repo add apache-airflow https://airflow.apache.org
helm install airflow apache-airflow/airflow -f values.yaml
```

## Useful Commands

### Docker Compose

```bash
# Start all services
docker-compose up -d

# Stop all services
docker-compose down

# View logs
docker-compose logs -f

# Restart a specific service
docker-compose restart airflow-scheduler

# Access the Airflow CLI
docker-compose run airflow-webserver airflow <command>
```

### Airflow CLI

```bash
# List DAGs
docker-compose run airflow-webserver airflow dags list

# Test a task
docker-compose run airflow-webserver airflow tasks test <dag_id> <task_id> <execution_date>

# Trigger a DAG
docker-compose run airflow-webserver airflow dags trigger <dag_id>
```

## Troubleshooting

### Permission Issues

If you encounter permission errors with logs or DAGs:

```bash
# On Linux, set the correct AIRFLOW_UID
echo "AIRFLOW_UID=$(id -u)" > .env
```

### Services Not Starting

Check resource allocation:
- Ensure Docker has at least 4GB RAM
- Ensure at least 10GB free disk space

View service logs:
```bash
docker-compose logs <service-name>
```

### DAGs Not Appearing

1. Check DAG file syntax: `docker-compose run airflow-webserver airflow dags list-import-errors`
2. Ensure the file is in the `dags/` directory
3. Check scheduler logs: `docker-compose logs airflow-scheduler`

## Cleanup

To completely remove all containers, volumes, and data:

```bash
docker-compose down -v
```

**Warning**: This will delete all metadata, logs, and DAG run history.

## Dependencies

Key dependencies (see `requirements.txt` for full list):
- `apache-airflow==2.3.4`
- `apache-airflow-providers-microsoft-mssql==3.2.0`
- `pandas==1.4.4`
- `pymssql==2.2.5`
- `opencensus-ext-azure==1.1.7` (for Azure Application Insights)

## License

This project is licensed under the Apache License 2.0 - see the [LICENSE](LICENSE) file for details.

## Resources

- [Apache Airflow Documentation](https://airflow.apache.org/docs/)
- [Airflow Docker Documentation](https://airflow.apache.org/docs/apache-airflow/stable/start/docker.html)
- [Airflow Helm Chart](https://airflow.apache.org/docs/helm-chart/stable/index.html)

## Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Submit a pull request

## Support

For issues and questions:
- Check the [Apache Airflow documentation](https://airflow.apache.org/docs/)
- Review Docker Compose logs
- Open an issue in this repository

