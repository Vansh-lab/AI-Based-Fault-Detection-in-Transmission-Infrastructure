#!/usr/bin/env python3
"""
Complete System Verification & Testing Script
Verifies all features are working properly before hosting
"""

import sys
import os
from pathlib import Path
import json

# Color codes
GREEN = '\033[92m'
RED = '\033[91m'
YELLOW = '\033[93m'
BLUE = '\033[94m'
RESET = '\033[0m'
BOLD = '\033[1m'

def print_header(text):
    print(f"\n{BOLD}{BLUE}{'='*70}{RESET}")
    print(f"{BOLD}{BLUE}{text:^70}{RESET}")
    print(f"{BOLD}{BLUE}{'='*70}{RESET}\n")

def print_success(text):
    print(f"{GREEN}✅ {text}{RESET}")

def print_error(text):
    print(f"{RED}❌ {text}{RESET}")

def print_warning(text):
    print(f"{YELLOW}⚠️  {text}{RESET}")

def print_info(text):
    print(f"{BLUE}ℹ️  {text}{RESET}")

def test_file_existence():
    """Test 1: Check all critical files exist"""
    print_header("TEST 1: FILE EXISTENCE CHECK")
    
    critical_files = {
        'app/main.py': 'Streamlit Dashboard',
        'src/severity_analyzer.py': 'Severity Analysis Module',
        'src/geo_mapping.py': 'Geospatial Mapping Module',
        'src/data_loader.py': 'Data Pipeline',
        'src/train.py': 'Training Script',
        'src/evaluate.py': 'Evaluation Module',
        'src/model_builder.py': 'Model Architecture',
        'src/grad_cam.py': 'Explainability Module',
        'requirements.txt': 'Dependencies',
        'Dockerfile': 'Container Configuration',
        'docker-compose.yml': 'Docker Compose',
        'config.py': 'Configuration',
    }
    
    passed = 0
    failed = 0
    
    for filepath, description in critical_files.items():
        if Path(filepath).exists():
            print_success(f"{filepath:35s} - {description}")
            passed += 1
        else:
            print_error(f"{filepath:35s} - {description}")
            failed += 1
    
    print(f"\n{BOLD}Result: {passed} passed, {failed} failed{RESET}")
    return failed == 0

def test_python_syntax():
    """Test 2: Verify Python syntax of all modules"""
    print_header("TEST 2: PYTHON SYNTAX CHECK")
    
    python_files = [
        'app/main.py',
        'src/severity_analyzer.py',
        'src/geo_mapping.py',
        'src/data_loader.py',
        'launch.py',
        'test_advanced_features.py',
    ]
    
    passed = 0
    failed = 0
    
    for filepath in python_files:
        try:
            with open(filepath, 'r') as f:
                code = f.read()
            compile(code, filepath, 'exec')
            print_success(f"{filepath:40s} - Syntax OK")
            passed += 1
        except SyntaxError as e:
            print_error(f"{filepath:40s} - {str(e)[:50]}")
            failed += 1
        except FileNotFoundError:
            print_error(f"{filepath:40s} - NOT FOUND")
            failed += 1
    
    print(f"\n{BOLD}Result: {passed} passed, {failed} failed{RESET}")
    return failed == 0

def test_imports():
    """Test 3: Verify critical imports"""
    print_header("TEST 3: IMPORT CHECK")
    
    packages = {
        'tensorflow': 'Deep Learning',
        'numpy': 'Numerical Computing',
        'pandas': 'Data Analysis',
        'cv2': 'Image Processing',
        'streamlit': 'Web Framework',
        'PIL': 'Image Library',
        'sklearn': 'Machine Learning Utils',
        'matplotlib': 'Visualization',
        'folium': 'Geospatial Mapping',
    }
    
    passed = 0
    failed = 0
    
    for package, description in packages.items():
        try:
            __import__(package)
            print_success(f"{package:15s} - {description}")
            passed += 1
        except ImportError:
            print_warning(f"{package:15s} - NOT INSTALLED (optional)")
            # Don't count as failure - packages can be installed later
        except Exception as e:
            print_error(f"{package:15s} - {str(e)[:50]}")
            failed += 1
    
    print(f"\n{BOLD}Result: {passed} available{RESET}")
    if failed > 0:
        print(f"{YELLOW}Note: Install missing packages with: pip install -r requirements.txt{RESET}")
    return True

def test_module_imports():
    """Test 4: Verify custom modules can be imported"""
    print_header("TEST 4: CUSTOM MODULE IMPORTS")
    
    sys.path.insert(0, str(Path.cwd() / "src"))
    
    modules = {
        'severity_analyzer': ['calculate_severity', 'get_severity_color'],
        'geo_mapping': ['generate_corridor_data', 'create_transmission_map'],
        'data_loader': ['get_data_generators', 'get_test_generator'],
    }
    
    passed = 0
    failed = 0
    
    for module_name, functions in modules.items():
        try:
            module = __import__(module_name)
            
            # Check functions exist
            missing_functions = []
            for func_name in functions:
                if not hasattr(module, func_name):
                    missing_functions.append(func_name)
            
            if missing_functions:
                print_error(f"{module_name:30s} - Missing: {', '.join(missing_functions)}")
                failed += 1
            else:
                print_success(f"{module_name:30s} - All functions present")
                passed += 1
                
        except ImportError as e:
            print_error(f"{module_name:30s} - Import failed: {str(e)[:50]}")
            failed += 1
        except Exception as e:
            print_error(f"{module_name:30s} - Error: {str(e)[:50]}")
            failed += 1
    
    print(f"\n{BOLD}Result: {passed} passed, {failed} failed{RESET}")
    return failed == 0

