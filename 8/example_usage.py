"""
Example usage of the validation library
Demonstrates practical usage scenarios with real-world examples
"""

from validator import Schema, ValidationError


def example_basic_validation():
    """Example of basic primitive type validation"""
    print("=== Basic Validation Examples ===")
    
    # String validation
    name_validator = Schema.string().min_length(2).max_length(50)
    
    print("String validation:")
    print(f"Valid name 'John': {name_validator.validate('John').is_valid}")
    print(f"Invalid name 'J': {name_validator.validate('J').is_valid}")
    
    # Number validation
    age_validator = Schema.number().min(0).max(150)
    
    print("\nNumber validation:")
    print(f"Valid age 25: {age_validator.validate(25).is_valid}")
    print(f"Invalid age -5: {age_validator.validate(-5).is_valid}")
    
    # Boolean validation
    active_validator = Schema.boolean()
    
    print("\nBoolean validation:")
    print(f"Valid boolean True: {active_validator.validate(True).is_valid}")
    print(f"Invalid boolean 'yes': {active_validator.validate('yes').is_valid}")


def example_email_validation():
    """Example of email validation using regex pattern"""
    print("\n=== Email Validation Example ===")
    
    email_validator = Schema.string().pattern(r'^[^\s@]+@[^\s@]+\.[^\s@]+$')
    
    test_emails = [
        "user@example.com",
        "test.email@domain.co.uk",
        "invalid-email",
        "user@",
        "@domain.com"
    ]
    
    for email in test_emails:
        result = email_validator.validate(email)
        status = "✓ Valid" if result.is_valid else "✗ Invalid"
        print(f"{status}: {email}")
        if not result.is_valid:
            print(f"   Error: {result.errors[0]}")


def example_array_validation():
    """Example of array validation"""
    print("\n=== Array Validation Example ===")
    
    # Array of strings with length constraints
    tags_validator = Schema.array(Schema.string()).min_length(1).max_length(5)
    
    test_arrays = [
        ["python", "javascript", "web"],
        [],  # Too short
        ["a", "b", "c", "d", "e", "f"],  # Too long
        ["python", 123]  # Invalid item type
    ]
    
    for i, array in enumerate(test_arrays):
        result = tags_validator.validate(array)
        status = "✓ Valid" if result.is_valid else "✗ Invalid"
        print(f"{status}: {array}")
        if not result.is_valid:
            for error in result.errors:
                print(f"   Error: {error}")


def example_complex_object_validation():
    """Example of complex nested object validation"""
    print("\n=== Complex Object Validation Example ===")
    
    # Define address schema
    address_schema = {
        "street": Schema.string().min_length(1),
        "city": Schema.string().min_length(1),
        "postal_code": Schema.string().pattern(r'^\d{5}$').with_message("Postal code must be 5 digits"),
        "country": Schema.string().min_length(2)
    }
    
    # Define user schema
    user_schema = {
        "id": Schema.string().with_message("ID must be a string"),
        "name": Schema.string().min_length(2).max_length(50),
        "email": Schema.string().pattern(r'^[^\s@]+@[^\s@]+\.[^\s@]+$'),
        "age": Schema.number().min(0).max(150).optional(),
        "is_active": Schema.boolean(),
        "tags": Schema.array(Schema.string()).min_length(1),
        "address": Schema.object(address_schema).optional()
    }
    
    validator = Schema.object(user_schema)
    
    # Valid user data
    valid_user = {
        "id": "12345",
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
    
    print("Validating valid user data:")
    result = validator.validate(valid_user)
    print(f"✓ Result: {result.is_valid}")
    
    # Invalid user data
    invalid_user = {
        "id": 12345,  # Should be string
        "name": "J",  # Too short
        "email": "invalid-email",  # Invalid format
        "age": -5,  # Below minimum
        "is_active": "yes",  # Wrong type
        "tags": [],  # Too short
        "address": {
            "street": "",  # Too short
            "city": "Anytown",
            "postal_code": "123",  # Wrong format
            "country": "US"
        }
    }
    
    print("\nValidating invalid user data:")
    result = validator.validate(invalid_user)
    print(f"✗ Result: {result.is_valid}")
    print("Errors:")
    for error in result.errors:
        print(f"   - {error}")


def example_parse_method():
    """Example of using the parse method for exception-based validation"""
    print("\n=== Parse Method Example ===")
    
    age_validator = Schema.number().min(0).max(150)
    
    try:
        # Valid case
        age = age_validator.parse(25)
        print(f"✓ Parsed age: {age}")
        
        # Invalid case
        age = age_validator.parse(-5)
        print(f"✓ Parsed age: {age}")
        
    except ValidationError as e:
        print(f"✗ Validation error: {e}")


def example_optional_fields():
    """Example of optional field validation"""
    print("\n=== Optional Fields Example ===")
    
    profile_schema = {
        "username": Schema.string().min_length(3),
        "email": Schema.string().pattern(r'^[^\s@]+@[^\s@]+\.[^\s@]+$'),
        "bio": Schema.string().max_length(200).optional(),
        "age": Schema.number().min(13).optional()
    }
    
    validator = Schema.object(profile_schema)
    
    # Profile with optional fields
    profile_with_optional = {
        "username": "johndoe",
        "email": "john@example.com",
        "bio": "Software developer passionate about Python",
        "age": 30
    }
    
    # Profile without optional fields
    profile_without_optional = {
        "username": "janedoe",
        "email": "jane@example.com"
    }
    
    print("Profile with optional fields:")
    result1 = validator.validate(profile_with_optional)
    print(f"✓ Valid: {result1.is_valid}")
    
    print("\nProfile without optional fields:")
    result2 = validator.validate(profile_without_optional)
    print(f"✓ Valid: {result2.is_valid}")


if __name__ == "__main__":
    example_basic_validation()
    example_email_validation()
    example_array_validation()
    example_complex_object_validation()
    example_parse_method()
    example_optional_fields() 