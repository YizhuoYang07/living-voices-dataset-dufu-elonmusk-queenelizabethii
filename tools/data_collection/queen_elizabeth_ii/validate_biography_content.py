"""
Biography Content Validation for Queen Elizabeth II

This script validates that the biography.json contains correct information
about Elizabeth II (1926-2022), not Elizabeth I (1533-1603) or other figures.

This prevents the critical data error that occurred on 2024-10-04.

Author: Living Voices Project
Date: 2024-10-13
"""

import json
import sys
from pathlib import Path
from typing import Dict, List, Tuple


class BiographyContentValidator:
    """
    Validates the biographical content for Queen Elizabeth II.
    """
    
    # Expected facts about Elizabeth II
    EXPECTED_FACTS = {
        "birth_year": 1926,
        "death_year": 2022,
        "reign_start": 1952,
        "dynasty": "Windsor",
        "full_name": "Elizabeth Alexandra Mary",
        "father": "George VI",
        "husband": "Philip",
        "children": ["Charles", "Anne", "Andrew", "Edward"],
        "coronation_year": 1953,
    }
    
    # Facts that should NOT appear (Elizabeth I)
    WRONG_FACTS = {
        "birth_year": 1533,
        "death_year": 1603,
        "dynasty": "Tudor",
        "father": "Henry VIII",
        "mother": "Anne Boleyn",
    }
    
    def __init__(self, biography_file: Path):
        """
        Initialize the validator.
        
        Args:
            biography_file: Path to biography.json file
        """
        self.biography_file = biography_file
        self.errors = []
        self.warnings = []
        self.validations = []
        
    def load_biography(self) -> Dict:
        """
        Load the biography JSON file.
        
        Returns:
            Dictionary containing biography data
        """
        try:
            with open(self.biography_file, 'r', encoding='utf-8') as f:
                return json.load(f)
        except FileNotFoundError:
            self.errors.append(f"Biography file not found: {self.biography_file}")
            return {}
        except json.JSONDecodeError as e:
            self.errors.append(f"Invalid JSON in biography file: {e}")
            return {}
    
    def validate_title(self, data: Dict) -> bool:
        """
        Validate the title is "Elizabeth II" not "Elizabeth I".
        
        Args:
            data: Biography data dictionary
            
        Returns:
            True if valid, False otherwise
        """
        title = data.get("title", "")
        
        if "Elizabeth II" in title:
            self.validations.append(("✓", "Title", f"Correct: '{title}'"))
            return True
        elif "Elizabeth I" in title and "Elizabeth II" not in title:
            self.errors.append(f"Wrong title: '{title}' - should be 'Elizabeth II'")
            self.validations.append(("✗", "Title", f"WRONG: '{title}'"))
            return False
        else:
            self.warnings.append(f"Unexpected title format: '{title}'")
            self.validations.append(("⚠", "Title", f"Unexpected: '{title}'"))
            return False
    
    def validate_url(self, data: Dict) -> bool:
        """
        Validate the Wikipedia URL is for Elizabeth II.
        
        Args:
            data: Biography data dictionary
            
        Returns:
            True if valid, False otherwise
        """
        url = data.get("url", "")
        
        if "Elizabeth_II" in url:
            self.validations.append(("✓", "URL", "Correct Wikipedia page"))
            return True
        elif "Elizabeth_I" in url:
            self.errors.append(f"Wrong URL: {url} - points to Elizabeth I")
            self.validations.append(("✗", "URL", "WRONG: Points to Elizabeth I"))
            return False
        else:
            self.warnings.append(f"Unexpected URL format: {url}")
            self.validations.append(("⚠", "URL", f"Unexpected format"))
            return False
    
    def validate_dates(self, data: Dict) -> Tuple[bool, int]:
        """
        Validate birth/death years and other important dates.
        
        Args:
            data: Biography data dictionary
            
        Returns:
            Tuple of (is_valid, checks_passed)
        """
        content = data.get("content", "")
        checks_passed = 0
        total_checks = 4
        
        # Check for correct birth year (1926)
        if "1926" in content:
            self.validations.append(("✓", "Birth Year", "1926 found (correct)"))
            checks_passed += 1
        else:
            self.errors.append("Missing birth year: 1926 not found in content")
            self.validations.append(("✗", "Birth Year", "1926 NOT FOUND"))
        
        # Check for correct death year (2022)
        if "2022" in content:
            self.validations.append(("✓", "Death Year", "2022 found (correct)"))
            checks_passed += 1
        else:
            self.warnings.append("Death year 2022 not prominently mentioned")
            self.validations.append(("⚠", "Death Year", "2022 not prominent"))
        
        # Check it's NOT Elizabeth I dates (1533, 1603)
        first_1000_chars = content[:1000]
        if "1533" in first_1000_chars:
            self.errors.append("Found 1533 (Elizabeth I birth year) in early content")
            self.validations.append(("✗", "Wrong Dates", "1533 found (Elizabeth I)"))
        else:
            self.validations.append(("✓", "Wrong Dates", "No 1533 (Elizabeth I birth)"))
            checks_passed += 1
        
        if "1603" in first_1000_chars:
            self.errors.append("Found 1603 (Elizabeth I death year) in early content")
            self.validations.append(("✗", "Wrong Dates", "1603 found (Elizabeth I)"))
        else:
            self.validations.append(("✓", "Wrong Dates", "No 1603 (Elizabeth I death)"))
            checks_passed += 1
        
        return checks_passed == total_checks, checks_passed
    
    def validate_dynasty(self, data: Dict) -> bool:
        """
        Validate the dynasty is Windsor, not Tudor.
        
        Args:
            data: Biography data dictionary
            
        Returns:
            True if valid, False otherwise
        """
        content = data.get("content", "")
        
        has_windsor = "Windsor" in content
        has_tudor = "Tudor" in content[:2000]  # Check early content
        
        if has_windsor and not has_tudor:
            self.validations.append(("✓", "Dynasty", "Windsor found, no Tudor"))
            return True
        elif has_tudor and not has_windsor:
            self.errors.append("Found Tudor dynasty (Elizabeth I), not Windsor (Elizabeth II)")
            self.validations.append(("✗", "Dynasty", "Tudor found (WRONG)"))
            return False
        elif has_windsor:
            self.validations.append(("✓", "Dynasty", "Windsor found (correct)"))
            return True
        else:
            self.warnings.append("Neither Windsor nor Tudor dynasty mentioned")
            self.validations.append(("⚠", "Dynasty", "Not mentioned"))
            return False
    
    def validate_reign_length(self, data: Dict) -> bool:
        """
        Validate the reign length is approximately 70 years, not 44.
        
        Args:
            data: Biography data dictionary
            
        Returns:
            True if valid, False otherwise
        """
        content = data.get("content", "")
        
        # Look for mentions of long reign
        has_70_years = "70 years" in content or "70-year" in content
        has_longest_reign = "longest" in content.lower() and "reign" in content.lower()
        
        if has_70_years or has_longest_reign:
            self.validations.append(("✓", "Reign Length", "70-year reign mentioned"))
            return True
        else:
            self.warnings.append("70-year reign not prominently mentioned")
            self.validations.append(("⚠", "Reign Length", "Not clearly stated"))
            return False
    
    def validate_key_people(self, data: Dict) -> Tuple[bool, int]:
        """
        Validate mentions of key people in Elizabeth II's life.
        
        Args:
            data: Biography data dictionary
            
        Returns:
            Tuple of (is_valid, mentions_found)
        """
        content = data.get("content", "")
        mentions = 0
        
        key_people = {
            "Philip": "husband",
            "George VI": "father",
            "Charles": "son",
            "Anne": "daughter",
        }
        
        for person, relation in key_people.items():
            if person in content[:5000]:  # Check early content
                self.validations.append(("✓", f"Key Person", f"{person} ({relation}) mentioned"))
                mentions += 1
            else:
                self.warnings.append(f"{person} ({relation}) not found in early content")
        
        return mentions >= 3, mentions
    
    def run_validation(self) -> bool:
        """
        Run all validation checks.
        
        Returns:
            True if all critical validations pass, False otherwise
        """
        print("="*70)
        print("Queen Elizabeth II Biography Content Validation")
        print("="*70)
        print()
        
        # Load biography
        print("Loading biography.json...")
        data = self.load_biography()
        
        if not data:
            print("✗ Failed to load biography file")
            return False
        
        print(f"✓ Loaded biography: {len(data.get('content', ''))} characters")
        print()
        
        # Run validations
        print("Running validation checks...")
        print("-"*70)
        
        title_valid = self.validate_title(data)
        url_valid = self.validate_url(data)
        dates_valid, date_checks = self.validate_dates(data)
        dynasty_valid = self.validate_dynasty(data)
        reign_valid = self.validate_reign_length(data)
        people_valid, people_found = self.validate_key_people(data)
        
        # Print results
        print()
        print("="*70)
        print("VALIDATION RESULTS")
        print("="*70)
        
        for symbol, check, result in self.validations:
            print(f"{symbol} {check:20s} : {result}")
        
        print()
        print("="*70)
        print("SUMMARY")
        print("="*70)
        
        critical_passed = title_valid and url_valid and dates_valid
        
        print(f"Critical Checks:  {'✅ PASSED' if critical_passed else '❌ FAILED'}")
        print(f"  - Title:        {'✓' if title_valid else '✗'}")
        print(f"  - URL:          {'✓' if url_valid else '✗'}")
        print(f"  - Dates:        {date_checks}/4")
        print()
        print(f"Quality Checks:")
        print(f"  - Dynasty:      {'✓' if dynasty_valid else '⚠'}")
        print(f"  - Reign length: {'✓' if reign_valid else '⚠'}")
        print(f"  - Key people:   {people_found}/4 mentioned")
        print()
        print(f"Errors:   {len(self.errors)}")
        print(f"Warnings: {len(self.warnings)}")
        
        if self.errors:
            print()
            print("ERRORS:")
            for error in self.errors:
                print(f"  ✗ {error}")
        
        if self.warnings:
            print()
            print("WARNINGS:")
            for warning in self.warnings:
                print(f"  ⚠ {warning}")
        
        print()
        print("="*70)
        
        if critical_passed:
            print("✅ BIOGRAPHY CONTENT VALIDATION PASSED")
            print("   The biography contains correct Elizabeth II data.")
        else:
            print("❌ BIOGRAPHY CONTENT VALIDATION FAILED")
            print("   The biography may contain incorrect data!")
        
        print("="*70)
        
        return critical_passed


def main():
    """
    Main execution function.
    """
    # Determine biography file path
    script_dir = Path(__file__).parent
    dataset_root = script_dir.parent.parent.parent
    biography_file = dataset_root / "datasets" / "queen_elizabeth_ii" / "raw_data" / "wikipedia" / "biography.json"
    
    # Run validation
    validator = BiographyContentValidator(biography_file)
    success = validator.run_validation()
    
    # Exit with appropriate code
    sys.exit(0 if success else 1)


if __name__ == "__main__":
    main()
