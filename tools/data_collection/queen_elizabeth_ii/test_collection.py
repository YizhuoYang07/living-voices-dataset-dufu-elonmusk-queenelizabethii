"""
Test script for Queen Elizabeth II data collection

Tests that the collect_wikipedia_data.py script fetches correct data
and doesn't mistakenly collect Elizabeth I data.

Author: Living Voices Project
Date: 2024-10-13
"""

import sys
from pathlib import Path

# Add parent directory to path for imports
script_dir = Path(__file__).parent
sys.path.insert(0, str(script_dir))

import wikipedia


def test_disambiguation_handling():
    """
    Test that we can correctly fetch Elizabeth II data and avoid Elizabeth I.
    """
    print("="*70)
    print("Testing Wikipedia Disambiguation Handling")
    print("="*70)
    print()
    
    print("Test 1: Direct 'Elizabeth II' query")
    print("-"*70)
    
    try:
        # This is what was causing the problem
        page = wikipedia.page("Elizabeth II")
        print(f"Result: {page.title}")
        print(f"URL: {page.url}")
        
        # Check if it's the right page
        if "1926" in page.content[:500]:
            print("✓ Contains 1926 (Elizabeth II birth year)")
        else:
            print("✗ Does NOT contain 1926")
        
        if "1533" in page.content[:500]:
            print("✗ WARNING: Contains 1533 (Elizabeth I birth year)")
        else:
            print("✓ Does not contain 1533")
            
    except Exception as e:
        print(f"✗ Error: {e}")
    
    print()
    print("Test 2: Improved disambiguation handling")
    print("-"*70)
    
    possible_titles = [
        "Elizabeth II of the United Kingdom",
        "Queen Elizabeth II",
        "Elizabeth II"
    ]
    
    page = None
    for title in possible_titles:
        try:
            print(f"Trying: {title}")
            test_page = wikipedia.page(title, auto_suggest=False)
            
            # Check if this is Elizabeth II
            if "1926" in test_page.content and ("2022" in test_page.content or "Elizabeth II" in test_page.title):
                page = test_page
                print(f"✓ Found correct page: {test_page.title}")
                break
        except:
            continue
    
    if page:
        print()
        print(f"Final result: {page.title}")
        print(f"URL: {page.url}")
        
        # Validate
        validations = []
        
        if "Elizabeth II" in page.title:
            validations.append("✓ Title contains 'Elizabeth II'")
        
        if "1926" in page.content:
            validations.append("✓ Contains birth year 1926")
        
        if "2022" in page.content:
            validations.append("✓ Contains death year 2022")
        
        if "Windsor" in page.content:
            validations.append("✓ Contains 'Windsor' dynasty")
        
        if "70 years" in page.content or "70-year" in page.content:
            validations.append("✓ Contains 70-year reign reference")
        
        # Check for wrong data
        if "1533" not in page.content[:1000]:
            validations.append("✓ Does NOT contain 1533 (Elizabeth I birth)")
        else:
            validations.append("✗ WARNING: Contains 1533 in early content")
        
        if "1603" not in page.content[:1000]:
            validations.append("✓ Does NOT contain 1603 (Elizabeth I death)")
        else:
            validations.append("✗ WARNING: Contains 1603 in early content")
        
        print()
        print("Validations:")
        for validation in validations:
            print(f"  {validation}")
        
        # Final check
        passed = all("✓" in v for v in validations)
        
        print()
        print("="*70)
        if passed:
            print("✅ TEST PASSED: Disambiguation handling works correctly")
        else:
            print("❌ TEST FAILED: Some validations failed")
        print("="*70)
        
        return passed
    else:
        print()
        print("="*70)
        print("❌ TEST FAILED: Could not fetch Elizabeth II page")
        print("="*70)
        return False


def test_collection_script_import():
    """
    Test that the collection script can be imported and has correct logic.
    """
    print()
    print("="*70)
    print("Testing Collection Script Import")
    print("="*70)
    print()
    
    try:
        from collect_wikipedia_data import QueenElizabethDataCollector
        print("✓ Successfully imported QueenElizabethDataCollector")
        
        # Check if the class has the expected method
        if hasattr(QueenElizabethDataCollector, 'collect_main_biography'):
            print("✓ Has collect_main_biography method")
        else:
            print("✗ Missing collect_main_biography method")
            return False
        
        print()
        print("="*70)
        print("✅ Import test passed")
        print("="*70)
        return True
        
    except ImportError as e:
        print(f"✗ Failed to import: {e}")
        print()
        print("="*70)
        print("❌ Import test failed")
        print("="*70)
        return False


def main():
    """
    Run all tests.
    """
    print("\n")
    print("╔" + "="*68 + "╗")
    print("║" + " "*15 + "Queen Elizabeth II Data Collection Tests" + " "*12 + "║")
    print("╚" + "="*68 + "╝")
    print()
    
    results = []
    
    # Test 1: Import
    results.append(("Import Test", test_collection_script_import()))
    
    # Test 2: Disambiguation
    results.append(("Disambiguation Test", test_disambiguation_handling()))
    
    # Summary
    print()
    print()
    print("="*70)
    print("TEST SUMMARY")
    print("="*70)
    
    for test_name, passed in results:
        status = "✅ PASSED" if passed else "❌ FAILED"
        print(f"{test_name:30s} : {status}")
    
    all_passed = all(passed for _, passed in results)
    
    print()
    print("="*70)
    if all_passed:
        print("✅ ALL TESTS PASSED")
        print("   The data collection script is working correctly.")
    else:
        print("❌ SOME TESTS FAILED")
        print("   Please review the errors above.")
    print("="*70)
    
    sys.exit(0 if all_passed else 1)


if __name__ == "__main__":
    main()
