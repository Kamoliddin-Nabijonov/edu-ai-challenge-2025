#!/usr/bin/env python3
"""
Unit tests for Service Analyzer application
"""

import unittest
import os
from unittest.mock import patch, MagicMock
from service_analyzer import ServiceAnalyzer


class TestServiceAnalyzer(unittest.TestCase):
    """Test cases for ServiceAnalyzer class."""
    
    def setUp(self):
        """Set up test fixtures."""
        # Mock environment variable for testing
        self.mock_api_key = "test-api-key-12345"
        
    @patch.dict(os.environ, {'OPENAI_API_KEY': 'test-api-key'})
    @patch('service_analyzer.load_dotenv')
    @patch('openai.OpenAI')
    def test_initialization_success(self, mock_openai, mock_load_dotenv):
        """Test successful initialization with API key."""
        analyzer = ServiceAnalyzer()
        self.assertIsNotNone(analyzer.client)
        mock_load_dotenv.assert_called_once()
        mock_openai.assert_called_once_with(api_key='test-api-key')
    
    @patch.dict(os.environ, {}, clear=True)
    @patch('service_analyzer.load_dotenv')
    def test_initialization_missing_api_key(self, mock_load_dotenv):
        """Test initialization failure when API key is missing."""
        with self.assertRaises(ValueError) as context:
            ServiceAnalyzer()
        self.assertIn("OpenAI API key not found", str(context.exception))
        mock_load_dotenv.assert_called_once()
    
    @patch.dict(os.environ, {'OPENAI_API_KEY': 'test-api-key'})
    @patch('service_analyzer.load_dotenv')
    @patch('openai.OpenAI')
    def test_create_service_prompt(self, mock_openai, mock_load_dotenv):
        """Test service prompt creation."""
        analyzer = ServiceAnalyzer()
        prompt = analyzer._create_service_prompt("Spotify")
        
        # Check that the prompt contains expected elements
        self.assertIn("Spotify", prompt)
        self.assertIn("Brief History", prompt)
        self.assertIn("Target Audience", prompt)
        self.assertIn("Core Features", prompt)
        self.assertIn("Unique Selling Points", prompt)
        self.assertIn("Business Model", prompt)
        self.assertIn("Tech Stack Insights", prompt)
        self.assertIn("Perceived Strengths", prompt)
        self.assertIn("Perceived Weaknesses", prompt)
    
    @patch.dict(os.environ, {'OPENAI_API_KEY': 'test-api-key'})
    @patch('service_analyzer.load_dotenv')
    @patch('openai.OpenAI')
    def test_create_text_prompt(self, mock_openai, mock_load_dotenv):
        """Test text prompt creation."""
        analyzer = ServiceAnalyzer()
        test_text = "We are a cloud-based project management platform"
        prompt = analyzer._create_text_prompt(test_text)
        
        # Check that the prompt contains the input text and expected sections
        self.assertIn(test_text, prompt)
        self.assertIn("Brief History", prompt)
        self.assertIn("Target Audience", prompt)
        self.assertIn("Core Features", prompt)
    
    @patch.dict(os.environ, {'OPENAI_API_KEY': 'test-api-key'})
    @patch('service_analyzer.load_dotenv')
    @patch('openai.OpenAI')
    def test_generate_report_success(self, mock_openai, mock_load_dotenv):
        """Test successful report generation."""
        # Mock the OpenAI response
        mock_response = MagicMock()
        mock_response.choices = [MagicMock()]
        mock_response.choices[0].message.content = "# Test Report\n\nThis is a test report."
        
        mock_client = MagicMock()
        mock_client.chat.completions.create.return_value = mock_response
        mock_openai.return_value = mock_client
        
        analyzer = ServiceAnalyzer()
        prompt = "Test prompt"
        report = analyzer._generate_report(prompt, "Test Context")
        
        # Verify the report contains expected content
        self.assertIn("# Test Report", report)
        self.assertIn("This is a test report.", report)
        self.assertIn("Report generated on", report)
        
        # Verify API was called with correct parameters
        mock_client.chat.completions.create.assert_called_once()
        call_args = mock_client.chat.completions.create.call_args
        self.assertEqual(call_args[1]['model'], 'gpt-4')
        self.assertEqual(len(call_args[1]['messages']), 2)
    
    @patch.dict(os.environ, {'OPENAI_API_KEY': 'test-api-key'})
    @patch('service_analyzer.load_dotenv')
    @patch('openai.OpenAI')
    def test_generate_report_api_error(self, mock_openai, mock_load_dotenv):
        """Test report generation with API error."""
        import openai
        
        mock_client = MagicMock()
        mock_client.chat.completions.create.side_effect = openai.APIError("API Error")
        mock_openai.return_value = mock_client
        
        analyzer = ServiceAnalyzer()
        prompt = "Test prompt"
        
        with self.assertRaises(Exception) as context:
            analyzer._generate_report(prompt, "Test Context")
        self.assertIn("OpenAI API error", str(context.exception))
    
    @patch.dict(os.environ, {'OPENAI_API_KEY': 'test-api-key'})
    @patch('service_analyzer.load_dotenv')
    @patch('openai.OpenAI')
    def test_analyze_service(self, mock_openai, mock_load_dotenv):
        """Test analyze_service method."""
        # Mock the OpenAI response
        mock_response = MagicMock()
        mock_response.choices = [MagicMock()]
        mock_response.choices[0].message.content = "# Spotify Analysis\n\nSpotify is a music streaming service."
        
        mock_client = MagicMock()
        mock_client.chat.completions.create.return_value = mock_response
        mock_openai.return_value = mock_client
        
        analyzer = ServiceAnalyzer()
        report = analyzer.analyze_service("Spotify")
        
        self.assertIn("Spotify", report)
        self.assertIn("music streaming", report)
    
    @patch.dict(os.environ, {'OPENAI_API_KEY': 'test-api-key'})
    @patch('service_analyzer.load_dotenv')
    @patch('openai.OpenAI')
    def test_analyze_text(self, mock_openai, mock_load_dotenv):
        """Test analyze_text method."""
        # Mock the OpenAI response
        mock_response = MagicMock()
        mock_response.choices = [MagicMock()]
        mock_response.choices[0].message.content = "# Service Analysis\n\nThis is a project management platform."
        
        mock_client = MagicMock()
        mock_client.chat.completions.create.return_value = mock_response
        mock_openai.return_value = mock_client
        
        analyzer = ServiceAnalyzer()
        test_text = "We are a cloud-based project management platform"
        report = analyzer.analyze_text(test_text)
        
        self.assertIn("Service Analysis", report)
        self.assertIn("project management", report)
    
    @patch.dict(os.environ, {'OPENAI_API_KEY': 'test-api-key'})
    @patch('service_analyzer.load_dotenv')
    @patch('openai.OpenAI')
    def test_verbose_mode(self, mock_openai, mock_load_dotenv):
        """Test verbose mode initialization."""
        analyzer = ServiceAnalyzer(verbose=True)
        self.assertTrue(analyzer.verbose)
        
        analyzer_quiet = ServiceAnalyzer(verbose=False)
        self.assertFalse(analyzer_quiet.verbose)


