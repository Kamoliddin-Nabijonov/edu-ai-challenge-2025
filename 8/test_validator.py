"""
Comprehensive unit tests for the validation library
Tests cover all core functionality with both valid and invalid data scenarios
"""

import unittest
import re
from validator import (
    Schema, ValidationResult, ValidationError,
    StringValidator, NumberValidator, BooleanValidator, 
    ArrayValidator, ObjectValidator
)


class TestValidationResult(unittest.TestCase):
    """Tests for ValidationResult class"""
    
    def test_validation_result_bool_conversion(self):
        """Test that ValidationResult can be used in boolean context"""
        valid_result = ValidationResult(True, [])
        invalid_result = ValidationResult(False, ["Error"])
        
        self.assertTrue(valid_result)
        self.assertFalse(invalid_result)


class TestStringValidator(unittest.TestCase):
    """Tests for StringValidator class"""
    
    def test_valid_string(self):
        """Test validation of valid strings"""
        validator = Schema.string()
        result = validator.validate("hello")
        
        self.assertTrue(result.is_valid)
        self.assertEqual(result.errors, [])
    
    def test_invalid_type(self):
        """Test validation fails for non-string types"""
        validator = Schema.string()
        result = validator.validate(123)
        
        self.assertFalse(result.is_valid)
        self.assertIn("Expected string, got int", result.errors[0])
    
    def test_min_length(self):
        """Test minimum length validation"""
        validator = Schema.string().min_length(5)
        
        # Valid case
        result = validator.validate("hello")
        self.assertTrue(result.is_valid)
        
        # Invalid case
        result = validator.validate("hi")
        self.assertFalse(result.is_valid)
        self.assertIn("must be at least 5 characters", result.errors[0])
    
    def test_max_length(self):
        """Test maximum length validation"""
        validator = Schema.string().max_length(3)
        
        # Valid case
        result = validator.validate("hi")
        self.assertTrue(result.is_valid)
        
        # Invalid case
        result = validator.validate("hello")
        self.assertFalse(result.is_valid)
        self.assertIn("must be at most 3 characters", result.errors[0])
    
    def test_pattern_validation(self):
        """Test regex pattern validation"""
        # Email pattern
        email_validator = Schema.string().pattern(r'^[^\s@]+@[^\s@]+\.[^\s@]+$')
        
        # Valid email
        result = email_validator.validate("test@example.com")
        self.assertTrue(result.is_valid)
        
        # Invalid email
        result = email_validator.validate("invalid-email")
        self.assertFalse(result.is_valid)
        self.assertIn("does not match required pattern", result.errors[0])
    
    def test_custom_message(self):
        """Test custom error messages"""
        validator = Schema.string().with_message("Custom error message")
        result = validator.validate(123)
        
        self.assertFalse(result.is_valid)
        self.assertEqual(result.errors[0], "Custom error message")
    
    def test_optional_string(self):
        """Test optional string validation"""
        validator = Schema.string().optional()
        
        # None should be valid
        result = validator.validate(None)
        self.assertTrue(result.is_valid)
        
        # Valid string should still work
        result = validator.validate("hello")
        self.assertTrue(result.is_valid)
    
    def test_parse_method(self):
        """Test the parse method"""
        validator = Schema.string()
        
        # Valid case
        result = validator.parse("hello")
        self.assertEqual(result, "hello")
        
        # Invalid case should raise exception
        with self.assertRaises(ValidationError) as context:
            validator.parse(123)
        
        self.assertIn("Expected string", str(context.exception))