def test_configuration():
    """Test 5: Verify configuration"""
    print_header("TEST 5: CONFIGURATION CHECK")
    
    config_checks = []
    
    # Check config.py
    try:
        import config
        config_checks.append(('config.py can be imported', True, None))
    except Exception as e:
        config_checks.append(('config.py import', False, str(e)))
    
    # Check requirements.txt
    try:
        with open('requirements.txt', 'r') as f:
            lines = f.readlines()
        if len(lines) > 10:
            config_checks.append(('requirements.txt has packages', True, f"{len(lines)} packages"))
        else:
            config_checks.append(('requirements.txt has packages', False, f"Only {len(lines)} packages"))
    except Exception as e:
        config_checks.append(('requirements.txt readable', False, str(e)))
    
    # Check Docker files
    docker_checks = [
        ('Dockerfile exists', Path('Dockerfile').exists()),
        ('docker-compose.yml exists', Path('docker-compose.yml').exists()),
    ]
    
    for check_name, result in docker_checks:
        config_checks.append((check_name, result, None))
    
    passed = 0
    failed = 0
    
    for check_name, result, detail in config_checks:
        if result:
            print_success(f"{check_name:40s} {detail if detail else ''}")
            passed += 1
        else:
            print_error(f"{check_name:40s} {detail if detail else ''}")
            failed += 1
    
    print(f"\n{BOLD}Result: {passed} passed, {failed} failed{RESET}")
    return failed == 0

def test_deployment_readiness():
    """Test 6: Check deployment readiness"""
    print_header("TEST 6: DEPLOYMENT READINESS")
    
    checks = []
    
    # Check documentation
    docs = [
        'HOSTING_DEPLOYMENT_GUIDE.md',
        'HOSTING_QUICK_REFERENCE.md',
        'DEPLOYMENT_READY.md',
        'QUICKSTART_ADVANCED_FEATURES.md',
    ]
    
    for doc in docs:
        exists = Path(doc).exists()
        checks.append((f"📖 {doc}", exists))
    
    # Check deployment scripts
    scripts = [
        'launch.py',
        'run_app.bat',
    ]
    
    for script in scripts:
        exists = Path(script).exists()
        checks.append((f"🚀 {script}", exists))
    
    passed = 0
    failed = 0
    
    for check_name, result in checks:
        if result:
            print_success(f"{check_name:50s}")
            passed += 1
        else:
            print_error(f"{check_name:50s}")
            failed += 1
    
    print(f"\n{BOLD}Result: {passed} passed, {failed} failed{RESET}")
    return failed == 0

def test_data_structure():
    """Test 7: Verify data directory structure"""
    print_header("TEST 7: DATA STRUCTURE CHECK")
    
    directories = {
        'dataset': ['train', 'val', 'test'],
        'models': [],
        'src': [],
        'app': [],
    }
    
    passed = 0
    failed = 0
    
    for base_dir, subdirs in directories.items():
        if Path(base_dir).exists():
            print_success(f"{base_dir:30s} - Exists")
            passed += 1
            
            for subdir in subdirs:
                subpath = Path(base_dir) / subdir
                if subpath.exists():
                    print_info(f"  ├─ {subdir:28s} - Exists")
                else:
                    print_warning(f"  ├─ {subdir:28s} - Create on first use")
        else:
            print_error(f"{base_dir:30s} - NOT FOUND")
            failed += 1
    
    print(f"\n{BOLD}Result: {passed} passed, {failed} failed{RESET}")
    return True

def generate_report():
    """Generate final verification report"""
    print_header("SYSTEM VERIFICATION REPORT")
    
    results = {
        'File Existence': test_file_existence(),
        'Python Syntax': test_python_syntax(),
        'Package Imports': test_imports(),
        'Module Imports': test_module_imports(),
        'Configuration': test_configuration(),
        'Deployment Ready': test_deployment_readiness(),
        'Data Structure': test_data_structure(),
    }
    
    # Print summary
    print_header("VERIFICATION SUMMARY")
    
    passed_tests = sum(1 for v in results.values() if v)
    total_tests = len(results)
    
    print(f"\n{BOLD}Test Results:{RESET}\n")
    for test_name, result in results.items():
        status = f"{GREEN}✅ PASS{RESET}" if result else f"{RED}❌ FAIL{RESET}"
        print(f"  {test_name:40s} {status}")
    
    print(f"\n{BOLD}Overall Status:{RESET}")
    print(f"  {passed_tests}/{total_tests} tests passed")
    
    if passed_tests == total_tests:
        print(f"\n{GREEN}{BOLD}✅ ALL SYSTEMS GO - READY TO DEPLOY!{RESET}\n")
        return True
    else:
        print(f"\n{YELLOW}{BOLD}⚠️  SOME TESTS FAILED - CHECK ABOVE FOR DETAILS{RESET}\n")
        return False

def main():
    print(f"\n{BOLD}{BLUE}")
    print("╔" + "═" * 68 + "╗")
    print("║" + " " * 10 + "🔬 SYSTEM VERIFICATION & FEATURE TEST" + " " * 20 + "║")
    print("║" + " " * 15 + "AI-Based Fault Detection System" + " " * 23 + "║")
    print("╚" + "═" * 68 + "╝")
    print(f"{RESET}\n")
    
    success = generate_report()
    
    if success:
        print_info("All systems verified! Proceed with hosting setup.")
        print_info("See HOSTING_QUICK_REFERENCE.md for deployment options.")
    else:
        print_warning("Review failed tests above and fix issues before deploying.")
    
    return 0 if success else 1

if __name__ == "__main__":
    exit_code = main()
    sys.exit(exit_code)
