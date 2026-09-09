# Connect Four AI

The project focuses on the Connect Four game and comparison of two AI agents. Both agents use the Min-Max algorithm with alpha-beta pruning, but use different evaluation functions:

* **Heuristic Agent** – uses a heuristic evaluation function
* **Neural Agent** – uses a neural network

## Setup

Python 3 is required.

Install the required packages:

```bash
pip install -r requirements.txt
```

## Playing Against the AI

The game can be played against the Heuristic AI agent through the terminal:

```bash
python -m ui.play_vs_ai
```

## Agent Comparison

The two agents can be compared using the benchmark:

```bash
python -m evaluation.benchmark
```

The benchmark measures the number of wins, draws, average number of moves, and average time per move.

Different Min-Max search depths can be tested using:

```bash
python -m evaluation.depth_test
```

The results of the tests are saved in the `data` folder.

## Project Structure

```text
connect4-ai/
├── game/          # Game board and rules
├── search/        # Min-Max and heuristic evaluation
├── neural/        # Neural network
├── evaluation/    # Benchmarks and tests
├── ui/            # Game against the AI
├── data/          # Datasets and trained models
├── report/        # Results and plots
├── requirements.txt
└── README.md
```