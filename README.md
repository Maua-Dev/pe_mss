# Portal das Entidades – Microservice (pe_mss)

Backend microservice of the **Portal das Entidades (PE)** platform.  
This service manages **Users** and **Warnings**, following **Clean Architecture** and running as stateless **AWS Lambda** functions behind **API Gateway**.

- **Users** are stored in **Aurora PostgreSQL (RDS Data API)**
- **Warnings** are stored in **DynamoDB**
- **S3 + CloudFront** handle user uploads
- **EventBridge** triggers scheduled tasks (e.g. warning deletion)
- **Secrets Manager** stores sensitive configuration
- **AWS CDK (Python)** manages all infrastructure (`iac/`)

---

## Project Overview

- **Domain**: management of users and warnings for the Portal das Entidades.
- **Runtime**: AWS Lambda + API Gateway, token-based authorization using **Microsoft Graph**.
- **Architecture**: Clean Architecture with clear separation between `modules` (use cases), `shared/domain`, `shared/infra`, and `iac` for infrastructure.
- **API base path**: typically exposed under `/pe-mss` (e.g. `/pe-mss/get-user`, `/pe-mss/create-warning`).

---

## High-Level Architecture

- **API Gateway**: routes HTTP requests to Lambda functions (one function per module/use case).
- **Lambda functions (`src/modules`)**: application entrypoints; orchestrate use cases, repositories, and view models.
- **Domain (`src/shared/domain`)**:
  - `entities`: core entities like `user` and `warning`
  - `enums`: role, organization, course, state, and active flags
  - `repositories` (interfaces): domain-level contracts for persistence
- **Infrastructure (`src/shared/infra`)**:
  - `external`: integration with AWS services (DynamoDB, Postgres/RDS, observability)
  - `repositories`: concrete implementations (User in Postgres/Aurora-style DB, Warning in DynamoDB)
- **AWS Clients (`src/shared/clients`)**: thin wrappers around `boto3` clients for S3, Secrets Manager, and EventBridge.
- **IaC (`iac/`)**: AWS CDK application that defines all resources, environments, and wiring.

---

## Directory Structure (Main Elements)

```bash
.
├── iac/                # AWS CDK app (infrastructure as code)
├── src/
│   ├── modules/        # Lambda entrypoints by use case
│   └── shared/         # Domain, infra, clients, helpers
└── tests/              # Unit and integration tests
```

### Modules (`src/modules`)

Each subdirectory represents a Lambda-backed use case exposed via API Gateway. Examples:

- **User-related**
  - `auth_user` – authorizes a user based on token and Microsoft Graph
  - `create_user` – creates a new user in Aurora PostgreSQL
  - `delete_user` – deletes a user
  - `get_user` / `get_all_users` – fetches a single user or a list of users
  - `update_user` – updates user attributes
  - `upload_users` – bulk user upload (can be invoked by another Lambda using ARN)
  - `export_users` – exports user data (e.g. to a file or stream)

- **Warning-related**
  - `create_warning` – creates a warning for a user/role/organization
  - `delete_warning` – deletes warnings, including those scheduled via EventBridge
  - `get_warning` / `get_all_warnings` – reads warnings from DynamoDB

Each module follows Clean Architecture: controller → use case → repositories/entities → view model/presenter.

### Shared Domain (`src/shared/domain`)

- **`entities/`**
  - `user.py` – user entity (id, name, email, role, organization, etc.)
  - `warning.py` – warning entity (title, description, schedule, owner, etc.)
- **`enums/`**
  - Role, organization, course, state, active flags (`*_enum.py`)
- **`repositories/`**
  - Interfaces for user and warning persistence (implemented in `infra/repositories`).

### Shared Infra (`src/shared/infra`)

- **`external/`**
  - `dynamo/` – DynamoDB datasource and table configuration
  - `postgres/` – Aurora Postgres-style datasource using RDS Data API
  - `observability/` – logging, tracing or metrics helpers
- **`repositories/`**
  - Implementations of domain repositories:
    - User repository (Aurora/Postgres)
    - Warning repository (DynamoDB)
  - Mock repositories and scripts to load mock data.

### Authorization (`src/shared/authorizer`)