class TestNumberValidator(unittest.TestCase):
    """Tests for NumberValidator class"""
    
    def test_valid_numbers(self):
        """Test validation of valid numbers"""
        validator = Schema.number()
        
        # Test integer
        result = validator.validate(42)
        self.assertTrue(result.is_valid)
        
        # Test float
        result = validator.validate(3.14)
        self.assertTrue(result.is_valid)
    
    def test_invalid_type(self):
        """Test validation fails for non-numeric types"""
        validator = Schema.number()
        result = validator.validate("123")
        
        self.assertFalse(result.is_valid)
        self.assertIn("Expected number, got str", result.errors[0])
    
    def test_min_value(self):
        """Test minimum value validation"""
        validator = Schema.number().min(10)
        
        # Valid case
        result = validator.validate(15)
        self.assertTrue(result.is_valid)
        
        # Invalid case
        result = validator.validate(5)
        self.assertFalse(result.is_valid)
        self.assertIn("must be at least 10", result.errors[0])
    
    def test_max_value(self):
        """Test maximum value validation"""
        validator = Schema.number().max(100)
        
        # Valid case
        result = validator.validate(50)
        self.assertTrue(result.is_valid)
        
        # Invalid case
        result = validator.validate(150)
        self.assertFalse(result.is_valid)
        self.assertIn("must be at most 100", result.errors[0])


class TestBooleanValidator(unittest.TestCase):
    """Tests for BooleanValidator class"""
    
    def test_valid_booleans(self):
        """Test validation of valid booleans"""
        validator = Schema.boolean()
        
        # Test True
        result = validator.validate(True)
        self.assertTrue(result.is_valid)
        
        # Test False
        result = validator.validate(False)
        self.assertTrue(result.is_valid)
    
    def test_invalid_type(self):
        """Test validation fails for non-boolean types"""
        validator = Schema.boolean()
        result = validator.validate("true")
        
        self.assertFalse(result.is_valid)
        self.assertIn("Expected boolean, got str", result.errors[0])


class TestArrayValidator(unittest.TestCase):
    """Tests for ArrayValidator class"""
    
    def test_valid_array(self):
        """Test validation of valid arrays"""
        validator = Schema.array(Schema.string())
        result = validator.validate(["hello", "world"])
        
        self.assertTrue(result.is_valid)
        self.assertEqual(result.errors, [])
    
    def test_invalid_type(self):
        """Test validation fails for non-list types"""
        validator = Schema.array(Schema.string())
        result = validator.validate("not a list")
        
        self.assertFalse(result.is_valid)
        self.assertIn("Expected list, got str", result.errors[0])
    
    def test_invalid_items(self):
        """Test validation fails when items don't match validator"""
        validator = Schema.array(Schema.string())
        result = validator.validate(["hello", 123, "world"])
        
        self.assertFalse(result.is_valid)
        self.assertIn("Item at index 1", result.errors[0])
        self.assertIn("Expected string, got int", result.errors[0])
    
    def test_min_length(self):
        """Test minimum length validation for arrays"""
        validator = Schema.array(Schema.string()).min_length(2)
        
        # Valid case
        result = validator.validate(["a", "b"])
        self.assertTrue(result.is_valid)
        
        # Invalid case
        result = validator.validate(["a"])
        self.assertFalse(result.is_valid)
        self.assertIn("must have at least 2 items", result.errors[0])
    
    def test_max_length(self):
        """Test maximum length validation for arrays"""
        validator = Schema.array(Schema.string()).max_length(2)
        
        # Valid case
        result = validator.validate(["a", "b"])
        self.assertTrue(result.is_valid)
        
        # Invalid case
        result = validator.validate(["a", "b", "c"])
        self.assertFalse(result.is_valid)
        self.assertIn("must have at most 2 items", result.errors[0])


