# Test Contracts

This project was written in ***Python** language using a version **3.12.6**, with the framework **Django Rest Framework**, the of default **REST***, **docker**, **docker-compose**, **PostgreSql** to database*** and was used an **object oriented programming**. 
This porject was used **django-filters** to filter searches in database. Other deatail this project is change the settings to connect in SQLite databse.

# Install

For the local installation, you must have Python language 3.12.6 the package manager PIP and execute the following command:
```sh
pip install -r requiriments.txt 
```

Case have the docker-compose installed execute the command:
```sh
docker-compose up
```

obs: In case the not working in firstime, execute again o command **docker-compose up** maybe not create database and tables to working correct of project. 


This will create one container ready for use.

## Environment Variable
```sh
export NAME=contracts
export USER=postgres
export PASSWORD=123456
export HOST="0.0.0.0"
export PORT=5432
```

# Execution System:

Create Database

```sh
 psql -U postgres -c 'create database contracts;'
```

It add the Environment of according with choices and execute:

```sh

python manager.py makemigrations # create changes of postgre database
python manager.py migrate # for create tables the of postgre database
python manager.py runserver # start application
```

# API


# Executions of Endpoints:

Create Contract with curl:

```sh
curl -X POST \
  http://localhost:8000/api/contracts/ \
  -H 'Cache-Control: no-cache' \
  -H 'Content-Type: application/json' \
  -H 'Postman-Token: 023ab60d-8de3-49e2-89e0-b07bd1126ca8' \
  -d '{"issue_date": "2020-05-18",
  "born_date": "1989-04-04",
  "value": 1000,
  "cpf": "40425173070",
  "country": "Brazil",
  "province": "MG",
  "city": "Sao Francisco",
  "telephone": "+5538993685543",
  "tax": 19.33,
  "invoices": [{
  "invoice_number": 1234,
  "value": 1000,
  "due_date": "2024-04-04"
  }
 ]

}
'

{"id": 1} 
```
Search Contract by to all contracts
```sh

curl -X GET http://localhost:8000/api/contracts/
[{
    "id": 1,
    "issue_date": "2020-05-18",
    "born_date": "1989-04-04",
    "value": 1000.0,
    "cpf": "40425173070",
    "country": "Brazil",
    "province": "MG",
    "city": "Sao Francisco",
    "telephone": "+5538993685543",
    "tax": 19.33,
    "invoices": [
        {
            "id": 1,
            "invoice_number": 1234,
            "value": 1000.0,
            "due_date": "2024-04-04"
        }
    ]
}]

```

Search Contract by id

```sh
curl -X GET http://localhost:8000/api/contracts/?id=1

[{
    "id": 1,
    "issue_date": "2020-05-18",
    "born_date": "1989-04-04",
    "value": 1000.0,
    "cpf": "40425173070",
    "country": "Brazil",
    "province": "MG",
    "city": "Sao Francisco",
    "telephone": "+5538993685543",
    "tax": 19.33,
    "invoices": [
        {
            "id": 1,
            "invoice_number": 1234,
            "value": 1000.0,
            "due_date": "2024-04-04"
        }
    ]
}]

```

Search Contract by cpf

```sh
curl -X GET http://localhost:8000/api/contracts/?cpf=40425173070

[{
    "id": 1,
    "issue_date": "2020-05-18",
    "born_date": "1989-04-04",
    "value": 1000.0,
    "cpf": "40425173070",
    "country": "Brazil",
    "province": "MG",
    "city": "Sao Francisco",
    "telephone": "+5538993685543",
    "tax": 19.33,
    "invoices": [
        {
            "id": 1,
            "invoice_number": 1234,
            "value": 1000.0,
            "due_date": "2024-04-04"
        }
    ]
}]
```

Search Contract by issue_date are 3 types differents with same result

```sh
curl -X GET http://localhost:8000/api/contracts/?issue_date=2020-05-18
curl -X GET http://localhost:8000/api/contracts/?issue_date__year=2020
curl -X GET http://localhost:8000/api/contracts/?issue_date__month=05```

[{
    "id": 1,
    "issue_date": "2020-05-18",
    "born_date": "1989-04-04",
    "value": 1000.0,
    "cpf": "40425173070",
    "country": "Brazil",
    "province": "MG",
    "city": "Sao Francisco",
    "telephone": "+5538993685543",
    "tax": 19.33,
    "invoices": [
        {
            "id": 1,
            "invoice_number": 1234,
            "value": 1000.0,
            "due_date": "2024-04-04"
        }
    ]
}]
```

Search Contract by Province

```sh
curl -X GET http://localhost:8000/api/contracts/?province=MG
[{
    "id": 1,
    "issue_date": "2020-05-18",
    "born_date": "1989-04-04",
    "value": 1000.0,
    "cpf": "40425173070",
    "country": "Brazil",
    "province": "MG",
    "city": "Sao Francisco",
    "telephone": "+5538993685543",
    "tax": 19.33,
    "invoices": [
        {
            "id": 1,
            "invoice_number": 1234,
            "value": 1000.0,
            "due_date": "2024-04-04"
        }
    ]
}]
```

Search contracts Consolidate and following same filter as (id, issue_date (with to all options), cpf, province) as above

```sh
  curl -X GET http://localhost:8000/api/contracts/consolidate/
  curl -X GET http://localhost:8000/api/contracts/consolidate/?id=1
  curl -X GET http://localhost:8000/api/contracts/consolidate/?issue_date=2020-05-18
  curl -X GET http://localhost:8000/api/contracts/consolidate/?issue_date__year=2020
  curl -X GET http://localhost:8000/api/contracts/consolidate/?issue_date__month=05
  curl -X GET http://localhost:8000/api/contracts/consolidate/?issue_date__year=2020&issue_date__month=05
  curl -X GET http://localhost:8000/api/contracts/consolidate/?province=MG

{
    "value_tot_pay_out": 3000.0,
    "value_tot_receive": 3000.0,
    "average_tax": 19.33,
    "quantity_contracts": 3
}
  
```

Observation was added more two option one put and delete.

The option put is very simple

Update Information PUT
```sh

curl -X PUT \
  http://localhost:8000/api/contracts/1 \
  -H 'Cache-Control: no-cache' \
  -H 'Content-Type: application/json' \
  -H 'Postman-Token: 023ab60d-8de3-49e2-89e0-b07bd1126ca8' \
  -d '{"issue_date": "2020-05-18",
  "born_date": "1989-04-04",
  "value": 1000,
  "cpf": "40425173070",
  "country": "Brazil",
  "province": "MG",
  "city": "Sao Francisco",
  "telephone": "+5538993685543",
  "tax": 19.33,
  "invoices": [{
  "invoice_number": 1234,
  "value": 1000,
  "due_date": "2024-04-04"
  }
 ]

}
'

```

Delete one record DELETE

```sh
curl -X DELETE http://localhost:8000/api/contracts/1

```
