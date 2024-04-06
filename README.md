# 📦 Product and User API Endpoints Documentation

## 🌟 Overview

This documentation provides detailed information about the API endpoints for managing products and users using FastAPI. The endpoints allow users to perform CRUD operations (Create, Read, Update, Delete) on product data and user authentication.

### Requirements
Before running the application, make sure to install all the required dependencies by executing the following command:

```bash
pip install -r requirements.txt
```

### Running the Application
To run this application, use the following command:

```bash
python -m uvicorn main:app --reload
```

---

## 🛒 Endpoints

### 📋 Product Endpoints

#### Get All Products

- **URL:** `/product/`
- **Method:** GET
- **Description:** Retrieve a list of all products.
- **Parameters:**
  - None
- **Response:**
  - Status Code: 200 OK
  - Content: JSON array of product objects
- **Example:**
  ```json
  [
    {
      "id": 1,
      "name": "Product 1",
      "description": "Description of Product 1",
      "price": 10.99
    },
    {
      "id": 2,
      "name": "Product 2",
      "description": "Description of Product 2",
      "price": 20.99
    }
  ]
  ```

#### Get Product by ID

- **URL:** `/product/{product_id}`
- **Method:** GET
- **Description:** Retrieve a product by its ID.
- **Parameters:**
  - `product_id`: ID of the product to retrieve (integer)
- **Response:**
  - Status Code: 200 OK
  - Content: JSON object representing the product
- **Example:**
  ```json
  {
    "id": 1,
    "name": "Product 1",
    "description": "Description of Product 1",
    "price": 10.99
  }
  ```

#### Create Product

- **URL:** `/product/`
- **Method:** POST
- **Description:** Create a new product.
- **Parameters:**
  - JSON object representing the product data (name, description, price)
- **Response:**
  - Status Code: 201 Created
  - Content: JSON object representing the created product
- **Example Request Body:**
  ```json
  {
    "name": "New Product",
    "description": "Description of New Product",
    "price": 15.99
  }
  ```
- **Example Response:**
  ```json
  {
    "id": 3,
    "name": "New Product",
    "description": "Description of New Product",
    "price": 15.99
  }
  ```

#### Update Product

- **URL:** `/product/{product_id}`
- **Method:** PUT
- **Description:** Update an existing product.
- **Parameters:**
  - `product_id`: ID of the product to update (integer)
  - JSON object representing the updated product data (name, description, price)
- **Response:**
  - Status Code: 204 No Content
- **Example Request Body:**
  ```json
  {
    "name": "Updated Product",
    "description": "Updated Description",
    "price": 19.99
  }
  ```

#### Delete Product

- **URL:** `/product/{product_id}`
- **Method:** DELETE
- **Description:** Delete a product by its ID.
- **Parameters:**
  - `product_id`: ID of the product to delete (integer)
- **Response:**
  - Status Code: 204 No Content

### 🔐 User Authentication Endpoints

#### Register User

- **URL:** `/auth/register`
- **Method:** POST
- **Description:** Register a new user.
- **Parameters:**
  - JSON object representing the user data (username, email, password)
- **Response:**
  - Status Code: 201 Created
  - Content: JSON object representing the created user
- **Example Request Body:**
  ```json
  {
    "username": "user1",
    "email": "user1@example.com",
    "password": "password123"
  }
  ```
- **Example Response:**
  ```json
  {
    "id": 1,
    "username": "user1",
    "email": "user1@example.com"
  }
  ```

#### Login User

- **URL:** `/auth/login`
- **Method:** POST
- **Description:** Authenticate and login a user.
- **Parameters:**
  - JSON object representing the login credentials (username, password)
- **Response:**
  - Status Code: 200 OK
  - Content: JSON object containing access token
- **Example Request Body:**
  ```json
  {
    "username": "user1",
    "password": "password123"
  }
  ```
- **Example Response:**
  ```json


  {
    "access_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
    "token_type": "bearer"
  }
  ```

---
