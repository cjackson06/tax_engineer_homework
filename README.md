# Installation

## uv

```bash
uv sync
```

## pip with uv

1. Create a virtual environment

```bash
    python3 -m venv .venv
```

2. Activate the virtual environment
   Linux/Mac

```bash
    source .venv/bin/activate
```

Windows

```bash
    .venv\Scripts\activate
```

3. Install packages

```bash
    pip install uv
    uv sync
```

## pip only

1. Create a virtual environment

```bash
    python3 -m venv .venv
```

2. Activate the virtual environment
   Linux/Mac

```bash
    source .venv/bin/activate
```

Windows

```bash
    .venv\Scripts\activate
```

3. Install packages

```bash
    pip install -r r.txt
```

# Running the Game

## Options

```
  --auto             Prevent request for user action, move game along automatically
  --output [OUTPUT]  Auto play game and output the game results to a log file
  --suit-up          run game with "suit up" house rule
```

## With uv

```bash
    uv run war_game.py [--auto] [--output [OUTPUT]] [--suit-up]
```

## Without uv

1. Activate virtual environment

```bash
war_game.py [--auto] [--output [OUTPUT]] [--suit-up]
```

# Running Tests

Tests were developed with pytest library. The easiest way to run them is:

```bash
uvx --with-requirements pyproject.toml pytest tests.py
```

Otherwise you can follow the steps above to create a virtual environment and install the required packages. Afterward, run pytest as shown above.

```
pytest tests.py
```
