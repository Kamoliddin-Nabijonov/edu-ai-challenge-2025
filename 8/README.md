# Python Validation Library

A simple but robust validation library for Python that provides type-safe validator functions for primitive and complex data types.

## Features

- ✅ **Type-safe validators** for strings, numbers, booleans, arrays, and objects
- ✅ **Chainable validation rules** with fluent API
- ✅ **Optional field support** with `.optional()` method
- ✅ **Custom error messages** with `.with_message()` method
- ✅ **Nested object validation** for complex data structures
- ✅ **Regex pattern matching** for string validation
- ✅ **Length constraints** for strings and arrays
- ✅ **Range validation** for numbers
- ✅ **Comprehensive error reporting** with detailed messages

## Installation

No external dependencies required! Just download the `validator.py` file and import it in your project.

```python
from validator import Schema, ValidationError
```

## Quick Start

### Basic Usage

```python
from validator import Schema

# String validation
name_validator = Schema.string().min_length(2).max_length(50)
result = name_validator.validate("John")
print(result.is_valid)  # True

# Number validation
age_validator = Schema.number().min(0).max(150)
result = age_validator.validate(25)
print(result.is_valid)  # True

# Boolean validation
active_validator = Schema.boolean()
result = active_validator.validate(True)
print(result.is_valid)  # True
```

### Email Validation Example

```python
email_validator = Schema.string().pattern(r'^[^\s@]+@[^\s@]+\.[^\s@]+$')

result = email_validator.validate("user@example.com")
print(result.is_valid)  # True

result = email_validator.validate("invalid-email")
print(result.is_valid)  # False
print(result.errors)  # ['String does not match required pattern']
```

### Array Validation Example

```python
# Array of strings with length constraints
tags_validator = Schema.array(Schema.string()).min_length(1).max_length(5)

result = tags_validator.validate(["python", "javascript", "web"])
print(result.is_valid)  # True

result = tags_validator.validate([])  # Too short
print(result.is_valid)  # False
```

### Complex Object Validation

```python
# Define nested schemas
address_schema = {
    "street": Schema.string().min_length(1),
    "city": Schema.string().min_length(1),
    "postal_code": Schema.string().pattern(r'^\d{5}$'),
    "country": Schema.string().min_length(2)
}

user_schema = {
    "name": Schema.string().min_length(2).max_length(50),
    "email": Schema.string().pattern(r'^[^\s@]+@[^\s@]+\.[^\s@]+$'),
    "age": Schema.number().min(0).max(150).optional(),
    "is_active": Schema.boolean(),
    "tags": Schema.array(Schema.string()).min_length(1),
    "address": Schema.object(address_schema).optional()
}

validator = Schema.object(user_schema)

# Validate user data
user_data = {
    "name": "John Doe",
    "email": "john@example.com",
    "age": 30,
    "is_active": True,
    "tags": ["developer", "python"],
    "address": {
        "street": "123 Main St",
        "city": "Anytown",
        "postal_code": "12345",
        "country": "USA"
    }
}

result = validator.validate(user_data)
print(result.is_valid)  # True
```

### Exception-Based Validation

```python
age_validator = Schema.number().min(0).max(150)

try:
    age = age_validator.parse(25)  # Returns 25 if valid
    print(f"Valid age: {age}")
except ValidationError as e:
    print(f"Validation failed: {e}")
```

### Optional Fields

```python
profile_schema = {
    "username": Schema.string().min_length(3),
    "email": Schema.string().pattern(r'^[^\s@]+@[^\s@]+\.[^\s@]+$'),
    "bio": Schema.string().max_length(200).optional(),  # Optional field
    "age": Schema.number().min(13).optional()           # Optional field
}

validator = Schema.object(profile_schema)

# This is valid even without bio and age
profile_data = {
    "username": "johndoe",
    "email": "john@example.com"
}

result = validator.validate(profile_data)
print(result.is_valid)  # True
```

### Custom Error Messages

```python
validator = Schema.string().min_length(8).with_message("Password must be at least 8 characters long")

result = validator.validate("123")
print(result.errors[0])  # "Password must be at least 8 characters long"
```

## API Reference

### Schema Factory Methods

- `Schema.string()` - Creates a string validator
- `Schema.number()` - Creates a number validator (int or float)
- `Schema.boolean()` - Creates a boolean validator
- `Schema.array(item_validator)` - Creates an array validator
- `Schema.object(schema_dict)` - Creates an object validator

### String Validator Methods

- `.min_length(length)` - Sets minimum length requirement
- `.max_length(length)` - Sets maximum length requirement
- `.pattern(regex)` - Sets regex pattern requirement (string or compiled regex)

### Number Validator Methods

- `.min(value)` - Sets minimum value requirement
- `.max(value)` - Sets maximum value requirement

### Array Validator Methods

- `.min_length(length)` - Sets minimum array length requirement
- `.max_length(length)` - Sets maximum array length requirement

### Common Validator Methods

- `.optional()` - Makes the validator accept None values
- `.with_message(message)` - Sets custom error message
- `.validate(value)` - Returns ValidationResult object
- `.parse(value)` - Returns value if valid, raises ValidationError if not

### ValidationResult Object

- `.is_valid` - Boolean indicating if validation passed
- `.errors` - List of error messages
- Can be used in boolean context: `if result: ...`

## Running Examples

To see the library in action, run the example file:

```bash
python example_usage.py
```

This will demonstrate various validation scenarios with sample data.

## Running Tests

To run the comprehensive test suite:

```bash
python -m unittest test_validator.py -v
```

### Generate Test Coverage Report

To generate a test coverage report:

```bash
# Install coverage if not already installed
pip install coverage

# Run tests with coverage
coverage run -m unittest test_validator.py

# Generate coverage report
coverage report -m > test_report.txt

# View the report
cat test_report.txt
```

## File Structure

```
├── validator.py          # Main validation library
├── test_validator.py     # Comprehensive unit tests
├── example_usage.py      # Usage examples and demonstrations
├── README.md            # This documentation
└── test_report.txt      # Test coverage report (generated)
```

## Design Principles

This library follows several key design principles:

1. **Simplicity** - Clean, intuitive API that's easy to understand and use
2. **Type Safety** - Proper type checking with clear error messages
3. **Composability** - Validators can be easily combined and nested
4. **Extensibility** - Easy to add new validator types and rules
5. **Error Clarity** - Detailed error messages that help developers debug issues

## Contributing

This is a simple validation library designed to be lightweight and easy to understand. The code is well-documented with inline comments explaining the functionality of each component.

## License

This project is open source and available under the MIT License. 