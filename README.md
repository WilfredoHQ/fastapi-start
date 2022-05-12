<div id="top"></div>
<br />
<div align="center">
  <a href="https://github.com/wilfredohq/fastapi-start">
    <img
      src="https://github.com/WilfredoHQ/md-readme/raw/main/images/logo.png"
      alt="Logo"
      width="80"
      height="80"
    />
  </a>
  <h3 align="center">FastAPI Start</h3>
  <p align="center">
    Simple structure for backend projects with FastAPI and PostgreSQL.
    <br />
    <a href="https://github.com/wilfredohq/fastapi-start">
      <strong>Explore the docs »</strong>
    </a>
    <br />
    <br />
    <a href="https://bwstart.herokuapp.com/docs">
      View demo
    </a>
    ·
    <a href="https://github.com/wilfredohq/fastapi-start/issues">
      Report bug
    </a>
    ·
    <a href="https://github.com/wilfredohq/fastapi-start/issues">
      Request feature
    </a>
  </p>
</div>
<details>
  <summary>Table of contents</summary>
  <ol>
    <li>
      <a href="#about-the-project">About the project</a>
      <ul>
        <li><a href="#built-with">Built with</a></li>
      </ul>
    </li>
    <li>
      <a href="#getting-started">Getting started</a>
      <ul>
        <li><a href="#prerequisites">Prerequisites</a></li>
        <li><a href="#installation">Installation</a></li>
      </ul>
    </li>
    <li><a href="#contributing">Contributing</a></li>
    <li><a href="#license">License</a></li>
  </ol>
</details>

## About the project

This is a base project to have a starting point for RESTful API projects with FastAPI based on [Full Stack FastAPI and PostgreSQL - Base Project Generator](https://github.com/tiangolo/full-stack-fastapi-postgresql) a project by [Sebastian Ramirez](https://github.com/tiangolo).

<p align="right">(<a href="#top"> ↑ back to top </a>)</p>

### Built with

-   [Python ^3.10](https://www.python.org/)
-   [PostgreSQL](https://www.postgresql.org/)

<p align="right">(<a href="#top"> ↑ back to top </a>)</p>

## Getting started

To obtain a working local copy, follow these simple steps.

### Prerequisites

Things you need to use the software and how to install them.

-   Python ^3.10
-   PostgreSQL

### Installation

1. Clone the repository.

    ```sh
    git clone https://github.com/wilfredohq/fastapi-start.git
    ```

2. Create a new database.
3. Make a copy of `.env.example` with the name `.env` and set your environment variables.

4. Install poetry.

    ```sh
    pip install poetry
    ```

5. Install poetry packages.

    ```sh
    poetry install
    ```

6. You can then start a shell session in the new environment.

    ```sh
    poetry shell
    ```

7. Migrate the database.

    ```sh
    alembic upgrade head
    ```

    **Note:** If you modify the tables, you must first generate a new revision.

    ```sh
    alembic revision --autogenerate -m "structure change message"
    ```

8. Create the first superuser.

    ```sh
    python -m app.initial_data
    ```

9. Run the uvicorn server.

    ```sh
    uvicorn app.main:app --host 0.0.0.0 --port 8000 --reload
    ```

10. Now you can open your browser and interact with these URLs.
    - Backend, JSON based web API based on OpenAPI: http://localhost:8000/api/v1/openapi.json
    - Automatic interactive documentation with Swagger UI (from the OpenAPI backend): http://localhost:8000/docs
    - Alternative automatic documentation with ReDoc (from the OpenAPI backend): http://localhost:8000/redoc

<p align="right">(<a href="#top"> ↑ back to top </a>)</p>

## Contributing

Contributions are what make the open source community such an amazing place to learn, inspire, and create. Any contributions you make are **greatly appreciated**.

If you have a suggestion that would make this better, please fork the repository and create a pull request. You can also simply open an issue with the tag "enhancement".
Don't forget to give the project a star! Thanks again!

1. Fork the project
2. Create your feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'feat: add some amazing-feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a pull request

<p align="right">(<a href="#top"> ↑ back to top </a>)</p>

## License

Distributed under the MIT License. See [LICENSE](LICENSE) for more information.

<p align="right">(<a href="#top"> ↑ back to top </a>)</p>
