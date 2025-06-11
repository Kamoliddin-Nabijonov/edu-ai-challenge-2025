# Sea Battle Game

A modernized implementation of the classic Sea Battle (Battleship) game in Node.js.

## Features

- 10x10 game board
- 3 ships of length 3 for each player
- Turn-based gameplay
- Smart CPU opponent with hunt/target strategy
- Command-line interface
- Modern ES6+ implementation
- Comprehensive test coverage

## Game Rules

1. Each player has a 10x10 board where they place their ships
2. Ships are placed randomly at the start of the game
3. Players take turns guessing coordinates to attack (e.g., "00", "34", "98")
4. Hits are marked with 'X', misses with 'O'
5. The game ends when all ships of one player are sunk

## Board Display

- `~` : Empty water
- `S` : Ship (only visible on player's board)
- `X` : Hit
- `O` : Miss

## Installation

```bash
npm install
```

## Running the Game

```bash
npm start
```

## Running Tests

```bash
npm test
```

## Code Structure

The game is implemented using modern JavaScript features and follows object-oriented principles:

- `Ship`: Represents a ship with its locations and hit status
- `Board`: Manages the game board and ship placement
- `Player`: Handles player/CPU logic and game moves
- `Game`: Controls the game flow and user interaction

## CPU Strategy

The CPU uses two modes of operation:

1. Hunt Mode: Random guessing to find ships
2. Target Mode: Once a hit is made, systematically check adjacent squares

## Test Coverage

The codebase includes comprehensive unit tests covering:

- Ship creation and status
- Board management and ship placement
- Player actions and game logic
- CPU strategy and decision making 