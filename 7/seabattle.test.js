const { Ship, Board, Player } = require('./seabattle');

describe('Ship', () => {
  let ship;

  beforeEach(() => {
    ship = new Ship(['00', '01', '02']);
  });

  test('should be created with correct locations', () => {
    expect(ship.locations).toEqual(['00', '01', '02']);
    expect(ship.hits).toEqual(['', '', '']);
  });

  test('should not be sunk initially', () => {
    expect(ship.isSunk()).toBe(false);
  });

  test('should be sunk when all positions are hit', () => {
    ship.hits = ['hit', 'hit', 'hit'];
    expect(ship.isSunk()).toBe(true);
  });
});

describe('Board', () => {
  let board;

  beforeEach(() => {
    board = new Board();
  });

  test('should create empty board', () => {
    expect(board.grid.length).toBe(10);
    expect(board.grid[0].length).toBe(10);
    expect(board.grid[0][0]).toBe('~');
  });

  test('should validate positions correctly', () => {
    expect(board.isValidPosition(0, 0)).toBe(true);
    expect(board.isValidPosition(9, 9)).toBe(true);
    expect(board.isValidPosition(-1, 0)).toBe(false);
    expect(board.isValidPosition(0, 10)).toBe(false);
  });

  test('should place ship horizontally', () => {
    const positions = board.placeShip(0, 0, true);
    expect(positions).toEqual(['00', '01', '02']);
    expect(board.grid[0][0]).toBe('S');
    expect(board.grid[0][1]).toBe('S');
    expect(board.grid[0][2]).toBe('S');
  });

  test('should place ship vertically', () => {
    const positions = board.placeShip(0, 0, false);
    expect(positions).toEqual(['00', '10', '20']);
    expect(board.grid[0][0]).toBe('S');
    expect(board.grid[1][0]).toBe('S');
    expect(board.grid[2][0]).toBe('S');
  });

  test('should not place ship outside board', () => {
    const positions = board.placeShip(8, 8, true);
    expect(positions).toBeNull();
  });

  test('should not place ship on occupied position', () => {
    board.placeShip(0, 0, true);
    const positions = board.placeShip(0, 1, false);
    expect(positions).toBeNull();
  });

  test('should mark hits and misses', () => {
    board.markHit(0, 0);
    board.markMiss(1, 1);
    expect(board.grid[0][0]).toBe('X');
    expect(board.grid[1][1]).toBe('O');
  });
});

describe('Player', () => {
  let player;
  let computer;

  beforeEach(() => {
    player = new Player();
    computer = new Player(true);
  });

  test('should initialize correctly', () => {
    expect(player.ships).toEqual([]);
    expect(player.numShips).toBe(3);
    expect(player.guesses.size).toBe(0);
    expect(player.isComputer).toBe(false);
    expect(computer.isComputer).toBe(true);
  });

  test('should place ships randomly', () => {
    player.placeShipsRandomly();
    expect(player.ships.length).toBe(3);
    expect(player.ships[0].locations.length).toBe(3);
  });

  test('should process valid guess', () => {
    const shipLocations = player.board.placeShip(0, 0, true);
    const ship = new Ship(shipLocations);
    player.ships.push(ship);
    const result = player.processGuess(0, 0);
    expect(result.valid).toBe(true);
    expect(result.hit).toBe(true);
    expect(result.sunk).toBe(false);
  });

  test('should process miss', () => {
    const shipLocations = player.board.placeShip(0, 0, true);
    const ship = new Ship(shipLocations);
    player.ships.push(ship);
    const result = player.processGuess(1, 1);
    expect(result.valid).toBe(true);
    expect(result.hit).toBe(false);
    expect(result.sunk).toBe(false);
  });

  test('should detect sunk ship', () => {
    const shipLocations = player.board.placeShip(0, 0, true);
    const ship = new Ship(shipLocations);
    player.ships.push(ship);
    player.processGuess(0, 0);
    player.processGuess(0, 1);
    const result = player.processGuess(0, 2);
    expect(result.sunk).toBe(true);
    expect(player.numShips).toBe(2);
  });

  test('should not allow repeated guesses', () => {
    player.processGuess(0, 0);
    const result = player.processGuess(0, 0);
    expect(result.valid).toBe(false);
  });

  test('computer should make valid guesses', () => {
    const guess = computer.makeComputerGuess();
    expect(guess).toHaveProperty('row');
    expect(guess).toHaveProperty('col');
    expect(computer.board.isValidPosition(guess.row, guess.col)).toBe(true);
  });

  test('computer should update target queue on hit', () => {
    computer.updateTargetQueue(5, 5, true);
    expect(computer.mode).toBe('target');
    expect(computer.targetQueue.length).toBe(4);
  });

  test('computer should switch to hunt mode when target queue is empty', () => {
    computer.mode = 'target';
    computer.updateTargetQueue(5, 5, false);
    expect(computer.mode).toBe('hunt');
  });
}); 