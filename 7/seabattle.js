// Game configuration
const BOARD_SIZE = 10;
const NUM_SHIPS = 3;
const SHIP_LENGTH = 3;

class Ship {
  constructor(locations = []) {
    this.locations = locations;
    this.hits = new Array(SHIP_LENGTH).fill('');
  }

  isSunk() {
    return this.hits.every(hit => hit === 'hit');
  }
}

class Board {
  constructor() {
    this.grid = Array(BOARD_SIZE).fill().map(() => Array(BOARD_SIZE).fill('~'));
  }

  placeShip(row, col, isHorizontal) {
    const positions = [];
    for (let i = 0; i < SHIP_LENGTH; i++) {
      const pos = {
        row: isHorizontal ? row : row + i,
        col: isHorizontal ? col + i : col
      };
      if (!this.isValidPosition(pos.row, pos.col)) return null;
      if (this.grid[pos.row][pos.col] !== '~') return null;
      positions.push(`${pos.row}${pos.col}`);
    }
    
    positions.forEach(pos => {
      const [r, c] = pos.split('').map(Number);
      this.grid[r][c] = 'S';
    });
    
    return positions;
  }

  isValidPosition(row, col) {
    return row >= 0 && row < BOARD_SIZE && col >= 0 && col < BOARD_SIZE;
  }

  markHit(row, col) {
    this.grid[row][col] = 'X';
  }

  markMiss(row, col) {
    this.grid[row][col] = 'O';
  }
}

class Player {
  constructor(isComputer = false) {
    this.board = new Board();
    this.ships = [];
    this.guesses = new Set();
    this.numShips = NUM_SHIPS;
    this.isComputer = isComputer;
    this.targetQueue = [];
    this.mode = 'hunt';
  }

  placeShipsRandomly() {
    let placedShips = 0;
    while (placedShips < NUM_SHIPS) {
      const isHorizontal = Math.random() < 0.5;
      const maxRow = isHorizontal ? BOARD_SIZE : BOARD_SIZE - SHIP_LENGTH + 1;
      const maxCol = isHorizontal ? BOARD_SIZE - SHIP_LENGTH + 1 : BOARD_SIZE;
      
      const row = Math.floor(Math.random() * maxRow);
      const col = Math.floor(Math.random() * maxCol);
      
      const shipLocations = this.board.placeShip(row, col, isHorizontal);
      if (shipLocations) {
        this.ships.push(new Ship(shipLocations));
        placedShips++;
      }
    }
  }

  processGuess(row, col) {
    const guessStr = `${row}${col}`;
    if (this.guesses.has(guessStr)) return { valid: false, message: 'Location already guessed' };
    
    this.guesses.add(guessStr);
    
    for (const ship of this.ships) {
      const hitIndex = ship.locations.indexOf(guessStr);
      if (hitIndex >= 0) {
        ship.hits[hitIndex] = 'hit';
        this.board.markHit(row, col);
        
        if (ship.isSunk()) {
          this.numShips--;
          return { valid: true, hit: true, sunk: true };
        }
        return { valid: true, hit: true, sunk: false };
      }
    }
    
    this.board.markMiss(row, col);
    return { valid: true, hit: false, sunk: false };
  }

  makeComputerGuess() {
    if (!this.isComputer) return null;

    let guessRow, guessCol, guessStr;
    
    do {
      if (this.mode === 'target' && this.targetQueue.length > 0) {
        guessStr = this.targetQueue.shift();
        [guessRow, guessCol] = guessStr.split('').map(Number);
      } else {
        guessRow = Math.floor(Math.random() * BOARD_SIZE);
        guessCol = Math.floor(Math.random() * BOARD_SIZE);
        guessStr = `${guessRow}${guessCol}`;
      }
    } while (this.guesses.has(guessStr));

    return { row: guessRow, col: guessCol };
  }