class TestPromptValidation(unittest.TestCase):
    """Test cases for prompt content validation."""
    
    @patch.dict(os.environ, {'OPENAI_API_KEY': 'test-api-key'})
    @patch('service_analyzer.load_dotenv')
    @patch('openai.OpenAI')
    def test_service_prompt_sections(self, mock_openai, mock_load_dotenv):
        """Test that service prompts contain all required sections."""
        analyzer = ServiceAnalyzer()
        prompt = analyzer._create_service_prompt("TestService")
        
        required_sections = [
            "Brief History",
            "Target Audience", 
            "Core Features",
            "Unique Selling Points",
            "Business Model",
            "Tech Stack Insights",
            "Perceived Strengths",
            "Perceived Weaknesses"
        ]
        
        for section in required_sections:
            with self.subTest(section=section):
                self.assertIn(section, prompt)
    
    @patch.dict(os.environ, {'OPENAI_API_KEY': 'test-api-key'})
    @patch('service_analyzer.load_dotenv')
    @patch('openai.OpenAI')
    def test_text_prompt_sections(self, mock_openai, mock_load_dotenv):
        """Test that text prompts contain all required sections."""
        analyzer = ServiceAnalyzer()
        prompt = analyzer._create_text_prompt("Sample service description")
        
        required_sections = [
            "Brief History",
            "Target Audience",
            "Core Features", 
            "Unique Selling Points",
            "Business Model",
            "Tech Stack Insights",
            "Perceived Strengths",
            "Perceived Weaknesses"
        ]
        
        for section in required_sections:
            with self.subTest(section=section):
                self.assertIn(section, prompt)


if __name__ == '__main__':
    # Run tests with verbose output
    unittest.main(verbosity=2)