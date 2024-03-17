# Chess Moves App

This Flask application provides endpoints to find valid moves for different chess pieces such as Knight, Bishop, Rook, and Queen. It takes a JSON payload containing the positions of the chess pieces and returns the valid moves for each piece.

## Running the App with Docker

To run this application using Docker, follow these steps:

1. **Build the Docker image:**

```bash
docker build -t chess-app .
```

2. **Run the Docker container:**

```bash
docker run -p 6000:6000 chess-app
```

The application will now be accessible at [http://localhost:6000](http://localhost:6000).

## Example Endpoint

You can use the following example to test the `/chess/rook` endpoint:

**Endpoint:** `http://127.0.0.1:6000/chess/rook`

**Request Body:**

```json
{
  "positions": {
    "Queen": "A5",
    "Bishop": "G8",
    "Rook": "H5",
    "Knight": "G4"
  }
}
```

This will return the valid moves for the Rook piece based on the provided positions.