- `graph_authorizer.py` – validates tokens using Microsoft Graph; plugged into API Gateway as a Lambda authorizer.

---

## AWS Client Files (Wrappers)

Located in `src/shared/clients/`:

- **`s3_client.py`**
  - Wraps the S3 client (supports endpoint override for local development using MinIO).
  - Used for file uploads/exports in user-related flows.

- **`sm_client.py`**
  - Wraps **AWS Secrets Manager** access (get/put secrets).
  - Central place for reading environment-specific configuration (DB secrets, Graph credentials, etc.).

- **`event_bridge_client.py`**
  - Wraps **Amazon EventBridge**.
  - Creates and manages rules/targets for scheduled warning deletion or other time-based workflows.

These wrappers centralize configuration (e.g. region, endpoints, retries) and make unit testing easier.

---

## Mock Data & Datasources for Users

User-related mocks are used both for **tests** and for populating **local/real data stores**.

- **`UserRepositoryMock` (`src/shared/infra/repositories/user_repository_mock.py`)**
  - Pure in-memory implementation of `IUserRepository` with a fixed list of users (students, presidents, admin).
  - Used directly in tests (see `tests/shared/infra/repositories/test_user_repository_mock.py`) to validate behavior without hitting any external service.
  - Also acts as the **single source of truth** for mock users when seeding databases.

- **Local Postgres / Aurora-style datasource (`load_user_mock_to_postgres.py`)**
  - Script: `src/shared/infra/repositories/load_user_mock_to_postgres.py`.
  - Connects to a **local PostgreSQL** instance (configured via `.env` and `iac/local/docker-compose.yml`) using `psycopg2`.
  - Creates a `users` table with the same shape expected by the Aurora/RDS Data API–backed repository.
  - Truncates the table and bulk-inserts all users from `UserRepositoryMock`.
  - This gives you a local relational dataset that mirrors the **Aurora** schema and contents for development/debugging.

- **DynamoDB datasources for user mocks (`load_user_mock_to_dynamo.py`)**
  - Script: `src/shared/infra/repositories/load_user_mock_to_dynamo.py`.
  - Uses `UserRepositoryMock` as the data source and `UserRepositoryDynamo` (real DynamoDB repository) as the writer.
  - **`load_mock_to_local_dynamo()`**
    - Spins up or connects to **DynamoDB Local** at `http://localhost:8000`.
    - Ensures the local table (e.g. `user_mss_template-table`) exists and seeds a `COUNTER` item.
    - Iterates over `UserRepositoryMock.users` and persists them via `UserRepositoryDynamo.create_user`.
  - **`load_mock_to_real_dynamo()`**
    - Connects to **real AWS DynamoDB** using the table name from `Environments.get_envs().dynamo_table_name`.
    - Seeds the same `COUNTER` item and then loads all mock users using the production-style repository.

In summary:

- **Tests** use `UserRepositoryMock` directly (no external services).
- **Local relational DB** uses `load_user_mock_to_postgres.py` to mirror the Aurora user dataset in a local Postgres container.
- **Local and real DynamoDB** use `load_user_mock_to_dynamo.py` to load the same mock user set into DynamoDB (both local and cloud), ensuring consistency across environments.

---

## Infrastructure as Code (IaC) – `iac/`

The `iac/` directory is an **AWS CDK (Python)** project that defines all infrastructure for this microservice.

- **Entry point**
  - `app.py` – reads environment (e.g. `STACK_NAME`, `AWS_ACCOUNT_ID`, `AWS_REGION`) and instantiates `IacStack`.

- **Main stack**
  - `stack/iac_stack.py`
    - Declares the main **Portal Entidades** stack.
    - Composes constructs for API Gateway, Lambdas, Aurora, DynamoDB, S3/CloudFront, Secrets Manager, and EventBridge.

- **Constructs (`components/`)**
  - `aurora_construct.py` – Aurora PostgreSQL Serverless v2 cluster + VPC + RDS Data API configuration.
  - `dynamo_construct.py` – DynamoDB table for warnings, including GSI such as `RoleOrgIndex`.
  - `bucket_construct.py` – S3 bucket with CloudFront distribution for static content/uploads.
  - `lambda_construct.py` – Lambda functions for all modules; integrates with API Gateway routes and authorizer.
  - `sm_construct.py` – Secrets Manager configuration (e.g. credentials, EventBridge secrets).

