#!/usr/bin/env python3
"""
Run property analysis from command line.
Provides easy interface for analyzing single properties or batches.
"""

import sys
import argparse
from pathlib import Path
import os

# Add src to path
project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root / 'src'))

import logging
from analyzer import NYCPropertyInvestmentAnalyzer

def setup_logging(verbose=False):
    """Setup logging configuration"""
    level = logging.DEBUG if verbose else logging.INFO
    logging.basicConfig(
        level=level,
        format='%(asctime)s - %(levelname)s - %(message)s'
    )

def load_api_key():
    """Load API key from environment or .env file"""
    try:
        from dotenv import load_dotenv
        load_dotenv()
    except ImportError:
        pass
    
    return os.getenv('GOOGLE_MAPS_API_KEY', 'demo-api-key')

def analyze_single_property(analyzer, address, output_file=None):
    """Analyze a single property"""
    print(f"\n🏠 Analyzing: {address}")
    print("-" * 60)
    
    try:
        # Perform analysis
        analysis = analyzer.analyze_property(address)
        
        # Generate report
        report = analyzer.generate_detailed_report(analysis)
        
        # Display report
        print(report)
        
        # Save to file if requested
        if output_file:
            analyzer.save_analysis_report(analysis, output_file)
            print(f"\n💾 Report saved to: {output_file}")
        
        return analysis
        
    except Exception as e:
        print(f"❌ Error analyzing property: {e}")
        return None

def analyze_batch_properties(analyzer, addresses, output_file=None):
    """Analyze multiple properties"""
    print(f"\n📊 Batch analyzing {len(addresses)} properties...")
    print("=" * 60)
    
    try:
        # Perform batch analysis
        results = analyzer.batch_analyze_properties(addresses)
        
        if results.empty:
            print("❌ No properties analyzed successfully")
            return None
        
        # Rank opportunities
        ranked = analyzer.rank_investment_opportunities(results)
        
        # Display results
        print("\n🏆 Investment Opportunity Ranking:")
        print("=" * 80)
        print(f"{'Rank':<4} {'Address':<35} {'Rent':<10} {'Yield':<8} {'Cash Flow':<12} {'Recommendation':<12}")
        print("-" * 80)
        
        for _, row in ranked.head(10).iterrows():
            cash_flow_str = f"${row['monthly_cash_flow']:+,.0f}" if pd.notna(row['monthly_cash_flow']) else "N/A"
            print(f"{row['rank']:<4} {row['address'][:33]:<35} ${row['predicted_monthly_rent']:,.0f}{'':<2} {row['gross_yield']:.1f}%{'':<4} {cash_flow_str:<12} {row['recommendation']:<12}")
        
        # Summary statistics
        print("\n📈 Summary Statistics:")
        print(f"   Average Monthly Rent: ${ranked['predicted_monthly_rent'].mean():,.0f}")
        print(f"   Average Gross Yield: {ranked['gross_yield'].mean():.1f}%")
        print(f"   Properties with Positive Cash Flow: {(ranked['monthly_cash_flow'] > 0).sum()}/{len(ranked)}")
        
        # Save to file if requested
        if output_file:
            if output_file.endswith('.csv'):
                ranked.to_csv(output_file, index=False)
                print(f"\n💾 Results saved to: {output_file}")
            else:
                # Save as text report
                with open(output_file, 'w') as f:
                    f.write("NYC Property Investment Analysis - Batch Results\n")
                    f.write("=" * 60 + "\n\n")
                    f.write(ranked.to_string(index=False))
                print(f"\n💾 Results saved to: {output_file}")
        
        return ranked
        
    except Exception as e:
        print(f"❌ Error in batch analysis: {e}")
        import traceback
        traceback.print_exc()
        return None

def main():
    """Main analysis function"""
    parser = argparse.ArgumentParser(
        description='Analyze NYC property investment potential',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  # Single property analysis
  python scripts/run_analysis.py -a "123 West 86th Street, New York, NY"
  
  # Batch analysis
  python scripts/run_analysis.py -b "456 East 74th St, NY" "789 Broadway, NY" "321 Park Ave, NY"
  
  # Save report to file
  python scripts/run_analysis.py -a "123 Main St, NY" -o report.txt
  
  # Use custom API key
  python scripts/run_analysis.py -k "your-api-key" -a "Your Address Here"
        """
    )
    
    parser.add_argument('--address', '-a', type=str,
                       help='Property address to analyze')
    parser.add_argument('--api-key', '-k', type=str,
                       help='Google Maps API key (optional, uses .env or demo mode)')
    parser.add_argument('--batch', '-b', type=str, nargs='+',
                       help='Multiple addresses for batch analysis')
    parser.add_argument('--output', '-o', type=str,
                       help='Save report to file (.txt, .csv for batch)')
    parser.add_argument('--verbose', '-v', action='store_true',
                       help='Enable verbose logging')
    
    args = parser.parse_args()
    
    # Check arguments
    if not args.address and not args.batch:
        parser.print_help()
        print("\n❌ Error: Must specify either --address or --batch")
        return False
    
    if args.address and args.batch:
        print("❌ Error: Cannot specify both --address and --batch")
        return False
    
    # Setup logging
    setup_logging(args.verbose)
    
    # Load API key
    api_key = args.api_key or load_api_key()
    
    print("🏙️  NYC Property Investment Analyzer")
    print("=" * 50)
    
    if api_key == 'demo-api-key':
        print("🔧 Running in demo mode (simulated data)")
        print("💡 Add Google API key to .env for real location data")
    else:
        print("🔑 Using Google API key for real location data")
    
    try:
        # Initialize analyzer
        print("\n⚙️  Initializing analyzer (training ML model)...")
        analyzer = NYCPropertyInvestmentAnalyzer(api_key)
        print("✅ Analyzer ready!")
        
        # Import pandas for batch analysis
        import pandas as pd
        
        if args.address:
            # Single property analysis
            result = analyze_single_property(analyzer, args.address, args.output)
            success = result is not None
        else:
            # Batch analysis
            result = analyze_batch_properties(analyzer, args.batch, args.output)
            success = result is not None
    
    except KeyboardInterrupt:
        print("\n⏹️  Analysis interrupted by user")
        return False
    except Exception as e:
        print(f"\n❌ Error: {e}")
        if args.verbose:
            import traceback
            traceback.print_exc()
        return False
    
    if success:
        print("\n✅ Analysis complete!")
        print("\n📚 More options:")
        print("  python scripts/test_system.py           # Test all components")
        print("  python scripts/run_analysis.py --help   # See all options")
    else:
        print("\n❌ Analysis failed. Check error messages above.")
    
    return success

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)
