# page analyzer
[![Actions Status](https://github.com/ithemask/python-project-83/actions/workflows/hexlet-check.yml/badge.svg)](https://github.com/ithemask/python-project-83/actions)
[![Linter](https://github.com/ithemask/python-project-83/actions/workflows/flake8-check.yml/badge.svg)](https://github.com/ithemask/python-project-83/actions/workflows/flake8-check.yml)
[![Maintainability](https://api.codeclimate.com/v1/badges/763cb23e92ab619c90ef/maintainability)](https://codeclimate.com/github/ithemask/python-project-83/maintainability)
## _Short description_
___page analyzer___ _is a web service that helps you find out whether your website provides data, which is being used 
by search engines to understand it's content. Web service analyzes a presence of HTML elements, which help users find 
your website through a search engine and make a decision about whether they should visit it or not._
### _[---> click here to start using online <---](https://page-analyzer-7k2n.onrender.com)_
_or you may use __page analyzer__ locally following the instructions below._
## _Local usage_
### <u>_Requirements_</u>
  + _OS Linux_
  + _Python >= 3.10_
  + _Pip >= 24.0_
  + _Poetry >= 1.8_
  + _PostgreSQL >= 14.0_
### <u>_Installation_</u>
  + _Cloning a repository_
    ```
    git clone git@github.com:ithemask/python-project-83.git
    cd python-project-83
    ```
  + _Setting environment variables_
    ```
    export SECRET_KEY={secret_key}
    export DATABASE_URL=postgresql://{username}:{password}@{host}:{port}/{database_name}
    ```
  + _Installing dependencies and initializing database tables_
    ```
    make build
    ```
    _**Attention! Existing tables "urls" and "url_checks" will be overwritten.**_
### <u>_Usage_</u>
  + _Run a web server with_ `make start`
  + _Go to **http://127.0.0.1:5000**_
