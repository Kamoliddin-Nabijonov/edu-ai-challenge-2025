# Product Filtering System using OpenAI Function Calling

This project demonstrates how to build a product filtering system using OpenAI's function calling capabilities. Instead of manually writing filtering logic, the system uses natural language processing to understand user preferences and automatically filters products from a dataset.

## Features

- **Natural Language Processing**: Accept user queries in plain English
- **OpenAI Function Calling**: Leverage OpenAI's structured function calling to interpret user preferences
- **Dynamic Filtering**: Filter products by category, price range, rating, stock availability, and keywords
- **Console Interface**: Easy-to-use command-line interface
- **Structured Output**: Clean, formatted results display

## Prerequisites

- Python 3.7 or higher
- OpenAI API key (get one from [OpenAI Platform](https://platform.openai.com/api-keys))

## Installation

1. **Clone or download the project files**
   ```bash
   # Navigate to the project directory
   cd 10/
   ```

2. **Install required Python packages**
   ```bash
   pip install -r requirements.txt
   ```

3. **Set up your OpenAI API key**
   
   
   ```bash
   export OPENAI_API_KEY='your-openai-api-key-here'
   ```

## Usage

1. **Run the application**
   ```bash
   python main.py
   ```

2. **Enter your search queries in natural language**
   
   The application will prompt you to enter search queries. You can use natural language like:
   - "I need electronics under $200 that are in stock"
   - "Show me fitness equipment with rating above 4.5"
   - "Find books about programming under $50"
   - "I want kitchen appliances that are highly rated"

3. **View filtered results**
   
   The system will display filtered products in the format:
   ```
   Filtered Products:
   1. Product Name - $Price, Rating: X.X, Stock Status
   2. Product Name - $Price, Rating: X.X, Stock Status
   ```

4. **Exit the application**
   
   Type `exit`, `quit`, or `q` to close the application.

## Available Product Categories

The dataset includes products from the following categories:
- **Electronics**: Headphones, laptops, smartphones, monitors, etc.
- **Fitness**: Yoga mats, treadmills, dumbbells, exercise bikes, etc.
- **Kitchen**: Blenders, air fryers, coffee makers, microwaves, etc.
- **Books**: Novels, programming guides, cookbooks, biographies, etc.
- **Clothing**: T-shirts, jeans, shoes, jackets, accessories, etc.

## How It Works

1. **User Input**: You provide a natural language query describing what you're looking for
2. **OpenAI Processing**: The system sends your query to OpenAI's GPT model with a function schema
3. **Function Calling**: OpenAI interprets your request and calls the filtering function with structured parameters
4. **Product Filtering**: The system filters the product database based on the extracted criteria
5. **Results Display**: Matching products are displayed in a clean, readable format

## Example Queries

Here are some example queries you can try:

- **Price-based filtering**: "Show me products under $100"
- **Category filtering**: "I need electronics"
- **Rating filtering**: "Find products with rating above 4.5"
- **Stock filtering**: "Show only items that are in stock"
- **Combined criteria**: "I want electronics under $200 with good ratings that are in stock"
- **Keyword search**: "Find headphones or speakers"

## Project Structure

```
10/
├── main.py              # Main application file
├── products.json        # Product dataset
├── requirements.txt     # Python dependencies
├── .env                 # Environment variables
├── README.md            # This file
└── sample_outputs.md    # Sample application runs
```

## Technical Details

### OpenAI Function Schema

The application defines a function schema that includes:

- **category**: Product category (Electronics, Fitness, Kitchen, Books, Clothing)
- **max_price**: Maximum price limit
- **min_price**: Minimum price limit
- **min_rating**: Minimum rating requirement (1.0 to 5.0)
- **in_stock_only**: Filter for in-stock items only
- **keywords**: Array of keywords to search for

### Error Handling

The application includes comprehensive error handling for:
- Missing API key
- Invalid API responses
- Network connectivity issues
- File reading errors
- Invalid user input

## Troubleshooting

### Common Issues

1. **"OPENAI_API_KEY not found" error**
   - Make sure you've created the `.env` file with your API key
   - Verify the API key format is correct

2. **"products.json file not found" error**
   - Ensure you're running the application from the correct directory
   - Check that `products.json` exists in the same folder as `main.py`

3. **API rate limiting**
   - If you encounter rate limiting, wait a few moments and try again
   - Consider upgrading your OpenAI plan for higher rate limits

4. **Import errors**
   - Make sure all required packages are installed: `pip install -r requirements.txt`
   - Check your Python version (3.7+ required)

## Security Notes

- Never commit your `.env` file or API key to version control
- Keep your OpenAI API key secure and don't share it publicly
- The `.env` file is excluded from git by default

## Support

If you encounter any issues:

1. Check the troubleshooting section above
2. Verify your OpenAI API key is valid and has sufficient credits
3. Ensure all dependencies are installed correctly
4. Check that you're using Python 3.7 or higher

## License

This project is for educational purposes as part of the AI Challenge 2025. 