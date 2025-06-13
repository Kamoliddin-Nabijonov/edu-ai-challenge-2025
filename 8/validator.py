"""
Simple but robust validation library for Python
Provides type-safe validator functions for primitive and complex data types
"""

import re
from typing import Any, Dict, List, Optional, Union, Callable
from dataclasses import dataclass


@dataclass
class ValidationResult:
    """Represents the result of a validation operation"""
    is_valid: bool
    errors: List[str]
    
    def __bool__(self) -> bool:
        """Allow ValidationResult to be used in boolean context"""
        return self.is_valid


class ValidationError(Exception):
    """Custom exception for validation errors"""
    def __init__(self, errors: List[str]):
        self.errors = errors
        super().__init__(f"Validation failed: {', '.join(errors)}")


class BaseValidator:
    """Base class for all validators"""
    
    def __init__(self):
        self._optional = False
        self._custom_message: Optional[str] = None
    
    def optional(self):
        """Makes this validator optional (allows None values)"""
        self._optional = True
        return self
    
    def with_message(self, message: str):
        """Sets a custom error message for this validator"""
        self._custom_message = message
        return self
    
    def validate(self, value: Any) -> ValidationResult:
        """Validates a value and returns a ValidationResult"""
        if value is None:
            if self._optional:
                return ValidationResult(True, [])
            else:
                error_msg = self._custom_message or "Value is required"
                return ValidationResult(False, [error_msg])
        
        return self._validate_value(value)
    
    def _validate_value(self, value: Any) -> ValidationResult:
        """Override this method in subclasses to implement validation logic"""
        raise NotImplementedError
    
    def parse(self, value: Any) -> Any:
        """Validates and returns the value if valid, raises ValidationError if not"""
        result = self.validate(value)
        if not result.is_valid:
            raise ValidationError(result.errors)
        return value


class StringValidator(BaseValidator):
    """Validator for string values"""
    
    def __init__(self):
        super().__init__()
        self._min_length: Optional[int] = None
        self._max_length: Optional[int] = None
        self._pattern: Optional[re.Pattern] = None
    
    def min_length(self, length: int):
        """Sets minimum length requirement for the string"""
        self._min_length = length
        return self
    
    def max_length(self, length: int):
        """Sets maximum length requirement for the string"""
        self._max_length = length
        return self
    
    def pattern(self, regex: Union[str, re.Pattern]):
        """Sets a regex pattern that the string must match"""
        if isinstance(regex, str):
            self._pattern = re.compile(regex)
        else:
            self._pattern = regex
        return self
    
    def _validate_value(self, value: Any) -> ValidationResult:
        """Validates that value is a string and meets all requirements"""
        errors = []
        
        if not isinstance(value, str):
            error_msg = self._custom_message or f"Expected string, got {type(value).__name__}"
            return ValidationResult(False, [error_msg])
        
        # Check minimum length
        if self._min_length is not None and len(value) < self._min_length:
            errors.append(f"String must be at least {self._min_length} characters long")
        
        # Check maximum length
        if self._max_length is not None and len(value) > self._max_length:
            errors.append(f"String must be at most {self._max_length} characters long")
        
        # Check pattern
        if self._pattern is not None and not self._pattern.match(value):
            errors.append(f"String does not match required pattern")
        
        return ValidationResult(len(errors) == 0, errors)


class NumberValidator(BaseValidator):
    """Validator for numeric values (int or float)"""
    
    def __init__(self):
        super().__init__()
        self._min_value: Optional[Union[int, float]] = None
        self._max_value: Optional[Union[int, float]] = None
    
    def min(self, value: Union[int, float]):
        """Sets minimum value requirement"""
        self._min_value = value
        return self
    
    def max(self, value: Union[int, float]):
        """Sets maximum value requirement"""
        self._max_value = value
        return self
    
    def _validate_value(self, value: Any) -> ValidationResult:
        """Validates that value is a number and meets all requirements"""
        errors = []
        
        if not isinstance(value, (int, float)):
            error_msg = self._custom_message or f"Expected number, got {type(value).__name__}"
            return ValidationResult(False, [error_msg])
        
        # Check minimum value
        if self._min_value is not None and value < self._min_value:
            errors.append(f"Number must be at least {self._min_value}")
        
        # Check maximum value
        if self._max_value is not None and value > self._max_value:
            errors.append(f"Number must be at most {self._max_value}")
        
        return ValidationResult(len(errors) == 0, errors)