- **Environments / stacks**
  - Typical stack names: `PortalEntidadesStackdev`, `PortalEntidadesStackhomolog`, `PortalEntidadesStackprod`.
  - Environment is controlled via `STACK_NAME` and account/region environment variables.

There are also auxiliary files under `iac/local/` to support local infrastructure.

---

## Local Development

Local setup is supported with Docker, local Postgres, DynamoDB Local, and optional SAM for invoking Lambdas.

- **Dependencies**
  - Python 3.11+
  - Docker + Docker Compose
  - Node.js (for CDK CLI)

- **Python environment**

  ```bash
  python -m venv venv
  source venv/bin/activate      # macOS / Linux
  # or
  venv\Scripts\activate         # Windows

  pip install -r requirements-dev.txt
  ```

- **Local infrastructure**
  - `iac/local/docker-compose.yml` – runs a local Postgres instance for Aurora compatibility.
  - `iac/local/minio/docker-compose.yml` – runs MinIO as an S3-compatible storage.
  - `iac/local/README.md` – detailed instructions for SAM, DynamoDB Local, and Postgres configuration (including `load_user_mock_to_postgres`).

- **Local environment variables (example)**

  ```bash
  STAGE=TEST

  POSTGRES_LOCAL_USER=myuser
  POSTGRES_LOCAL_PASSWORD=mypassword
  POSTGRES_LOCAL_DB=mydatabase
  POSTGRES_LOCAL_HOST=localhost
  POSTGRES_LOCAL_PORT=5432

  DYNAMO_ENDPOINT_URL=localhost
  DYNAMO_ENDPOINT_PORT=8000
  DYNAMO_REGION=local
  ```

Additional variables are required for cloud environments (e.g. `AWS_ACCOUNT_ID`, `AWS_REGION`, `STACK_NAME`, `GRAPH_MICROSOFT_ENDPOINT`, `CREATE_USER_ENDPOINT`).

---

## Deployment (CDK)

From the `iac/` directory:

```bash
cd iac
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt

cdk synth    # synthesize CloudFormation templates
cdk deploy   # deploy the stack to the configured AWS account/region
```

Useful commands:

- `cdk ls` – list stacks
- `cdk synth` – emit the synthesized template
- `cdk deploy` – deploy the stack
- `cdk diff` – compare with deployed state

CI/CD (if configured) will typically deploy from specific branches (`dev`, `homolog`, `prod`) into matching environments.

---

## Running Tests

From the project root (with `venv` active):

```bash
pytest
```

Tests are structured to mirror the main code:

- `tests/modules/...` – tests for each module (use case)
- `tests/shared/...` – tests for domain entities, helpers, and infra components

---

## Naming & Conventions (Code Style)

- **Files & directories**: `snake_case` (e.g. `create_user_controller.py`).
- **Classes**: `CamelCase` (e.g. `CreateUserUsecase`, `WarningRepositoryDynamo`).
- **Interfaces**: start with `I` (e.g. `IUserRepository`).
- **Repositories**: same name as interface without `I`, plus type suffix (e.g. `UserRepositoryMock`, `UserRepositoryDynamo`).
- **Controllers / Usecases / Viewmodels / Presenters**:
  - `*Controller`, `*Usecase`, `*Viewmodel`, `*Presenter`.
- **Methods & variables**: `snake_case`, methods usually start with a verb (`create_user`, `get_warning`).
- **Tests**: files start with `test_` and follow the class or behavior name.

These conventions keep the Clean Architecture layers consistent across modules and make it easy to navigate the codebase.

## Contributors 💰🤝💰

- Leonardo Luiz Seixas Iorio - [lseixas](https://github.com/lseixas) 🥷
- Lucas Gozze Crapino - [LucasCrapino](https://github.com/LucasCrapino) 🐼


## Special Thanks 🙏

- [Dev. Community Mauá](https://www.instagram.com/devcommunitymaua/)
- [Clean Architecture: A Craftsman's Guide to Software Structure and Design](https://www.amazon.com.br/Clean-Architecture-Craftsmans-Software-Structure/dp/0134494164)
- [Institute Mauá of Technology](https://www.maua.br/)
