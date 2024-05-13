# Blog API

This API allows users to create, read, update, and delete blog posts, as well as add comments, like, and dislike posts. It utilizes FastAPI for building the web service, MongoDB for data storage, and Pydantic for data validation.

## Installation

1. Clone the repository:

    ```bash
    git clone <repository-url>
    ```

2. Install dependencies:

    ```bash
    pip install -r requirements.txt
    ```

3. Set up environment variables by creating a `.env` file in the root directory with the following variables:

    ```plaintext
    ATLAS_URL=<your-mongodb-atlas-url>
    DB_NAME=<your-database-name>
    COLLECTION_NAME=<your-collection-name>
    ```

## Usage

1. Run the FastAPI application using Uvicorn:

    ```bash
    uvicorn main:app --reload
    ```

2. The API will be available at [http://localhost:8000](http://localhost:8000).

3. Access the API documentation [here](https://documenter.getpostman.com/view/33074643/2sA3JNazvM).

## API Endpoints

### Create Post

- **URL:** `/posts/`
- **Method:** `POST`
- **Request Body:**
    ```json
    {
      "title": "string",
      "content": "string",
      "author": "string"
    }
    ```
- **Response:**
    ```json
    {
      "message": "Post created successfully",
      "post_id": "string"
    }
    ```

### Read Posts

- **URL:** `/posts/`
- **Method:** `GET`
- **Response:** Array of post objects.

### Update Post

- **URL:** `/posts/{post_id}`
- **Method:** `PUT`
- **Request Body:** Same as create post.
- **Response:**
    ```json
    {
      "message": "Post updated successfully"
    }
    ```

### Delete Post

- **URL:** `/posts/{post_id}`
- **Method:** `DELETE`
- **Response:**
    ```json
    {
      "message": "Post deleted successfully"
    }
    ```

### Create Comment

- **URL:** `/posts/{post_id}/comments/`
- **Method:** `PUT`
- **Request Body:**
    ```json
    {
      "text": "string",
      "author": "string"
    }
    ```
- **Response:**
    ```json
    {
      "message": "Comment added successfully"
    }
    ```

### Like Post

- **URL:** `/posts/{post_id}/like/`
- **Method:** `PUT`
- **Response:**
    ```json
    {
      "message": "Post liked successfully"
    }
    ```

### Dislike Post

- **URL:** `/posts/{post_id}/dislike/`
- **Method:** `PUT`
- **Response:**
    ```json
    {
      "message": "Post disliked successfully"
    }
    ```

## Data Models

### Post

- **Fields:**
  - `title`: Title of the post (string)
  - `content`: Content of the post (string)
  - `author`: Author of the post (string)
  - `comments`: List of comments associated with the post (array of Comment objects)
  - `likes`: Number of likes for the post (integer)
  - `dislikes`: Number of dislikes for the post (integer)

### Comment

- **Fields:**
  - `text`: Text content of the comment (string)
  - `author`: Author of the comment (string)

## Additional Notes

- Ensure MongoDB is running and accessible from the provided URL.
- All POST and PUT requests require a JSON body.
