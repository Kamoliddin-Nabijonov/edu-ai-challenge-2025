#!/usr/bin/env python3
"""
Product Filtering System using OpenAI Function Calling
This application allows users to search for products using natural language
and returns filtered results using OpenAI's function calling capabilities.
"""

import json
import os
import sys
from typing import List, Dict, Any
from openai import OpenAI
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

class ProductFilter:
    def __init__(self):
        """Initialize the ProductFilter with OpenAI client and product data."""
        api_key = os.getenv('OPENAI_API_KEY')
        if not api_key:
            print("Error: OPENAI_API_KEY not found in environment variables.")
            print("Please create a .env file with your OpenAI API key.")
            sys.exit(1)
        
        self.client = OpenAI(api_key=api_key)
        self.products = self.load_products()
    
    def load_products(self) -> List[Dict[str, Any]]:
        """Load products from the JSON file."""
        try:
            with open('products.json', 'r') as file:
                return json.load(file)
        except FileNotFoundError:
            print("Error: products.json file not found.")
            sys.exit(1)
        except json.JSONDecodeError:
            print("Error: Invalid JSON format in products.json.")
            sys.exit(1)
    
    def filter_products(self, products: List[Dict[str, Any]], criteria: Dict[str, Any]) -> List[Dict[str, Any]]:
        """
        Filter products based on the provided criteria.
        This function will be called by OpenAI with structured arguments.
        """
        filtered = []
        
        for product in products:
            # Check if product matches all criteria
            if self._matches_criteria(product, criteria):
                filtered.append(product)
        
        return filtered
    
    def _matches_criteria(self, product: Dict[str, Any], criteria: Dict[str, Any]) -> bool:
        """Check if a product matches the given criteria."""
        # Check category
        if criteria.get('category') and product['category'].lower() != criteria['category'].lower():
            return False
        
        # Check maximum price
        if criteria.get('max_price') and product['price'] > criteria['max_price']:
            return False
        
        # Check minimum price
        if criteria.get('min_price') and product['price'] < criteria['min_price']:
            return False
        
        # Check minimum rating
        if criteria.get('min_rating') and product['rating'] < criteria['min_rating']:
            return False
        
        # Check stock availability
        if criteria.get('in_stock_only') and not product['in_stock']:
            return False
        
        # Check if product name contains keywords
        if criteria.get('keywords'):
            product_text = f"{product['name']} {product['category']}".lower()
            keywords = [kw.lower() for kw in criteria['keywords']]
            if not any(keyword in product_text for keyword in keywords):
                return False
        
        return True
    
    def search_products(self, user_query: str) -> List[Dict[str, Any]]:
        """
        Use OpenAI function calling to interpret user query and filter products.
        """
        # Define the function schema for OpenAI
        function_schema = {
            "name": "filter_products",
            "description": "Filter products based on user preferences and criteria",
            "parameters": {
                "type": "object",
                "properties": {
                    "category": {
                        "type": "string",
                        "enum": ["Electronics", "Fitness", "Kitchen", "Books", "Clothing"],
                        "description": "Product category to filter by"
                    },
                    "max_price": {
                        "type": "number",
                        "description": "Maximum price limit"
                    },
                    "min_price": {
                        "type": "number",
                        "description": "Minimum price limit"
                    },
                    "min_rating": {
                        "type": "number",
                        "description": "Minimum rating requirement (1.0 to 5.0)"
                    },
                    "in_stock_only": {
                        "type": "boolean",
                        "description": "Whether to only show in-stock items"
                    },
                    "keywords": {
                        "type": "array",
                        "items": {"type": "string"},
                        "description": "Keywords to search for in product names"
                    }
                },
                "required": []
            }
        }
        
        # Create the system message with product information
        system_message = f"""
        You are a product search assistant. Based on the user's natural language query, 
        you need to call the filter_products function with appropriate parameters.
        
        Available products data:
        {json.dumps(self.products, indent=2)}
        
        Analyze the user's request and extract filtering criteria such as:
        - Category preferences
        - Price range (max/min price)
        - Rating requirements
        - Stock availability needs
        - Specific product keywords or features
        
        Call the filter_products function with the extracted criteria.
        """
        
        try:
            # Make the API call with function calling
            response = self.client.chat.completions.create(
                model="gpt-4.1-mini",
                messages=[
                    {"role": "system", "content": system_message},
                    {"role": "user", "content": user_query}
                ],
                functions=[function_schema],
                function_call={"name": "filter_products"}
            )
            
            # Extract function call arguments
            function_call = response.choices[0].message.function_call
            if function_call and function_call.name == "filter_products":
                criteria = json.loads(function_call.arguments)
                return self.filter_products(self.products, criteria)
            else:
                print("No function call was made by the model.")
                return []
                
        except Exception as e:
            print(f"Error calling OpenAI API: {e}")
            return []
    
    def format_results(self, products: List[Dict[str, Any]]) -> str:
        """Format the filtered products for display."""
        if not products:
            return "No products found matching your criteria."
        
        result = "Filtered Products:\n"
        for i, product in enumerate(products, 1):
            stock_status = "In Stock" if product['in_stock'] else "Out of Stock"
            result += f"{i}. {product['name']} - ${product['price']:.2f}, Rating: {product['rating']}, {stock_status}\n"
        
        return result

def main():
    """Main function to run the console application."""
    print("=== Product Search System ===")
    print("Using OpenAI Function Calling for Natural Language Product Filtering")
    print("Type 'exit' to quit the application\n")
    
    filter_system = ProductFilter()
    
    while True:
        try:
            # Get user input
            user_query = input("Enter your product search query: ").strip()
            
            if user_query.lower() in ['exit', 'quit', 'q']:
                print("Thank you for using the Product Search System!")
                break
            
            if not user_query:
                print("Please enter a valid search query.\n")
                continue
            
            print("\nSearching products...")
            
            # Search for products using OpenAI function calling
            results = filter_system.search_products(user_query)
            
            # Display results
            formatted_results = filter_system.format_results(results)
            print(f"\n{formatted_results}")
            print("-" * 50)
            
        except KeyboardInterrupt:
            print("\n\nApplication interrupted by user. Goodbye!")
            break
        except Exception as e:
            print(f"An error occurred: {e}")
            print("Please try again.\n")

if __name__ == "__main__":
    main() 