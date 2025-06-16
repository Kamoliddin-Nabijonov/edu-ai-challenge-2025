#!/usr/bin/env python3
"""
Service Analyzer - Main Console Application
Analyzes services and generates comprehensive markdown reports
"""

import argparse
import sys
from service_analyzer import ServiceAnalyzer


def main():
    """Main entry point for the service analyzer application."""
    parser = argparse.ArgumentParser(
        description="Analyze services and generate comprehensive reports",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
                Examples:
                python main.py --service "Spotify"
                python main.py --service "Notion"
                python main.py --text "We are a cloud-based project management platform..."
                python main.py --service "Discord" --output report.md
        """
    )
    
    # Create mutually exclusive group for input type
    input_group = parser.add_mutually_exclusive_group(required=True)
    input_group.add_argument(
        '--service', '-s',
        type=str,
        help='Name of a known service (e.g., "Spotify", "Notion")'
    )
    input_group.add_argument(
        '--text', '-t',
        type=str,
        help='Raw service description text to analyze'
    )
    
    parser.add_argument(
        '--output', '-o',
        type=str,
        help='Output file path (default: print to console)'
    )
    
    parser.add_argument(
        '--verbose', '-v',
        action='store_true',
        help='Enable verbose output'
    )

    args = parser.parse_args()

    try:
        # Initialize the service analyzer
        analyzer = ServiceAnalyzer(verbose=args.verbose)
        
        # Determine input type and generate report
        if args.service:
            if args.verbose:
                print(f"Analyzing known service: {args.service}")
            report = analyzer.analyze_service(args.service)
        else:
            if args.verbose:
                print("Analyzing provided service description text")
            report = analyzer.analyze_text(args.text)
        
        # Output the report
        if args.output:
            with open(args.output, 'w', encoding='utf-8') as f:
                f.write(report)
            print(f"Report saved to: {args.output}")
        else:
            print(report)
            
    except Exception as e:
        print(f"Error: {e}", file=sys.stderr)
        sys.exit(1)


if __name__ == "__main__":
    main()