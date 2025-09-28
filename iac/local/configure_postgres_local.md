# DynamoDB Setup Guide

This guide will walk you through the steps to set up DynamoDB on your local machine using Docker and configure it for your project.

## Installation (Only first time)

Before getting started, make sure you have the following installed on your machine:

- Docker: (https://docs.docker.com/desktop/install/windows-install/)
- NoSQL Workbench: (https://docs.aws.amazon.com/amazondynamodb/latest/developerguide/workbench.settingup.html)
- AWS CLI: (https://docs.aws.amazon.com/cli/latest/userguide/getting-started-install.html)

### Docker Settings

Next, you need to configure Postgres for your project and Docker compose. Follow the steps below:

1. Open a terminal and navigate to your project directory
2. Make sure that in your .env file you have the following variables configured

```bash
    POSTGRES_LOCAL_USER=myuser
    POSTGRES_LOCAL_PASSWORD=mypassword
    POSTGRES_LOCAL_DB=mydatabase
    POSTGRES_LOCAL_HOST=localhost
    POSTGRES_LOCAL_PORT=5432
```

3. Make sure this variables are the same in your `iac/local/docker-compose.yml` file and have the same values
4. Then, prompt the following command:

```bash
    iac/local/docker-compose up -d
```

## Launch PostgreSQL in Docker

Start the PostgreSQL container using Docker:

1. Open Docker
2. Start local container

## Running the `load_user_mock_to_postgres` Script

Finally, you can run the `load_user_mock_to_postgres` script to load mock data into Postgres. Follow the steps below:

1. Locate the directory or file named `load_user_mock_to_postgres` within your project. This directory or file is responsible for loading mock data into PostgreSQL.
2. If the `load_user_mock_to_postgres` file doesn't exist, you need to create it.
3. Once you have located or created the `load_user_mock_to_postgres` file, make sure it is in the correct location within your project structure. The file should be located in the `src/shared/infra/repositories`` directory, as shown below:

```bash
.
├── iac
├── src
│   ├── ...
│   │     
│   │    
│   └── shared
│       ├── domain
│       │   └── ...
│       │   
│       ├── helpers
│       │   └── ...
│       │   
│       └── infra
│           ├── dto
│           ├── external
│           └── repositories
│               └── -> [load_user_mock_to_postgres] <-
...
```

4. This file is responsible for populating PostgreSQL with mock data
5. Then, make sure you are in the root directory of your project again
6. Run the following command to execute the script:

```bash
   python -m src.shared.infra.repositories.load_user_mock_to_postgres
```

This command will run the `load_user_mock_to_postgres` script and populate PostgreSQL with the provided mock data

## Using DBever for visualization

You can use DBever to visualize and manage your PostgreSQL database. Follow the steps below:

1. Open DBever
2. Create a new connection
3. Select PostgreSQL
4. Fill the connection details with the ones in your .env file
5. Test the connection and save it
6. You can now visualize and manage your PostgreSQL database using DBever

## Stopping PostgreSQL Container

When you are done using PostgreSQL, you can stop the container by running the following command in your terminal:

```bash
   iac/local/docker-compose down
```
