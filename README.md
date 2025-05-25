# A2A LangGraph Project

## installation uv

https://docs.astral.sh/uv/getting-started/installation/

## Getting started

1. Go to langGraphProject:

   ```bash
   cd langgraphproject
   ```

2. Create venv

   ```bash
   uv venv
   ```

3. Activate venv

   ```bash
   source .venv/bin/activate
   ```

4. Download libaray:

```bash
    uv sync
```

5. Create an environment file with your API key::

```bash
echo "GEMINI_API_KEY=your_api_key_here" > .env
```

6. Start the server

   ```bash
   uv run .
   ```

7. Run the test client

   ```bash
   uv run test_client.py
   ```