class TestObjectValidator(unittest.TestCase):
    """Tests for ObjectValidator class"""
    
    def test_valid_object(self):
        """Test validation of valid objects"""
        schema = {
            "name": Schema.string(),
            "age": Schema.number(),
            "active": Schema.boolean()
        }
        validator = Schema.object(schema)
        
        data = {
            "name": "John",
            "age": 30,
            "active": True
        }
        
        result = validator.validate(data)
        self.assertTrue(result.is_valid)
        self.assertEqual(result.errors, [])
    
    def test_invalid_type(self):
        """Test validation fails for non-dict types"""
        validator = Schema.object({"name": Schema.string()})
        result = validator.validate("not a dict")
        
        self.assertFalse(result.is_valid)
        self.assertIn("Expected dict, got str", result.errors[0])
    
    def test_invalid_fields(self):
        """Test validation fails when fields don't match schema"""
        schema = {
            "name": Schema.string(),
            "age": Schema.number()
        }
        validator = Schema.object(schema)
        
        data = {
            "name": 123,  # Should be string
            "age": "thirty"  # Should be number
        }
        
        result = validator.validate(data)
        self.assertFalse(result.is_valid)
        
        # Should have errors for both fields
        error_text = " ".join(result.errors)
        self.assertIn("Field 'name'", error_text)
        self.assertIn("Field 'age'", error_text)
    
    def test_missing_required_field(self):
        """Test validation fails when required fields are missing"""
        schema = {
            "name": Schema.string(),
            "age": Schema.number()
        }
        validator = Schema.object(schema)
        
        data = {
            "name": "John"
            # Missing age field
        }
        
        result = validator.validate(data)
        self.assertFalse(result.is_valid)
        self.assertIn("Field 'age'", result.errors[0])
        self.assertIn("Value is required", result.errors[0])
    
    def test_optional_fields(self):
        """Test validation passes when optional fields are missing"""
        schema = {
            "name": Schema.string(),
            "age": Schema.number().optional()
        }
        validator = Schema.object(schema)
        
        data = {
            "name": "John"
            # Missing optional age field
        }
        
        result = validator.validate(data)
        self.assertTrue(result.is_valid)


class TestComplexValidation(unittest.TestCase):
    """Tests for complex nested validation scenarios"""
    
    def test_nested_objects(self):
        """Test validation of nested objects"""
        address_schema = {
            "street": Schema.string(),
            "city": Schema.string(),
            "postal_code": Schema.string().pattern(r'^\d{5}$')
        }
        
        user_schema = {
            "name": Schema.string().min_length(2).max_length(50),
            "email": Schema.string().pattern(r'^[^\s@]+@[^\s@]+\.[^\s@]+$'),
            "age": Schema.number().min(0).max(150).optional(),
            "active": Schema.boolean(),
            "tags": Schema.array(Schema.string()),
            "address": Schema.object(address_schema).optional()
        }
        
        validator = Schema.object(user_schema)
        
        # Valid user data
        valid_data = {
            "name": "John Doe",
            "email": "john@example.com",
            "age": 30,
            "active": True,
            "tags": ["developer", "python"],
            "address": {
                "street": "123 Main St",
                "city": "Anytown",
                "postal_code": "12345"
            }
        }
        
        result = validator.validate(valid_data)
        self.assertTrue(result.is_valid)
        
        # Invalid user data
        invalid_data = {
            "name": "J",  # Too short
            "email": "invalid-email",  # Invalid format
            "age": -5,  # Below minimum
            "active": "yes",  # Wrong type
            "tags": [123, "developer"],  # Invalid item type
            "address": {
                "street": "123 Main St",
                "city": "Anytown",
                "postal_code": "123"  # Wrong format
            }
        }
        
        result = validator.validate(invalid_data)
        self.assertFalse(result.is_valid)
        
        # Should have multiple errors
        self.assertGreater(len(result.errors), 3)
    
    def test_array_of_objects(self):
        """Test validation of arrays containing objects"""
        item_schema = {
            "id": Schema.number(),
            "name": Schema.string()
        }
        
        validator = Schema.array(Schema.object(item_schema)).min_length(1)
        
        # Valid data
        valid_data = [
            {"id": 1, "name": "Item 1"},
            {"id": 2, "name": "Item 2"}
        ]
        
        result = validator.validate(valid_data)
        self.assertTrue(result.is_valid)
        
        # Invalid data
        invalid_data = [
            {"id": "1", "name": "Item 1"},  # Wrong type for id
            {"id": 2}  # Missing name
        ]
        
        result = validator.validate(invalid_data)
        self.assertFalse(result.is_valid)
        self.assertGreater(len(result.errors), 1)


if __name__ == '__main__':
    unittest.main() 