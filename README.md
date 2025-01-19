# What to do

API to finally find what to do.

## Getting Started

Follow the steps below to set up and run the project.

### Prerequisites

Install `Docker Desktop` from [official website](https://www.docker.com/).
`docker-compose` will be installed by default.

### Setup

1. **Clone the repository**

   Pull the project to your local machine:

   ```sh
   git clone https://github.com/iamkorniichuk/what-to-do.git
   cd what-to-do
   ```

2. **Set up environment**

   Create a `.env` file in the root directory and populate it with variables like showed in [example](.env.example).

3. **Run the project**

   Build the containers and start the application:

   ```sh
   docker-compose up --build
   ```

   > :warning: Make sure you have running Docker instance.

   You can access API's schema at http://127.0.0.1:8000/schema/swagger/
