#!/usr/bin/env python3
"""Run the complete test suite with reporting"""
import subprocess
import sys
import os
from datetime import datetime
from pathlib import Path

def run_tests():
    """Run all test categories and generate reports"""
    
    print("🧪 Running Data Pipeline QA Test Suite")
    print("=" * 50)
    
    # Ensure reports directory exists
    reports_dir = Path("reports")
    reports_dir.mkdir(exist_ok=True)
    
    # Test commands to run
    test_commands = [
        {
            "name": "Unit Tests",
            "command": ["pytest", "tests/unit/", "-v", "--tb=short"],
            "markers": "unit"
        },
        {
            "name": "Integration Tests", 
            "command": ["pytest", "tests/integration/", "-v", "--tb=short"],
            "markers": "integration"
        },
        {
            "name": "Regression Tests",
            "command": ["pytest", "tests/regression/", "-v", "--tb=short"],
            "markers": "regression"
        }
    ]
    
    results = {}
    
    for test_suite in test_commands:
        print(f"\n📋 Running {test_suite['name']}...")
        
        try:
            result = subprocess.run(
                test_suite["command"],
                capture_output=True,
                text=True,
                timeout=300  # 5 minute timeout
            )
            
            results[test_suite["name"]] = {
                "exit_code": result.returncode,
                "stdout": result.stdout,
                "stderr": result.stderr
            }
            
            if result.returncode == 0:
                print(f"✅ {test_suite['name']} PASSED")
            else:
                print(f"❌ {test_suite['name']} FAILED")
                
        except subprocess.TimeoutExpired:
            print(f"⏰ {test_suite['name']} TIMEOUT")
            results[test_suite["name"]] = {"exit_code": -1, "error": "timeout"}
        except Exception as e:
            print(f"💥 {test_suite['name']} ERROR: {e}")
            results[test_suite["name"]] = {"exit_code": -1, "error": str(e)}
    
    # Generate summary report
    print("\n📊 Test Summary")
    print("=" * 30)
    
    total_suites = len(test_commands)
    passed_suites = sum(1 for r in results.values() if r["exit_code"] == 0)
    
    print(f"Total test suites: {total_suites}")
    print(f"Passed: {passed_suites}")
    print(f"Failed: {total_suites - passed_suites}")
    
    # Return overall status
    return 0 if passed_suites == total_suites else 1

if __name__ == "__main__":
    exit_code = run_tests()
    sys.exit(exit_code)
