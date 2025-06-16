"""
Service Analyzer Core Module
Handles OpenAI API integration and report generation logic
"""

import os
import openai
from datetime import datetime
from typing import Optional
from dotenv import load_dotenv


class ServiceAnalyzer:
    """Analyzes services and generates comprehensive markdown reports."""
    
    def __init__(self, verbose: bool = False):
        """
        Initialize the ServiceAnalyzer.
        
        Args:
            verbose (bool): Enable verbose output for debugging
        """
        self.verbose = verbose
        self.client = self._initialize_openai_client()
    
    def _initialize_openai_client(self) -> openai.OpenAI:
        """Initialize OpenAI client with API key from environment."""
        # Load environment variables from .env file
        load_dotenv()
        
        api_key = os.getenv('OPENAI_API_KEY')
        if not api_key:
            raise ValueError(
                "OpenAI API key not found. Please set OPENAI_API_KEY environment variable or create a .env file with OPENAI_API_KEY=your-key-here"
            )
        
        return openai.OpenAI(api_key=api_key)
    
    def analyze_service(self, service_name: str) -> str:
        """
        Analyze a known service by name.
        
        Args:
            service_name (str): Name of the service to analyze
            
        Returns:
            str: Formatted markdown report
        """
        prompt = self._create_service_prompt(service_name)
        return self._generate_report(prompt, f"Service: {service_name}")
    
    def analyze_text(self, service_text: str) -> str:
        """
        Analyze service based on provided description text.
        
        Args:
            service_text (str): Raw service description text
            
        Returns:
            str: Formatted markdown report
        """
        prompt = self._create_text_prompt(service_text)
        return self._generate_report(prompt, "Custom Service Description")
    
    def _create_service_prompt(self, service_name: str) -> str:
        """Create prompt for analyzing a known service."""
        return f"""
You are a business analyst tasked with creating a comprehensive analysis report for the service "{service_name}".

Please provide a detailed analysis in markdown format with the following sections:

# {service_name} - Service Analysis Report

## Brief History
Provide founding year, key milestones, major developments, and evolution of the service.

## Target Audience
Identify and describe the primary user segments and demographics.

## Core Features
List and explain the top 2-4 key functionalities that define this service.

## Unique Selling Points
Highlight the key differentiators that set this service apart from competitors.

## Business Model
Explain how the service generates revenue (subscription, freemium, advertising, etc.).

## Tech Stack Insights
Provide insights about the technologies, platforms, or technical approaches used (based on publicly available information).

## Perceived Strengths
List the main advantages and standout features that users and industry experts praise.

## Perceived Weaknesses
Identify common criticisms, limitations, or areas for improvement mentioned by users or analysts.

Please ensure each section is substantive and informative. Use bullet points, subheadings, and proper markdown formatting where appropriate.
        """
    
    def _create_text_prompt(self, service_text: str) -> str:
        """Create prompt for analyzing service from description text."""
        return f"""
You are a business analyst tasked with creating a comprehensive analysis report based on the following service description:

"{service_text}"

Please analyze this service and provide a detailed report in markdown format with the following sections:

# Service Analysis Report

## Brief History
Based on the description, infer or extract information about the service's history, founding, or development timeline. If specific details aren't available, indicate what can be reasonably inferred.

## Target Audience
Identify and describe the primary user segments and demographics based on the service description.

## Core Features
Extract and list the top 2-4 key functionalities mentioned or implied in the description.

## Unique Selling Points
Identify the key differentiators and unique aspects highlighted in the description.

## Business Model
Analyze and infer how this service likely generates revenue based on the description provided.

## Tech Stack Insights
Based on the description, provide insights about potential technologies, platforms, or technical approaches that might be used.

## Perceived Strengths
Identify the main advantages and benefits mentioned or implied in the description.

## Perceived Weaknesses
Identify potential limitations, challenges, or areas not addressed in the description that might be weaknesses.

Please ensure each section is substantive and informative. If certain information isn't available in the description, make reasonable inferences based on industry standards and similar services. Use bullet points, subheadings, and proper markdown formatting where appropriate.
        """
    
    def _generate_report(self, prompt: str, context: str) -> str:
        """
        Generate report using OpenAI API.
        
        Args:
            prompt (str): The prompt to send to OpenAI
            context (str): Context for verbose output
            
        Returns:
            str: Generated markdown report
        """
        if self.verbose:
            print(f"Generating report for: {context}")
            print("Sending request to OpenAI API...")
        
        try:
            response = self.client.chat.completions.create(
                model="gpt-4.1-mini",
                messages=[
                    {
                        "role": "system",
                        "content": "You are an expert business analyst specializing in digital services and technology companies. You provide comprehensive, well-structured analysis reports in markdown format."
                    },
                    {
                        "role": "user",
                        "content": prompt
                    }
                ],
                max_tokens=2500,
                temperature=0.7
            )
            
            report = response.choices[0].message.content
            
            # Add metadata footer
            timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            footer = f"\n\n---\n*Report generated on {timestamp} using OpenAI GPT-4*"
            
            if self.verbose:
                print("Report generated successfully!")
            
            return report + footer
            
        except openai.APIError as e:
            raise Exception(f"OpenAI API error: {e}")
        except Exception as e:
            raise Exception(f"Failed to generate report: {e}")