class BooleanValidator(BaseValidator):
    """Validator for boolean values"""
    
    def _validate_value(self, value: Any) -> ValidationResult:
        """Validates that value is a boolean"""
        if not isinstance(value, bool):
            error_msg = self._custom_message or f"Expected boolean, got {type(value).__name__}"
            return ValidationResult(False, [error_msg])
        
        return ValidationResult(True, [])


class ArrayValidator(BaseValidator):
    """Validator for array/list values"""
    
    def __init__(self, item_validator: BaseValidator):
        super().__init__()
        self.item_validator = item_validator
        self._min_length: Optional[int] = None
        self._max_length: Optional[int] = None
    
    def min_length(self, length: int):
        """Sets minimum length requirement for the array"""
        self._min_length = length
        return self
    
    def max_length(self, length: int):
        """Sets maximum length requirement for the array"""
        self._max_length = length
        return self
    
    def _validate_value(self, value: Any) -> ValidationResult:
        """Validates that value is a list and all items are valid"""
        errors = []
        
        if not isinstance(value, list):
            error_msg = self._custom_message or f"Expected list, got {type(value).__name__}"
            return ValidationResult(False, [error_msg])
        
        # Check length constraints
        if self._min_length is not None and len(value) < self._min_length:
            errors.append(f"Array must have at least {self._min_length} items")
        
        if self._max_length is not None and len(value) > self._max_length:
            errors.append(f"Array must have at most {self._max_length} items")
        
        # Validate each item
        for i, item in enumerate(value):
            result = self.item_validator.validate(item)
            if not result.is_valid:
                for error in result.errors:
                    errors.append(f"Item at index {i}: {error}")
        
        return ValidationResult(len(errors) == 0, errors)


class ObjectValidator(BaseValidator):
    """Validator for object/dictionary values"""
    
    def __init__(self, schema: Dict[str, BaseValidator]):
        super().__init__()
        self.schema = schema
    
    def _validate_value(self, value: Any) -> ValidationResult:
        """Validates that value is a dict and all fields are valid"""
        errors = []
        
        if not isinstance(value, dict):
            error_msg = self._custom_message or f"Expected dict, got {type(value).__name__}"
            return ValidationResult(False, [error_msg])
        
        # Check each field in the schema
        for field_name, field_validator in self.schema.items():
            field_value = value.get(field_name)
            result = field_validator.validate(field_value)
            
            if not result.is_valid:
                for error in result.errors:
                    errors.append(f"Field '{field_name}': {error}")
        
        return ValidationResult(len(errors) == 0, errors)


class Schema:
    """Factory class for creating validators"""
    
    @staticmethod
    def string() -> StringValidator:
        """Creates a string validator"""
        return StringValidator()
    
    @staticmethod
    def number() -> NumberValidator:
        """Creates a number validator"""
        return NumberValidator()
    
    @staticmethod
    def boolean() -> BooleanValidator:
        """Creates a boolean validator"""
        return BooleanValidator()
    
    @staticmethod
    def array(item_validator: BaseValidator) -> ArrayValidator:
        """Creates an array validator with the specified item validator"""
        return ArrayValidator(item_validator)
    
    @staticmethod
    def object(schema: Dict[str, BaseValidator]) -> ObjectValidator:
        """Creates an object validator with the specified schema"""
        return ObjectValidator(schema) 