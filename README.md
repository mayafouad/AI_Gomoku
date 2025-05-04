# AI Gomoku Game Solver

## 📌 Overview

This project implements a **Gomoku (Five in a Row)** game solver using the **Minimax** and **Alpha-Beta Pruning** algorithms. Gomoku is a strategic board game where two players take turns placing their marks on a grid, aiming to align five of their symbols in a row — horizontally, vertically, or diagonally — before their opponent does.

## 🎮 Game Modes

1. **Human vs AI**

   * A human player competes against an AI opponent.
   * The AI uses the **Minimax algorithm** to choose the best move.

2. **AI vs AI**

   * Two AI players compete:

     * One uses the **Minimax algorithm**.
     * The other uses **Alpha-Beta Pruning**, an optimized version of Minimax.

## 🧠 Algorithms Used

* **Minimax Algorithm**: A recursive strategy that explores all possible moves to find the optimal one.
* **Alpha-Beta Pruning**: Enhances Minimax by eliminating branches that don’t affect the final decision, improving performance.
* **Depth-limited Search**: Both algorithms use a depth limit to manage performance on larger boards.


