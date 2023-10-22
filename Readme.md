# Stock Data ETL Dashboard

This project is designed to set up a Docker environment for an end-to-end data engineering project. It includes a [Chartbrew](https://hub.docker.com/r/razvanilin/chartbrew) instance to visualize data. The setup consists of MySQL containers, a Python data fetching container, and a shell script to launch Chartbrew once the MySQL databases are initialized.

![Alt Text](https://github.com/caidam/stockdata-etl-chartbrew/blob/main/misc/stockdataetl-dashboard.png)

## Prerequisites

Before getting started, make sure you have the following prerequisites installed:

- [Docker](https://www.docker.com/get-started/)
- [Docker Compose](https://docs.docker.com/compose/install/)

## Project Structure

The project directory is structured as follows:

 ```
    StockDataETL-Dashboard/
    │
    ├── docker-compose.yml
    ├── run-chartbrew-container.sh
    └── python_container/
        ├── credentials.py
        ├── Dockerfile
        ├── main.py
        └── requirements.txt
 ```

### `docker-compose.yml`

The `docker-compose.yml` file defines the Docker services for your project. It sets up the necessary containers, including MySQL databases and the python script. It also configures the network for communication between containers.

### `run-chartbrew-container.sh`

The `run-chartbrew-container.sh` script helps launching the Chartbrew container with the required environment variables once the MySQL databases are initialized.

### `python_container/`

The python_container folder contains the Python script and related files:

- `credentials.py`: Store your [API keys](https://rapidapi.com/amansharma2910/api/realstonks) and database connection details here.
- `Dockerfile`: Defines the Docker image for the Python script.
- `main.py`: Contains the Python script for fetching and uploading stock data.
- `requirements.txt`: Lists the Python dependencies required for the script.

## Getting Started

Follow these steps to set up and run your StockDataETL-Dashboard:

1. Clone this repository to your local machine or cloud instance.

```bash
    git clone https://github.com/caidam/stockdata-etl-chartbrew.git
```

2. Ensure you have Docker and Docker Compose installed.

3. Open a terminal and navigate to the project directory.

4. Run the following command to start the Docker containers:

```bash
    sudo docker compose -f docker-compose.yml up --build -d
```
This command will create and start the MySQL containers and the Chartbrew container.

5. To check if the chartbrewdata MySQL database has been created run the following commands :

```bash
    sudo docker exec -it mysql-chartbrewdata bash
```

This will enable you to run commands from inside the container :

```bash
    mysql -u root -p
```

Enter the password you chose in the Dockerfile, then :

```sql
    SHOW databases;
```
Finally, make sure you can locate the `chartbrew` database and exit the container.

6. Start the chartbrew container :

First make the script executable :

```bash
    chmod +x run-chartbrew-container.sh
```

Then run it :

```bash
    ./run-chartbrew-container.sh
```

> If you're running the project on a cloud instance replace the "http://localhost" portions inside the script with the public IP of your instance before running it.

7. Your Chartbrew instance should now be accessible at:

- Frontend: http://localhost:4018
- API: http://localhost:4019

> Similarlly, if you're running the project on a cloud instance replace the "http://localhost" portion with the public IP of your instance.

8. The Python script in the python_container will automatically fetch and upload stock data to the `financialdata` MySQL database every minute.

9. Open Chartbrew's frontend, sign in, connect to `financialdata` and start designing your dashboard.

## Cutsomization

- You can customize the Python script in `main.py` to fetch data from your desired source.

- Update `credentials.py` with your API keys and database connection details.

- Modify the `requirements.txt` file to include any additional Python dependencies.

- Adjust the MySQL container configurations in the `docker-compose.yml` file to suit your needs including username, password etc.

- Adjust the `run-chartbrew-container.sh` script depending on how you plan on running this project.

## Troubleshooting

- If you encounter any issues or want to view container logs, use the following command:

```bash
    sudo docker logs -f container-id

    # alternatively when applicable
    sudo docker-compose logs
```

The `-f` or follow flag will stream the logs in real-time in the terminal. Stop it with CTRL + C.

- You can stop docker containers using :

```bash
    # stop containers by name or id
    sudo docker stop container-id

    # stop all running containers
    sudo docker stop $(docker ps -a -q)

    # stop all containers you started with docker compose
    sudo docker-compose down

```

- If you want to check network information use :

```bash
    # get the list of networks
    sudo docker network ls
    
    # get container information, including network related :
    sudo docker inspect container-id
```

- If you want to open a terminal inside a container :

```bash
    sudo docker exec -it container-id bash
```

> In most of these commands the name of a container can be used instead of its id.

## Cleaning up

Containers can take a lot of sapce on your computer or instance quickly, use the following commands to monitor and clean up your docker environment.

- Delete containers :

```bash
    sudo docker rm container-id
```

- Delete images :

``` bash
    sudo docker rmi container-id
```

- Get list of volumes :

```bash
    sudo docker volume ls
```
 - Delete volume :

 ```bash
    sudo docker volume rm volume-name
 ```

- Hardcore cleaning :

```bash
    sudo docker prune -a
```

> The `-a` flag removes all images, even those that are not associated with any containers. Be cautious when using this command, as it will remove all unused resources.
