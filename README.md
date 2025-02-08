# Morph Sample AI Apps / Data Apps

Welcome to the **Morph Sample AI Apps / Data Apps Collection** repository!

This repository is dedicated to showcasing a variety of sample applications built with the [Morph](https://github.com/morph-data/morph).

Whether you are new to Morph or an experienced user, these examples will help you understand how to leverage the framework to build powerful and efficient applications.

---

## Table of Contents

- [Overview](#overview)
- [AI Apps / Data Apps](#ai-apps-data-apps)
  - [RBAC Langchain App](#rbac-langchain-app)
  - [SQL Agent App](#sql-agent-app)
---

## Overview

The Morph framework provides a flexible and powerful foundation for building AI Apps and Data Apps. This repository contains a curated set of sample applications that demonstrate various features and use cases of Morph.

---

## AI Apps / Data Apps

### **RBAC Langchain App**
- **Description:**

    This app demonstrates a Role-Based Access Control (RBAC) system implemented using LangChain for AI workflow and Morph for frontend and RBAC.

    It allows only users with the `admin` role to access AI chat created by LangChain.

- **Installation & Usage:**
  Please set OPENAI_API_KEY in the `.env` file.
- **Files**
    - [rbac_langchain_app/](./rbac_langchain_app/)
- **Related Articles:**
  - [Create a chat app using Langchain](https://www.morph-data.io/tools/snippets/item/create-a-chat-app-using-langchain)

---

### **SQL Agent App**
- **Description:**

    SQL Agent answers the user's question. It generates a SQL query from the user's question and executes the query to retrieve the result.

    This sample app uses LangChain and DuckDB.

- **Installation & Usage:**
    - Please set OPENAI_API_KEY in the `.env` file.
- **Files**
    - [sql_agent_app/](./sql_agent_app/)
- **Related Articles:**
  - [Text to SQL: makes it easy to communicate with your database](https://www.morph-data.io/tools/snippets/item/text-to-sql-makes-it-easy-to-communicate-with-your-database)
---
