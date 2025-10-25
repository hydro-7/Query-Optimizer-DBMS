# Query Optimizer – SQL Query Optimization Project

This project demonstrates SQL query optimization techniques using PostgreSQL and the Pagila sample database.  
It is developed as part of the CS315: Principles of Database Systems course project.

---

## Overview

The Query Optimizer allows users to:
- Execute and analyze SQL queries.
- Compare execution performance between original and optimized queries.
- Visualize and evaluate query plans using PostgreSQL.

---

## Prerequisites

Before setting up the project, ensure you have the following installed:

- [Python 3.8+](https://www.python.org/downloads/)
- [PostgreSQL](https://www.postgresql.org/download/)
- [pgAdmin](https://www.pgadmin.org/download/)
- [Git](https://git-scm.com/downloads)

---

## Database Setup (Using pgAdmin)

We use the **Pagila** sample database for this project.

### Step 1: Create a New Database and User

1. Open **pgAdmin** and connect to your PostgreSQL server.  
2. Right-click on **Databases → Create → Database...**  
   - Database name: `optiquery_db`  
   - Owner: your PostgreSQL user (e.g., `postgres`)  
   - Click **Save**.  
3. (Optional) If you wish to use a dedicated user, create one by navigating to:  
   **Login/Group Roles → Create → Login/Group Role...**  
   - Name: `optique_user`  
   - Set a password under the “Definition” tab.  
   - Under “Privileges,” ensure “Can login?” and “Create DB?” are checked.  
   - Click **Save**.

---

### Step 2: Download the Pagila Dataset

Download the following two SQL files from the official Pagila GitHub repository:  

- `pagila-schema.sql` – defines all tables, views, and relationships.  
- `pagila-data.sql` – populates the tables with data.  

Link: [Pagila GitHub Repository](https://github.com/devrimgunduz/pagila/tree/master/pagila-data)

Save both files in an accessible directory, for example:


### Step 3: Load the Schema and Data Using pgAdmin

1. Open **pgAdmin** and select your `optiquery_db` database.  
2. Click on the **Query Tool** icon (lightning symbol).  
3. Open the `pagila-schema.sql` file (File → Open File) and click **Execute**.  
   This will create all tables, views, and relationships.  
4. Once the schema is created, open `pagila-data.sql` and click **Execute** again.  
   This will load all the data into the tables.  
5. After execution, refresh your database to see all the tables and data.

---

## Application Setup

### Step 1: Clone the Repository

```bash
git clone https://github.com/hydro-7/Query-Optimizer-DBMS.git
cd Query-Optimizer-DBMS
```


### Step 2: Create and Activate a Virtual Environment
```bash
python -m venv venv

```
### Activate the environment:

#### Windows:
```bash
venv\Scripts\activate
```

#### Linux/Mac:
```bash
source venv/bin/activate
```
### Step 3: Install Dependencies
```bash
pip install -r requirements.txt
```
### Step 4: Configure Database Credentials
```bash
Open app.py and update the following lines with your PostgreSQL database details:
```
```bash
DB_NAME = "optiquery_db"
DB_USER = "optique_user"
DB_PASSWORD = "your_password"
```

### Step 5: Run the Application


```bash
python app.py
```
