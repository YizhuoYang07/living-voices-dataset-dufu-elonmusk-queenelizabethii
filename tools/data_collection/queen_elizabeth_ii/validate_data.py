"""
Queen Elizabeth II Data Validation and Quality Check

This script validates collected data for quality, completeness, and compliance
with academic standards.

Author: Living Voices Project
Date: 2024-10-04
"""

import json
from datetime import datetime
from pathlib import Path
from typing import Dict, List, Tuple


class DataValidator:
    """
    Validator for Queen Elizabeth II dataset quality assurance.
    """
    
    def __init__(self, dataset_dir: str):
        """
        Initialize the validator.
        
        Args:
            dataset_dir: Root directory of the dataset
        """
        self.dataset_dir = Path(dataset_dir)
        self.raw_data_dir = self.dataset_dir / "raw_data"
        self.validation_results = {
            "timestamp": datetime.now().isoformat(),
            "checks": [],
            "errors": [],
            "warnings": [],
            "statistics": {}
        }
    
    def validate_all(self) -> Dict:
        """
        Run all validation checks.
        
        Returns:
            Dictionary containing validation results
        """
        print("="*70)
        print("Data Validation Report - Queen Elizabeth II Dataset")
        print("="*70)
        print()
        
        # Check 1: Directory structure
        self._check_directory_structure()
        
        # Check 2: Wikipedia data
        self._validate_wikipedia_data()
        
        # Check 3: Token count and progress
        self._calculate_statistics()
        
        # Check 4: Data quality
        self._check_data_quality()
        
        # Print summary
        self._print_summary()
        
        # Save validation report
        self._save_report()
        
        return self.validation_results
    
    def _check_directory_structure(self):
        """
        Verify that all required directories exist.
        """
        print("Checking directory structure...")
        
        required_dirs = [
            self.raw_data_dir,
            self.raw_data_dir / "wikipedia",
            self.raw_data_dir / "speeches",
            self.raw_data_dir / "metadata"
        ]
        
        for directory in required_dirs:
            if directory.exists():
                self.validation_results["checks"].append({
                    "check": "directory_structure",
                    "item": str(directory.name),
                    "status": "pass"
                })
                print(f"  ✓ {directory.name}/")
            else:
                self.validation_results["errors"].append({
                    "check": "directory_structure",
                    "item": str(directory),
                    "message": "Directory does not exist"
                })
                print(f"  ✗ {directory.name}/ - NOT FOUND")
        print()
    
    def _validate_wikipedia_data(self):
        """
        Validate Wikipedia collected data.
        """
        print("Validating Wikipedia data...")
        
        # Check biography file
        biography_file = self.raw_data_dir / "wikipedia" / "biography.json"
        if biography_file.exists():
            try:
                with open(biography_file, 'r', encoding='utf-8') as f:
                    biography = json.load(f)
                
                # Validate required fields
                required_fields = ["title", "url", "content", "summary", "word_count"]
                missing_fields = [f for f in required_fields if f not in biography]
                
                if missing_fields:
                    self.validation_results["warnings"].append({
                        "file": "biography.json",
                        "message": f"Missing fields: {missing_fields}"
                    })
                    print(f"  ⚠ biography.json - Missing fields: {missing_fields}")
                else:
                    self.validation_results["checks"].append({
                        "check": "wikipedia_biography",
                        "status": "pass",
                        "word_count": biography.get("word_count", 0)
                    })
                    print(f"  ✓ biography.json - {biography.get('word_count', 0):,} words")
                
            except json.JSONDecodeError as e:
                self.validation_results["errors"].append({
                    "file": "biography.json",
                    "message": f"Invalid JSON: {e}"
                })
                print(f"  ✗ biography.json - Invalid JSON")
        else:
            self.validation_results["errors"].append({
                "file": "biography.json",
                "message": "File not found"
            })
            print("  ✗ biography.json - NOT FOUND")
        
        # Check related articles
        related_file = self.raw_data_dir / "wikipedia" / "related_articles.json"
        if related_file.exists():
            try:
                with open(related_file, 'r', encoding='utf-8') as f:
                    articles = json.load(f)
                
                total_words = sum(article.get("word_count", 0) for article in articles)
                self.validation_results["checks"].append({
                    "check": "wikipedia_related",
                    "status": "pass",
                    "article_count": len(articles),
                    "total_words": total_words
                })
                print(f"  ✓ related_articles.json - {len(articles)} articles, {total_words:,} words")
                
            except json.JSONDecodeError as e:
                self.validation_results["errors"].append({
                    "file": "related_articles.json",
                    "message": f"Invalid JSON: {e}"
                })
                print(f"  ✗ related_articles.json - Invalid JSON")
        else:
            self.validation_results["warnings"].append({
                "file": "related_articles.json",
                "message": "File not found"
            })
            print("  ⚠ related_articles.json - NOT FOUND")
        
        print()
    
    def _calculate_statistics(self):
        """
        Calculate dataset statistics and token counts.
        """
        print("Calculating statistics...")
        
        total_words = 0
        total_sources = 0
        
        # Count Wikipedia words
        biography_file = self.raw_data_dir / "wikipedia" / "biography.json"
        if biography_file.exists():
            with open(biography_file, 'r', encoding='utf-8') as f:
                biography = json.load(f)
                total_words += biography.get("word_count", 0)
                total_sources += 1
        
        related_file = self.raw_data_dir / "wikipedia" / "related_articles.json"
        if related_file.exists():
            with open(related_file, 'r', encoding='utf-8') as f:
                articles = json.load(f)
                total_words += sum(article.get("word_count", 0) for article in articles)
                total_sources += len(articles)
        
        # Count speech words (if any collected)
        speeches_dir = self.raw_data_dir / "speeches"
        speech_words = 0
        speech_count = 0
        if speeches_dir.exists():
            for speech_file in speeches_dir.glob("*.json"):
                if speech_file.name != "speech_entry_template.json":
                    try:
                        with open(speech_file, 'r', encoding='utf-8') as f:
                            speech = json.load(f)
                            if "speeches" in speech:
                                for s in speech["speeches"]:
                                    speech_words += s.get("word_count", 0)
                                    speech_count += 1
                            elif "word_count" in speech:
                                speech_words += speech.get("word_count", 0)
                                speech_count += 1
                    except Exception:
                        continue
        
        total_words += speech_words
        total_sources += speech_count
        
        # Estimate tokens (1.3 words per token for English)
        estimated_tokens = int(total_words / 1.3)
        
        self.validation_results["statistics"] = {
            "total_sources": total_sources,
            "total_words": total_words,
            "estimated_tokens": estimated_tokens,
            "wikipedia_sources": total_sources - speech_count,
            "speech_sources": speech_count,
            "target_tokens": 75000,
            "progress_percent": round((estimated_tokens / 75000) * 100, 2),
            "tokens_remaining": max(0, 75000 - estimated_tokens)
        }
        
        stats = self.validation_results["statistics"]
        print(f"  Total sources: {stats['total_sources']}")
        print(f"  Total words: {stats['total_words']:,}")
        print(f"  Estimated tokens: {stats['estimated_tokens']:,}")
        print(f"  Progress: {stats['progress_percent']}% of 75K target")
        print()
    
    def _check_data_quality(self):
        """
        Perform quality checks on collected data.
        """
        print("Checking data quality...")
        
        quality_checks = []
        
        # Check 1: Sufficient content
        stats = self.validation_results["statistics"]
        if stats["estimated_tokens"] >= 75000:
            quality_checks.append(("Token target met", "pass"))
        elif stats["estimated_tokens"] >= 50000:
            quality_checks.append(("Token target", "warning", "50K-75K tokens collected"))
        else:
            quality_checks.append(("Token target", "fail", f"Only {stats['estimated_tokens']:,} tokens"))
        
        # Check 2: Source diversity
        if stats["wikipedia_sources"] > 0 and stats["speech_sources"] > 0:
            quality_checks.append(("Source diversity", "pass"))
        elif stats["wikipedia_sources"] > 0:
            quality_checks.append(("Source diversity", "warning", "Only Wikipedia sources"))
        else:
            quality_checks.append(("Source diversity", "fail", "Insufficient sources"))
        
        # Check 3: Metadata completeness
        metadata_file = self.raw_data_dir / "metadata" / "collection_log.json"
        if metadata_file.exists():
            quality_checks.append(("Metadata logging", "pass"))
        else:
            quality_checks.append(("Metadata logging", "warning", "No collection log"))
        
        # Print results
        for check in quality_checks:
            if len(check) == 2:
                name, status = check
                symbol = "✓" if status == "pass" else "✗"
                print(f"  {symbol} {name}")
            else:
                name, status, message = check
                if status == "pass":
                    print(f"  ✓ {name}")
                elif status == "warning":
                    print(f"  ⚠ {name}: {message}")
                else:
                    print(f"  ✗ {name}: {message}")
        
        print()
    
    def _print_summary(self):
        """
        Print validation summary.
        """
        print("="*70)
        print("VALIDATION SUMMARY")
        print("="*70)
        
        checks_passed = len([c for c in self.validation_results["checks"] if c.get("status") == "pass"])
        total_checks = len(self.validation_results["checks"])
        errors = len(self.validation_results["errors"])
        warnings = len(self.validation_results["warnings"])
        
        print(f"Checks passed: {checks_passed}/{total_checks}")
        print(f"Errors: {errors}")
        print(f"Warnings: {warnings}")
        print()
        
        stats = self.validation_results["statistics"]
        print("Dataset Progress:")
        print(f"  Current: {stats['estimated_tokens']:,} tokens")
        print(f"  Target: {stats['target_tokens']:,} tokens")
        print(f"  Progress: {stats['progress_percent']}%")
        print(f"  Remaining: {stats['tokens_remaining']:,} tokens")
        print()
        
        if stats['tokens_remaining'] > 0:
            print("Recommendations:")
            speeches_needed = int(stats['tokens_remaining'] / 600)  # Avg speech ~600 tokens
            print(f"  - Collect approximately {speeches_needed} more speeches")
            print(f"  - Focus on Christmas broadcasts (high quality, consistent format)")
            print(f"  - Consider state addresses and jubilee speeches")
        else:
            print("✓ Token target achieved!")
        
        print("="*70)
    
    def _save_report(self):
        """
        Save validation report to file.
        """
        report_file = self.raw_data_dir / "metadata" / "validation_report.json"
        with open(report_file, 'w', encoding='utf-8') as f:
            json.dump(self.validation_results, f, ensure_ascii=False, indent=2)
        
        print(f"\nValidation report saved to: {report_file}")


def main():
    """
    Main execution function.
    """
    script_dir = Path(__file__).parent
    dataset_root = script_dir.parent.parent.parent
    dataset_dir = dataset_root / "datasets" / "queen_elizabeth_ii"
    
    validator = DataValidator(str(dataset_dir))
    validator.validate_all()


if __name__ == "__main__":
    main()
