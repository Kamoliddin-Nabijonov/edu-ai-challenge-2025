<img src="enigma.png" alt="Broken Enigma Machine" width="300"/>

# Enigma Machine - Fixed Implementation

A corrected implementation of the classic Enigma cipher machine with comprehensive testing.

## Overview

This implementation includes:
- Multiple rotors with configurable wiring and stepping
- Plugboard for letter swaps  
- Reflector logic
- Proper double-stepping mechanism
- CLI interface for encryption/decryption
- Comprehensive unit tests with >90% coverage

## Installation

1. Make sure you have Node.js installed (version 14 or higher)
2. Navigate to the project directory
3. Install dependencies:

```bash
npm install
```

## Running the Application

### Interactive CLI Mode

To run the Enigma machine interactively:

```bash
npm start
```

or

```bash
node enigma.js
```

You will be prompted to enter:
1. **Message**: The text to encrypt/decrypt
2. **Rotor positions**: Three numbers (0-25) representing initial rotor positions
3. **Ring settings**: Three numbers (0-25) for rotor ring settings  
4. **Plugboard pairs**: Letter pairs for plugboard swaps (e.g., "AB CD EF")

### Example Usage

```
Enter message: HELLOWORLD
Rotor positions (e.g. 0 0 0): 0 0 0
Ring settings (e.g. 0 0 0): 0 0 0
Plugboard pairs (e.g. AB CD): AB CD EF
Output: QWERTYUIOP
```

To decrypt, use the same settings with the encrypted message:

```
Enter message: QWERTYUIOP
Rotor positions (e.g. 0 0 0): 0 0 0
Ring settings (e.g. 0 0 0): 0 0 0
Plugboard pairs (e.g. AB CD): AB CD EF
Output: HELLOWORLD
```

## Configuration Options

### Rotor Positions
- Three integers from 0-25
- Represents the initial position of each rotor
- Example: `5 10 15`

### Ring Settings  
- Three integers from 0-25
- Adjusts the internal wiring offset of each rotor
- Example: `1 2 3`

### Plugboard Pairs
- Letter pairs separated by spaces
- Each pair swaps two letters
- Maximum 10 pairs (20 letters)
- Example: `AB CD EF GH IJ`

## Testing

### Run All Tests

```bash
npm test
```

### Run Tests with Coverage Report

```bash
npm run test:coverage
```

This will generate:
- Console coverage report
- HTML coverage report in `coverage/` directory
- LCOV coverage data

### Coverage Requirements

The test suite maintains:
- **>90% Line Coverage**
- **>85% Branch Coverage**  
- **>90% Function Coverage**
- **>90% Statement Coverage**

## Test Categories

### Basic Functionality Tests
- Rotor initialization and stepping
- Plugboard swapping
- Character encryption/decryption

### Encryption-Decryption Symmetry Tests
- Verify that encrypt(decrypt(message)) === message
- Test with various configurations
- Test with and without plugboard pairs

### Rotor Mechanism Tests
- Proper rotor stepping behavior
- Double-stepping mechanism verification
- Notch detection

### Edge Case Tests
- Empty messages
- Non-alphabetic characters
- Complex plugboard configurations
- Boundary conditions

### Historical Accuracy Tests
- Letters never encrypt to themselves
- Rotor advancement follows Enigma specifications
- Plugboard behavior matches historical implementation

## Code Structure

```
6/
├── enigma.js           # Main Enigma implementation (fixed)
├── enigma.test.js      # Comprehensive unit tests
├── package.json        # Dependencies and scripts
├── fix.md             # Detailed bug fix explanation
├── README.md          # This file
└── coverage/          # Generated coverage reports
```

## Key Classes and Functions

### `Enigma`
Main class representing the Enigma machine
- `constructor(rotorIDs, rotorPositions, ringSettings, plugboardPairs)`
- `process(text)` - Encrypt/decrypt a full message
- `encryptChar(char)` - Encrypt/decrypt a single character

### `Rotor`
Represents individual rotors
- `step()` - Advance rotor position
- `forward(char)` - Encrypt character in forward direction
- `backward(char)` - Encrypt character in backward direction
- `atNotch()` - Check if rotor is at stepping notch

### `plugboardSwap`
Utility function for plugboard letter swapping

## Bug Fixes

This implementation fixes two critical bugs from the original:

1. **Missing Final Plugboard Swap**: Added the required second plugboard operation after the return path through rotors

2. **Incorrect Double-Stepping**: Fixed the rotor stepping mechanism to properly implement Enigma's characteristic double-stepping behavior

See `fix.md` for detailed technical explanation of the bugs and fixes.

## Verification Examples

### Basic Encryption/Decryption
```javascript
const { Enigma } = require('./enigma.js');

// Create Enigma with basic settings
const enigma1 = new Enigma([0, 1, 2], [0, 0, 0], [0, 0, 0], []);
const encrypted = enigma1.process('HELLOWORLD');

// Create second Enigma with same settings for decryption
const enigma2 = new Enigma([0, 1, 2], [0, 0, 0], [0, 0, 0], []);
const decrypted = enigma2.process(encrypted);

console.log(decrypted); // Should output: HELLOWORLD
```

### With Plugboard Configuration
```javascript
const plugPairs = [['A', 'B'], ['C', 'D'], ['E', 'F']];
const enigma1 = new Enigma([0, 1, 2], [5, 10, 15], [1, 2, 3], plugPairs);
const encrypted = enigma1.process('TESTMESSAGE');

const enigma2 = new Enigma([0, 1, 2], [5, 10, 15], [1, 2, 3], plugPairs);
const decrypted = enigma2.process(encrypted);

console.log(decrypted); // Should output: TESTMESSAGE
```

## Historical Notes

This implementation simulates the behavior of the German Enigma I machine used during World War II, including:
- Three-rotor configuration (Rotors I, II, III)
- Reflector B wiring
- Plugboard (Steckerbrett) capability
- Double-stepping anomaly
- Ring settings (Ringstellung)

## License

MIT License - Feel free to use for educational purposes.