  updateTargetQueue(row, col, wasHit) {
    if (!this.isComputer) return;

    if (wasHit) {
      this.mode = 'target';
      const adjacent = [
        { row: row - 1, col },
        { row: row + 1, col },
        { row, col: col - 1 },
        { row, col: col + 1 }
      ];

      for (const pos of adjacent) {
        if (this.board.isValidPosition(pos.row, pos.col)) {
          const posStr = `${pos.row}${pos.col}`;
          if (!this.guesses.has(posStr) && !this.targetQueue.includes(posStr)) {
            this.targetQueue.push(posStr);
          }
        }
      }
    } else if (this.targetQueue.length === 0) {
      this.mode = 'hunt';
    }
  }
}

class Game {
  constructor() {
    this.player = new Player();
    this.computer = new Player(true);
    this.readline = require('readline').createInterface({
      input: process.stdin,
      output: process.stdout
    });
  }

  async initialize() {
    this.player.placeShipsRandomly();
    this.computer.placeShipsRandomly();
    console.log("\nLet's play Sea Battle!");
    console.log(`Try to sink the ${NUM_SHIPS} enemy ships.`);
    await this.gameLoop();
  }

  printBoards() {
    console.log('\n   --- OPPONENT BOARD ---          --- YOUR BOARD ---');
    const header = '  ' + [...Array(BOARD_SIZE)].map((_, i) => i).join(' ');
    console.log(header + '     ' + header);

    for (let i = 0; i < BOARD_SIZE; i++) {
      let rowStr = `${i} ${this.computer.board.grid[i].map(cell => cell === 'S' ? '~' : cell).join(' ')}`;
      rowStr += `    ${i} ${this.player.board.grid[i].join(' ')}`;
      console.log(rowStr);
    }
    console.log('\n');
  }

  async getPlayerGuess() {
    return new Promise(resolve => {
      this.readline.question('Enter your guess (e.g., 00): ', answer => {
        if (!answer || answer.length !== 2) {
          console.log('Please enter exactly two digits (e.g., 00).');
          resolve(null);
          return;
        }

        const [row, col] = answer.split('').map(Number);
        if (!this.computer.board.isValidPosition(row, col)) {
          console.log(`Please enter valid coordinates between 0 and ${BOARD_SIZE - 1}.`);
          resolve(null);
          return;
        }

        resolve({ row, col });
      });
    });
  }

  async gameLoop() {
    while (true) {
      this.printBoards();

      // Player's turn
      const playerGuess = await this.getPlayerGuess();
      if (!playerGuess) continue;

      const result = this.computer.processGuess(playerGuess.row, playerGuess.col);
      if (!result.valid) {
        console.log(result.message);
        continue;
      }

      console.log(result.hit ? 'PLAYER HIT!' : 'PLAYER MISS.');
      if (result.sunk) {
        console.log('You sunk an enemy battleship!');
        if (this.computer.numShips === 0) {
          console.log('\n*** CONGRATULATIONS! You sunk all enemy battleships! ***');
          this.printBoards();
          break;
        }
      }

      // Computer's turn
      const computerGuess = this.computer.makeComputerGuess();
      const computerResult = this.player.processGuess(computerGuess.row, computerGuess.col);
      
      console.log(`\nCPU guesses: ${computerGuess.row}${computerGuess.col}`);
      console.log(computerResult.hit ? 'CPU HIT!' : 'CPU MISS.');
      
      this.computer.updateTargetQueue(computerGuess.row, computerGuess.col, computerResult.hit);

      if (computerResult.sunk) {
        console.log('CPU sunk your battleship!');
        if (this.player.numShips === 0) {
          console.log('\n*** GAME OVER! The CPU sunk all your battleships! ***');
          this.printBoards();
          break;
        }
      }
    }

    this.readline.close();
  }
}

// Export classes for testing
if (typeof module !== 'undefined' && module.exports) {
  module.exports = { Ship, Board, Player, Game };
}

// Start the game only if running directly (not in test environment)
if (require.main === module) {
  const game = new Game();
  game.initialize();
}
