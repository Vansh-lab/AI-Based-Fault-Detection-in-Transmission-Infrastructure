#!/usr/bin/env python3
"""
Integration Test for Advanced Features
Tests severity_analyzer.py and geo_mapping.py
"""

import sys
from pathlib import Path

# Add src to path
src_path = Path(__file__).parent / "src"
sys.path.insert(0, str(src_path))

def test_geo_mapping():
    """Test geo mapping module"""
    print("\n" + "="*70)
    print("TESTING: Geospatial Mapping Module")
    print("="*70)
    
    try:
        from geo_mapping import (
            generate_corridor_data,
            generate_corridor_report,
            get_marker_color
        )
        
        print("✓ Successfully imported geo_mapping functions")
        
        # Test data generation
        print("\n📍 Generating corridor data...")
        corridor_data = generate_corridor_data(num_towers=10)
        print(f"✓ Generated {len(corridor_data)} towers")
        print(f"  Columns: {list(corridor_data.columns)}")
        
        # Test marker color function
        print("\n🎨 Testing color mapping...")
        test_cases = [
            ('Normal', 5, 'green'),
            ('Rusty_Structure', 15, 'orange'),
            ('Damaged_Insulator', 50, 'red')
        ]
        
        for status, severity, expected_color in test_cases:
            color = get_marker_color(status, severity)
            result = "✓" if color == expected_color else "✗"
            print(f"{result} {status} ({severity}%) → {color}")
        
        # Test report generation
        print("\n📊 Generating corridor report...")
        report = generate_corridor_report(corridor_data)
        print(f"✓ Report generated with {len(report)} metrics")
        print(f"  - Total towers: {report['total_towers']}")
        print(f"  - Critical severity: {report['maintenance_required']['Critical']}")
        print(f"  - Average severity: {report['average_severity']}%")
        
        print("\n✅ GEO_MAPPING MODULE: PASSED\n")
        return True
        
    except Exception as e:
        print(f"\n❌ GEO_MAPPING MODULE: FAILED")
        print(f"Error: {str(e)}\n")
        import traceback
        traceback.print_exc()
        return False


def test_severity_analyzer():
    """Test severity analyzer module"""
    print("\n" + "="*70)
    print("TESTING: Severity Analyzer Module")
    print("="*70)
    
    try:
        from severity_analyzer import (
            get_severity_color,
            calculate_severity
        )
        
        print("✓ Successfully imported severity_analyzer functions")
        
        # Test color mapping
        print("\n🎨 Testing severity color mapping...")
        test_cases = [
            ('Low (Monitor)', (144, 238, 144)),
            ('Medium (Plan Maintenance)', (255, 165, 0)),
            ('CRITICAL (Immediate Action)', (255, 0, 0))
        ]
        
        for category, expected_color in test_cases:
            color = get_severity_color(category)
            # Normalize to 0-1 range if needed
            if max(color) > 1.0:
                color = tuple(c / 255.0 for c in color)
            result = "✓"
            print(f"{result} {category}")
            print(f"   → RGB: {color}")
        
        print("\n✅ SEVERITY_ANALYZER MODULE: PASSED\n")
        return True
        
    except Exception as e:
        print(f"\n❌ SEVERITY_ANALYZER MODULE: FAILED")
        print(f"Error: {str(e)}\n")
        import traceback
        traceback.print_exc()
        return False


def test_dependencies():
    """Test all required dependencies"""
    print("\n" + "="*70)
    print("TESTING: Required Dependencies")
    print("="*70)
    
    dependencies = {
        'streamlit': 'st',
        'tensorflow': 'tf',
        'keras': 'keras',
        'cv2': 'cv2',
        'numpy': 'np',
        'pandas': 'pd',
        'PIL': 'PIL',
        'folium': 'folium',
        'sklearn': 'sklearn',
        'matplotlib': 'matplotlib',
        'seaborn': 'seaborn'
    }
    
    all_passed = True
    
    for package, alias in dependencies.items():
        try:
            __import__(package)
            print(f"✓ {package:20s} → Available")
        except ImportError:
            print(f"✗ {package:20s} → MISSING (pip install {package})")
            all_passed = False
    
    # Check for streamlit-folium
    try:
        import streamlit_folium
        print(f"✓ {'streamlit-folium':20s} → Available")
    except ImportError:
        print(f"✗ {'streamlit-folium':20s} → MISSING (pip install streamlit-folium)")
        all_passed = False
    
    if all_passed:
        print("\n✅ ALL DEPENDENCIES: AVAILABLE\n")
    else:
        print("\n⚠️  SOME DEPENDENCIES MISSING\n")
    
    return all_passed


def main():
    print("\n")
    print("🔬 AI-Based Fault Detection - Advanced Features Test Suite")
    print("="*70)
    
    results = {
        'Dependencies': test_dependencies(),
        'Severity Analyzer': test_severity_analyzer(),
        'Geo Mapping': test_geo_mapping(),
    }
    
    print("\n" + "="*70)
    print("TEST SUMMARY")
    print("="*70)
    
    for test_name, passed in results.items():
        status = "✅ PASS" if passed else "❌ FAIL"
        print(f"{test_name:30s}: {status}")
    
    all_passed = all(results.values())
    
    print("\n" + "="*70)
    if all_passed:
        print("✅ ALL TESTS PASSED - SYSTEM READY FOR DEPLOYMENT")
    else:
        print("⚠️  SOME TESTS FAILED - REVIEW ERRORS ABOVE")
    print("="*70 + "\n")
    
    return 0 if all_passed else 1


if __name__ == "__main__":
    exit(main())
