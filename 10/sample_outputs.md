# Sample Application Runs

This document shows example runs of the Product Filtering System to demonstrate how the application works with different types of user queries.

## Sample Run 1: Electronics with Price and Stock Filter

**User Query**: "I need electronics under $200 that are in stock"

```
=== Product Search System ===
Using OpenAI Function Calling for Natural Language Product Filtering
Type 'exit' to quit the application

Enter your product search query: I need electronics under $200 that are in stock

Searching products...

Filtered Products:
1. Wireless Headphones - $99.99, Rating: 4.5, In Stock
2. Smart Watch - $199.99, Rating: 4.6, In Stock
3. Bluetooth Speaker - $49.99, Rating: 4.4, In Stock
4. Gaming Mouse - $59.99, Rating: 4.3, In Stock
5. External Hard Drive - $89.99, Rating: 4.4, In Stock
6. Portable Charger - $29.99, Rating: 4.2, In Stock
--------------------------------------------------
```

**Analysis**: 
- OpenAI correctly identified the category filter (Electronics)
- Extracted the maximum price constraint ($200)
- Applied the stock availability filter (in_stock_only: true)
- Returned 6 matching products from the Electronics category

## Sample Run 2: Fitness Equipment with Rating Filter

**User Query**: "Show me fitness equipment with rating above 4.5"

```
Enter your product search query: Show me fitness equipment with rating above 4.5

Searching products...

Filtered Products:
1. Treadmill - $899.99, Rating: 4.6, Out of Stock
2. Dumbbell Set - $149.99, Rating: 4.7, In Stock
3. Exercise Bike - $499.99, Rating: 4.5, In Stock
--------------------------------------------------
```

**Analysis**:
- OpenAI identified the category filter (Fitness)
- Extracted the minimum rating constraint (4.5)
- Note: Exercise Bike has exactly 4.5 rating, showing the system includes boundary values
- Returned products regardless of stock status since it wasn't specified

## Sample Run 3: Kitchen Appliances with Combined Filters

**User Query**: "I want kitchen appliances under $100 with good ratings that are available"

```
Enter your product search query: I want kitchen appliances under $100 with good ratings that are available

Searching products...

Filtered Products:
1. Air Fryer - $89.99, Rating: 4.6, In Stock
2. Coffee Maker - $79.99, Rating: 4.3, In Stock
3. Electric Kettle - $39.99, Rating: 4.4, In Stock
4. Rice Cooker - $59.99, Rating: 4.3, In Stock
5. Pressure Cooker - $99.99, Rating: 4.7, In Stock
--------------------------------------------------
```

**Analysis**:
- OpenAI identified multiple criteria:
  - Category: Kitchen
  - Maximum price: $100
  - "Good ratings" interpreted as minimum rating (likely 4.0+)
  - "Available" interpreted as in_stock_only: true
- Returned 5 matching kitchen appliances

## Sample Run 4: Keyword-Based Search

**User Query**: "Find headphones or speakers"

```
Enter your product search query: Find headphones or speakers

Searching products...

Filtered Products:
1. Wireless Headphones - $99.99, Rating: 4.5, In Stock
2. Noise-Cancelling Headphones - $299.99, Rating: 4.8, In Stock
3. Bluetooth Speaker - $49.99, Rating: 4.4, In Stock
--------------------------------------------------
```

**Analysis**:
- OpenAI identified keywords ["headphones", "speakers"]
- Searched across product names for matching terms
- Found products containing either "headphones" or "speaker" in their names
- No category, price, or rating filters were applied

## Sample Run 5: No Results Found

**User Query**: "Show me electronics over $2000 with rating above 4.9"

```
Enter your product search query: Show me electronics over $2000 with rating above 4.9

Searching products...

No products found matching your criteria.
--------------------------------------------------
```

**Analysis**:
- OpenAI correctly parsed the criteria:
  - Category: Electronics
  - Minimum price: $2000
  - Minimum rating: 4.9
- No products in the dataset match these strict criteria
- System gracefully handles empty results

## Key Observations

1. **Natural Language Understanding**: The system successfully interprets various phrasings like "under $200", "above 4.5", "that are available", etc.

2. **Multiple Criteria Handling**: OpenAI can extract and apply multiple filters simultaneously (category + price + rating + stock).

3. **Keyword Recognition**: The system can identify product-specific keywords and search across product names.

4. **Boundary Handling**: Products with exact boundary values (like rating 4.5 when asking for "above 4.5") are included appropriately.

5. **Error Handling**: When no products match the criteria, the system provides a clear message rather than crashing.

6. **Flexible Queries**: Users can phrase their requests in many different ways, and the system adapts to understand the intent.

## Exit Example

```
Enter your product search query: exit

Thank you for using the Product Search System!
```

The application exits gracefully when the user types 'exit', 'quit', or 'q'. 