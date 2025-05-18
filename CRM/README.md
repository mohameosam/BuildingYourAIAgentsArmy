# Computer Store CRM & n8n Integration

This repository provides a complete setup for the **Computer Store** backend service built with Flask and MySQL, orchestrated via Docker Compose, along with example n8n workflows (including MCP Client and Server) that interact with the API.

---

## Table of Contents
- [Project Overview](#project-overview)
- [Prerequisites](#prerequisites)
- [Architecture & Services](#architecture--services)
- [Installation & Running](#installation--running)
- [Environment Variables](#environment-variables)
- [API Endpoints](#api-endpoints)
- [n8n Workflows](#n8n-workflows)
  - [Chat Workflow (Computer Store)](#chat-workflow-computer-store)
  - [MCP Client Workflow](#mcp-client-workflow)
  - [MCP Server Workflow](#mcp-server-workflow)
- [License](#license)

---

## Project Overview
The **Computer Store** project offers:

1. A Flask-based CRM API (`crm_api`) for managing customers, products, and orders (`app.py`) citeturn0file0
2. A MySQL database to store `customer`, `product`, `order`, and `order_item` data.
3. A Docker Compose stack to orchestrate all services: MySQL, Flask API, n8n, Postgres (for n8n), pgvector, Ollama, Botpress citeturn1file2
4. n8n workflows demonstrating chat-triggered shopping, with both standard HTTP nodes and Model Context Protocol (MCP) integration.

## Prerequisites
- Docker & Docker Compose (v3.8+) installed
- (Optional) Access to Gmail OAuth2 credentials for email sending in n8n workflows

## Architecture & Services
- **mysql**: Holds CRM data (`crm_database`). Initialized via SQL scripts in `CRM/mysql-init`. citeturn1file2
- **crm_api**: Flask app serving RESTful endpoints on port `5000`. Built from `CRM/crm_flask_api` directory. citeturn1file2
- **n8n**: Workflow automation on port `5678`, backed by Postgres. Configured with basic auth.
- **postgres & pgvector**: n8n’s primary and vector databases.
- **ollama & botpress**: AI model hosting and chat GUI (optional).

## Installation & Running

1. Clone the repository:
   ```bash
   git clone <repo-url>
   cd <repo-dir>
   ```
2. Bring up all containers:
   ```bash
   docker-compose up -d
   ```
3. Verify services:
   ```bash
   docker ps
   ```
4. The CRM API is available at `http://localhost:5000`.

## Environment Variables
Set via Docker Compose for `crm_api`:

- `DB_HOST` (default: `mysql`)
- `DB_USER` (default: `crm_user`)
- `DB_PASSWORD` (default: `crm_pass`)
- `DB_NAME` (default: `crm_database`)

## API Endpoints

All endpoints are served under `http://<host>:5000` by `crm_api`.

### Customer Lookup
- **GET** `/customer/phone/<phone>`
  - Fetch a single customer by phone number.
  - Returns a JSON object (or `{}` if not found). citeturn0file0

### Create Order with Items
- **POST** `/order`
  - Payload:
    ```json
    {
      "phone": "<customer_phone>",
      "products": [
        { "product_id": 1, "quantity": 2 },
        { "product_id": 3, "quantity": 1 }
      ]
    }
    ```
  - Validates customer exists, calculates totals, inserts into `order` and `order_item` tables. Returns `order_id`, `order_date`, and `total_amount`. citeturn0file0

### Generic CRUD Endpoints
> **Note**: Orders must use `/order`. Other tables use generic routes.

- **GET** `/<table>`
  - List all records in the specified table.
- **GET** `/<table>/<id>`
  - Fetch a single record by `<table>_id`.
- **POST** `/<table>`
  - Create a new record. Field names in JSON body map directly to columns. Returns success message.
  - For `order`, returns a 404 error advising to use `/order`.
- **PUT** `/<table>/<id>`
  - Update record by `<table>_id`. JSON body keys are updated fields.
- **DELETE** `/<table>/<id>`
  - Delete record by `<table>_id`.

All generic endpoints handle errors with `500` status on exceptions. citeturn0file0

## n8n Workflows

### Chat Workflow (Computer Store)
Located in `Computer_Store.json`, this flow triggers on chat messages and uses HTTP Request nodes to:

1. Lookup or register customer (`/customer` endpoints). 
2. List available products (`GET /product`).
3. Place orders (`POST /order`).
4. Send confirmation emails via Gmail node. citeturn0file1

### MCP Client Workflow
In `Computer_Store___MCP_Client.json`, the MCP Client node connects via SSE to the MCP Server, allowing tool calls (`Register_Customer`, `get_customer_by_phone`, `List_Products`, `Make_Order`, `Send_Email`) to be dispatched through the workflow runtime. citeturn0file2

### MCP Server Workflow
The MCP Server flow (`Computer_Store___MCP_Server.json`) listens on the MCP webhook, exposes the same HTTP Request tools as above, and acts as the backend for MCP-driven agents. citeturn0file3

## License
This project is licensed under the MIT License. Feel free to use and modify as needed.
