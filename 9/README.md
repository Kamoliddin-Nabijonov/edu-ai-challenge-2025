# Service Analyzer

A powerful console application that generates comprehensive, multi-perspective analysis reports for digital services and products. The application uses OpenAI's GPT-4.1 mini to analyze services from multiple viewpoints including business, technical, and user-focused perspectives.

## Features

- **Flexible Input**: Analyze known services by name (e.g., "Spotify", "Notion") or provide custom service descriptions
- **Comprehensive Analysis**: Generate reports with 8 key sections covering all aspects of a service
- **Professional Output**: Clean, markdown-formatted reports suitable for business presentations
- **Console Interface**: Easy-to-use command-line interface with multiple options
- **File Export**: Save reports to files or display in terminal

## Installation

### Prerequisites

- Python 3.7 or higher
- OpenAI API key (get one from [OpenAI Platform](https://platform.openai.com/api-keys))

### Setup Steps

1. **Clone or download the project files**
   ```bash
   # Create a new directory for the project
   mkdir service-analyzer
   cd service-analyzer
   
   # Copy all the project files to this directory
   # - main.py
   # - service_analyzer.py
   # - test_service_analyzer.py
   # - requirements.txt
   # - README.md
   # - sample_outputs.md
   ```

2. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

3. **Set up your OpenAI API key**
   
   **Option A: Environment Variable (Temporary)**
   ```bash
   # On Linux/Mac
   export OPENAI_API_KEY="your-api-key-here"
   
   # On Windows
   set OPENAI_API_KEY=your-api-key-here
   ```
   
   **Option B: Create a .env file (Recommended)**
   ```bash
   # Create a .env file in the project directory
   echo "OPENAI_API_KEY=your-api-key-here" > .env
   
   # Or copy the example file and edit it
   cp .env.example .env
   # Then edit .env with your actual API key
   ```
   
   **⚠️ Security Note**: Never commit your API key to version control. The `.env` file is already included in `.gitignore` to prevent accidental commits.

## Usage

The application provides two main modes of operation:

### 1. Analyze Known Services

Analyze popular services by name:

```bash
python main.py --service "Spotify"
python main.py --service "Notion"
python main.py --service "Discord"
python main.py -s "OpenAI"
```

### 2. Analyze Custom Service Descriptions

Provide your own service description:

```bash
python main.py --text "We are a cloud-based project management platform that helps teams collaborate on tasks, track progress, and manage deadlines. Our service includes real-time collaboration, automated reporting, and integrations with popular tools."
```

### Command Line Options

```bash
python main.py [OPTIONS]

Required (choose one):
  --service, -s TEXT    Name of a known service (e.g., "Spotify", "Notion")
  --text, -t TEXT       Raw service description text to analyze

Optional:
  --output, -o FILE     Save report to file instead of printing to console
  --verbose, -v         Enable verbose output for debugging
  --help, -h            Show help message and exit
```

### Examples

**Basic service analysis:**
```bash
python main.py --service "Spotify"
```

**Custom service with file output:**
```bash
python main.py --text "A mobile app for food delivery with real-time tracking" --output report.md
```

**Verbose mode for debugging:**
```bash
python main.py --service "Notion" --verbose
```

## Report Structure

Each generated report includes the following sections:

1. **Brief History**: Founding year, milestones, and key developments
2. **Target Audience**: Primary user segments and demographics
3. **Core Features**: Top 2-4 key functionalities
4. **Unique Selling Points**: Key differentiators from competitors
5. **Business Model**: Revenue generation methods
6. **Tech Stack Insights**: Technology and platform information
7. **Perceived Strengths**: Advantages and standout features
8. **Perceived Weaknesses**: Common criticisms and limitations

## Running Tests

The project includes comprehensive unit tests to ensure reliability:

```bash
# Run all tests
python -m pytest test_service_analyzer.py -v

# Alternative: Run with unittest
python test_service_analyzer.py

# Run specific test class
python -m pytest test_service_analyzer.py::TestServiceAnalyzer -v

# Run with coverage (requires pytest-cov)
pip install pytest-cov
python -m pytest test_service_analyzer.py --cov=service_analyzer --cov-report=html
```

### Test Coverage

The tests cover:
- ✅ Initialization and API key validation
- ✅ Prompt generation for both service names and text descriptions
- ✅ OpenAI API integration and error handling
- ✅ Report generation and formatting
- ✅ Verbose mode functionality
- ✅ All required report sections validation

## Troubleshooting

### Common Issues

**1. API Key Not Found (Even with .env file)**
```
Error: OpenAI API key not found. Please set OPENAI_API_KEY environment variable.
```
**Solution**: 
- Make sure your `.env` file is in the same directory as `main.py`
- Check that your `.env` file contains: `OPENAI_API_KEY=your-actual-key-here` (no spaces around the equals sign)
- Ensure the `.env` file doesn't have any extra characters or quotes around the key
- Try running with verbose mode: `python main.py --service "test" --verbose` to see if there are any loading errors

**2. OpenAI API Error**
```
Error: OpenAI API error: Rate limit exceeded
```
**Solution**: You've hit the API rate limit. Wait a moment and try again, or check your OpenAI usage limits.

**3. Import Error**
```
ModuleNotFoundError: No module named 'openai'
```
**Solution**: Install the required dependencies: `pip install -r requirements.txt`

**4. Permission Denied (File Output)**
```
Error: [Errno 13] Permission denied: 'report.md'
```
**Solution**: Ensure you have write permissions to the output directory, or choose a different output path.

### Debugging

Use the `--verbose` flag to see detailed information about the analysis process:

```bash
python main.py --service "Spotify" --verbose
```

This will show:
- Which service or text is being analyzed
- API request status
- Generation progress
- Any warnings or additional information

## Development

### Project Structure

```
service-analyzer/
├── main.py                    # Console application entry point
├── service_analyzer.py        # Core analysis logic and OpenAI integration
├── test_service_analyzer.py   # Unit tests
├── requirements.txt           # Python dependencies
├── README.md                  # This file
├── sample_outputs.md          # Example outputs
└── .env                       # Environment variables (create this)
```

### Adding New Features

To extend the application:

1. **Add new analysis sections**: Modify the prompt templates in `service_analyzer.py`
2. **Support new input formats**: Extend the argument parser in `main.py`
3. **Add new output formats**: Modify the report generation logic
4. **Improve error handling**: Add more specific exception handling

### Code Style

The project follows Python best practices:
- PEP 8 style guide
- Comprehensive docstrings
- Type hints where appropriate
- Modular design with separation of concerns

## API Costs

This application uses OpenAI's GPT-4 model. Approximate costs:
- Each report generation: ~$0.05-0.15 USD
- Costs vary based on input length and report complexity
- Monitor your usage at [OpenAI Usage Dashboard](https://platform.openai.com/usage)

## Contributing

1. Fork the repository
2. Create a feature branch
3. Add tests for new functionality
4. Ensure all tests pass
5. Submit a pull request

## License

This project is provided as-is for educational and demonstration purposes. Please ensure compliance with OpenAI's usage policies when using this application.

## Support

For issues and questions:
1. Check the troubleshooting section above
2. Review the test cases for expected behavior
3. Verify your OpenAI API key and usage limits
4. Check the sample outputs for expected report format

---

**Note**: This application requires an active OpenAI API key and internet connection to function. API costs apply based on usage.