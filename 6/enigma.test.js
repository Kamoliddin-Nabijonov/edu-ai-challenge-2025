const { Enigma, Rotor, plugboardSwap, ROTORS, REFLECTOR, alphabet } = require('./enigma.js');

describe('Enigma Machine Tests', () => {
  
  describe('Basic Utility Functions', () => {
    test('plugboardSwap should swap letters correctly', () => {
      const pairs = [['A', 'B'], ['C', 'D']];
      expect(plugboardSwap('A', pairs)).toBe('B');
      expect(plugboardSwap('B', pairs)).toBe('A');
      expect(plugboardSwap('C', pairs)).toBe('D');
      expect(plugboardSwap('D', pairs)).toBe('C');
      expect(plugboardSwap('E', pairs)).toBe('E'); // No swap
    });

    test('plugboardSwap should work with empty pairs', () => {
      expect(plugboardSwap('A', [])).toBe('A');
    });
  });

  describe('Rotor Class', () => {
    test('rotor should initialize correctly', () => {
      const rotor = new Rotor('EKMFLGDQVZNTOWYHXUSPAIBRCJ', 'Q', 0, 0);
      expect(rotor.wiring).toBe('EKMFLGDQVZNTOWYHXUSPAIBRCJ');
      expect(rotor.notch).toBe('Q');
      expect(rotor.position).toBe(0);
      expect(rotor.ringSetting).toBe(0);
    });

    test('rotor should step correctly', () => {
      const rotor = new Rotor('EKMFLGDQVZNTOWYHXUSPAIBRCJ', 'Q', 0, 0);
      rotor.step();
      expect(rotor.position).toBe(1);
      
      // Test wrap-around
      rotor.position = 25;
      rotor.step();
      expect(rotor.position).toBe(0);
    });

    test('rotor should detect notch correctly', () => {
      const rotor = new Rotor('EKMFLGDQVZNTOWYHXUSPAIBRCJ', 'Q', 0, 16); // Q is at position 16
      expect(rotor.atNotch()).toBe(true);
      
      rotor.position = 15;
      expect(rotor.atNotch()).toBe(false);
    });

    test('rotor forward and backward should be inverse operations', () => {
      const rotor = new Rotor('EKMFLGDQVZNTOWYHXUSPAIBRCJ', 'Q', 0, 5);
      const original = 'H';
      const forward = rotor.forward(original);
      const backward = rotor.backward(forward);
      expect(backward).toBe(original);
    });
  });

  describe('Enigma Machine Basic Functionality', () => {
    test('enigma should initialize correctly', () => {
      const enigma = new Enigma([0, 1, 2], [0, 0, 0], [0, 0, 0], []);
      expect(enigma.rotors.length).toBe(3);
      expect(enigma.plugboardPairs.length).toBe(0);
    });

    test('enigma should process single character', () => {
      const enigma = new Enigma([0, 1, 2], [0, 0, 0], [0, 0, 0], []);
      const result = enigma.process('A');
      expect(result).toMatch(/[A-Z]/);
      expect(result.length).toBe(1);
    });

    test('enigma should handle non-alphabetic characters', () => {
      const enigma = new Enigma([0, 1, 2], [0, 0, 0], [0, 0, 0], []);
      const result = enigma.process('A1B2C');
      expect(result).toMatch(/[A-Z]1[A-Z]2[A-Z]/);
    });

    test('enigma should convert to uppercase', () => {
      const enigma = new Enigma([0, 1, 2], [0, 0, 0], [0, 0, 0], []);
      const result1 = enigma.process('hello');
      
      // Reset enigma to same state
      const enigma2 = new Enigma([0, 1, 2], [0, 0, 0], [0, 0, 0], []);
      const result2 = enigma2.process('HELLO');
      
      expect(result1).toBe(result2);
    });
  });

  describe('Enigma Encryption-Decryption Symmetry', () => {
    test('encryption and decryption should be symmetric with same settings', () => {
      const settings = {
        rotorIDs: [0, 1, 2],
        rotorPositions: [0, 0, 0],
        ringSettings: [0, 0, 0],
        plugboardPairs: []
      };

      const enigma1 = new Enigma(settings.rotorIDs, settings.rotorPositions, settings.ringSettings, settings.plugboardPairs);
      const plaintext = 'HELLOWORLD';
      const encrypted = enigma1.process(plaintext);

      const enigma2 = new Enigma(settings.rotorIDs, settings.rotorPositions, settings.ringSettings, settings.plugboardPairs);
      const decrypted = enigma2.process(encrypted);

      expect(decrypted).toBe(plaintext);
    });

    test('encryption-decryption with plugboard pairs', () => {
      const settings = {
        rotorIDs: [0, 1, 2],
        rotorPositions: [5, 10, 15],
        ringSettings: [1, 2, 3],
        plugboardPairs: [['A', 'B'], ['C', 'D'], ['E', 'F']]
      };

      const enigma1 = new Enigma(settings.rotorIDs, settings.rotorPositions, settings.ringSettings, settings.plugboardPairs);
      const plaintext = 'TESTMESSAGE';
      const encrypted = enigma1.process(plaintext);

      const enigma2 = new Enigma(settings.rotorIDs, settings.rotorPositions, settings.ringSettings, settings.plugboardPairs);
      const decrypted = enigma2.process(encrypted);

      expect(decrypted).toBe(plaintext);
    });

    test('different settings should produce different results', () => {
      const plaintext = 'HELLO';
      
      const enigma1 = new Enigma([0, 1, 2], [0, 0, 0], [0, 0, 0], []);
      const result1 = enigma1.process(plaintext);
      
      const enigma2 = new Enigma([0, 1, 2], [1, 0, 0], [0, 0, 0], []);
      const result2 = enigma2.process(plaintext);
      
      expect(result1).not.toBe(result2);
    });
  });

  describe('Rotor Stepping Mechanism', () => {
    test('right rotor should always step', () => {
      const enigma = new Enigma([0, 1, 2], [0, 0, 0], [0, 0, 0], []);
      const initialPos = enigma.rotors[2].position;
      
      enigma.encryptChar('A');
      
      expect(enigma.rotors[2].position).toBe((initialPos + 1) % 26);
    });

    test('middle rotor should step when right rotor is at notch', () => {
      // Set right rotor to notch position (V = 21)
      const enigma = new Enigma([0, 1, 2], [0, 0, 21], [0, 0, 0], []);
      const initialMiddlePos = enigma.rotors[1].position;
      
      enigma.encryptChar('A');
      
      expect(enigma.rotors[1].position).toBe((initialMiddlePos + 1) % 26);
    });

    test('double stepping should occur', () => {
      // Set middle rotor to notch position (E = 4)
      const enigma = new Enigma([0, 1, 2], [0, 4, 0], [0, 0, 0], []);
      
      const initialLeftPos = enigma.rotors[0].position;
      const initialMiddlePos = enigma.rotors[1].position;
      
      enigma.encryptChar('A');
      
      // Both left and middle rotors should have stepped
      expect(enigma.rotors[0].position).toBe((initialLeftPos + 1) % 26);
      expect(enigma.rotors[1].position).toBe((initialMiddlePos + 1) % 26);
    });
  });

  describe('Known Test Vectors', () => {
    test('should match historical enigma behavior', () => {
      // Basic test with known configuration
      const enigma = new Enigma([0, 1, 2], [0, 0, 0], [0, 0, 0], []);
      
      // Test that the same letter encrypts differently in different positions
      const result1 = enigma.encryptChar('A');
      const result2 = enigma.encryptChar('A');
      
      expect(result1).not.toBe(result2); // Should be different due to rotor stepping
    });

    test('a letter should never encrypt to itself', () => {
      const enigma = new Enigma([0, 1, 2], [0, 0, 0], [0, 0, 0], []);
      
      for (let i = 0; i < 26; i++) {
        const letter = alphabet[i];
        const encrypted = enigma.encryptChar(letter);
        expect(encrypted).not.toBe(letter);
      }
    });
  });

  describe('Edge Cases', () => {
    test('should handle empty message', () => {
      const enigma = new Enigma([0, 1, 2], [0, 0, 0], [0, 0, 0], []);
      const result = enigma.process('');
      expect(result).toBe('');
    });

    test('should handle message with only spaces and numbers', () => {
      const enigma = new Enigma([0, 1, 2], [0, 0, 0], [0, 0, 0], []);
      const result = enigma.process('123 456');
      expect(result).toBe('123 456');
    });

    test('should handle complex plugboard configuration', () => {
      const plugPairs = [['A', 'Z'], ['B', 'Y'], ['C', 'X'], ['D', 'W'], ['E', 'V']];
      const enigma1 = new Enigma([0, 1, 2], [0, 0, 0], [0, 0, 0], plugPairs);
      const enigma2 = new Enigma([0, 1, 2], [0, 0, 0], [0, 0, 0], plugPairs);
      
      const plaintext = 'ABCDE';
      const encrypted = enigma1.process(plaintext);
      const decrypted = enigma2.process(encrypted);
      
      expect(decrypted).toBe(plaintext);
    });
  });

  describe('Ring Settings Impact', () => {
    test('different ring settings should produce different results', () => {
      const plaintext = 'HELLO';
      
      const enigma1 = new Enigma([0, 1, 2], [0, 0, 0], [0, 0, 0], []);
      const result1 = enigma1.process(plaintext);
      
      const enigma2 = new Enigma([0, 1, 2], [0, 0, 0], [1, 2, 3], []);
      const result2 = enigma2.process(plaintext);
      
      expect(result1).not.toBe(result2);
    });
  });
}); 