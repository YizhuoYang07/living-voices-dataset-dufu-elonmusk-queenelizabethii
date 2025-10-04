"""
Queen Elizabeth II Dataset - Final Verification Script

This script performs comprehensive verification of the completed dataset,
checking all files, validating data integrity, and generating a final report.

Author: Living Voices Project
Date: 2024-10-04
"""

import json
from datetime import datetime
from pathlib import Path
from typing import Dict, List


class DatasetVerifier:
    """
    Comprehensive verification for Queen Elizabeth II dataset.
    """
    
    def __init__(self, dataset_dir: str):
        """
        Initialize the verifier.
        
        Args:
            dataset_dir: Root directory of the dataset
        """
        self.dataset_dir = Path(dataset_dir)
        self.verification_results = {
            "timestamp": datetime.now().isoformat(),
            "checks": [],
            "errors": [],
            "warnings": [],
            "summary": {}
        }
    
    def verify_all(self):
        """
        Run all verification checks.
        """
        print("="*70)
        print("Queen Elizabeth II Dataset - Final Verification")
        print("="*70)
        print()
        
        # Check 1: Directory structure
        print("1. Verifying directory structure...")
        self._check_directories()
        
        # Check 2: Raw data files
        print("\n2. Verifying raw data files...")
        self._check_raw_data()
        
        # Check 3: Processed data files
        print("\n3. Verifying processed data files...")
        self._check_processed_data()
        
        # Check 4: Documentation files
        print("\n4. Verifying documentation files...")
        self._check_documentation()
        
        # Check 5: Data consistency
        print("\n5. Verifying data consistency...")
        self._check_data_consistency()
        
        # Check 6: Quality metrics
        print("\n6. Calculating quality metrics...")
        self._calculate_quality_metrics()
        
        # Generate final report
        print("\n7. Generating final verification report...")
        self._generate_final_report()
        
        # Print summary
        self._print_summary()
    
    def _check_directories(self):
        """
        Verify all required directories exist.
        """
        required_dirs = [
            "raw_data",
            "raw_data/wikipedia",
            "raw_data/speeches",
            "raw_data/metadata",
            "processed_data"
        ]
        
        for dir_name in required_dirs:
            dir_path = self.dataset_dir / dir_name
            if dir_path.exists():
                self.verification_results["checks"].append({
                    "check": "directory_structure",
                    "item": dir_name,
                    "status": "pass"
                })
                print(f"  ✓ {dir_name}/")
            else:
                self.verification_results["errors"].append({
                    "check": "directory_structure",
                    "item": dir_name,
                    "message": "Directory not found"
                })
                print(f"  ✗ {dir_name}/ - NOT FOUND")
    
    def _check_raw_data(self):
        """
        Verify raw data files.
        """
        files_to_check = [
            ("raw_data/wikipedia/biography.json", "Biography"),
            ("raw_data/wikipedia/related_articles.json", "Related articles"),
            ("raw_data/metadata/collection_log.json", "Collection log"),
            ("raw_data/metadata/validation_report.json", "Validation report")
        ]
        
        for file_path, description in files_to_check:
            full_path = self.dataset_dir / file_path
            if full_path.exists():
                try:
                    with open(full_path, 'r', encoding='utf-8') as f:
                        data = json.load(f)
                    
                    file_size = full_path.stat().st_size / 1024  # KB
                    self.verification_results["checks"].append({
                        "check": "raw_data_file",
                        "item": description,
                        "status": "pass",
                        "size_kb": round(file_size, 2)
                    })
                    print(f"  ✓ {description}: {file_size:.2f} KB")
                    
                except json.JSONDecodeError:
                    self.verification_results["errors"].append({
                        "check": "raw_data_file",
                        "item": description,
                        "message": "Invalid JSON"
                    })
                    print(f"  ✗ {description}: Invalid JSON")
            else:
                self.verification_results["errors"].append({
                    "check": "raw_data_file",
                    "item": description,
                    "message": "File not found"
                })
                print(f"  ✗ {description}: NOT FOUND")
    
    def _check_processed_data(self):
        """
        Verify processed data files.
        """
        files_to_check = [
            ("processed_data/structured_documents.json", "Structured documents"),
            ("processed_data/training_chunks.json", "Training chunks"),
            ("processed_data/dataset_metadata.json", "Dataset metadata"),
            ("processed_data/processing_report.json", "Processing report")
        ]
        
        for file_path, description in files_to_check:
            full_path = self.dataset_dir / file_path
            if full_path.exists():
                try:
                    with open(full_path, 'r', encoding='utf-8') as f:
                        data = json.load(f)
                    
                    file_size = full_path.stat().st_size / 1024  # KB
                    self.verification_results["checks"].append({
                        "check": "processed_data_file",
                        "item": description,
                        "status": "pass",
                        "size_kb": round(file_size, 2)
                    })
                    print(f"  ✓ {description}: {file_size:.2f} KB")
                    
                except json.JSONDecodeError:
                    self.verification_results["errors"].append({
                        "check": "processed_data_file",
                        "item": description,
                        "message": "Invalid JSON"
                    })
                    print(f"  ✗ {description}: Invalid JSON")
            else:
                self.verification_results["errors"].append({
                    "check": "processed_data_file",
                    "item": description,
                    "message": "File not found"
                })
                print(f"  ✗ {description}: NOT FOUND")
    
    def _check_documentation(self):
        """
        Verify documentation files.
        """
        doc_files = [
            ("README.md", "Main README"),
            ("PROJECT_SUMMARY.md", "Project summary"),
            ("COLLECTION_COMPLETE.md", "Collection report"),
            ("QUICK_REFERENCE.md", "Quick reference")
        ]
        
        for file_name, description in doc_files:
            file_path = self.dataset_dir / file_name
            if file_path.exists():
                file_size = file_path.stat().st_size / 1024  # KB
                self.verification_results["checks"].append({
                    "check": "documentation",
                    "item": description,
                    "status": "pass",
                    "size_kb": round(file_size, 2)
                })
                print(f"  ✓ {description}: {file_size:.2f} KB")
            else:
                self.verification_results["warnings"].append({
                    "check": "documentation",
                    "item": description,
                    "message": "File not found"
                })
                print(f"  ⚠ {description}: NOT FOUND")
    
    def _check_data_consistency(self):
        """
        Verify data consistency across files.
        """
        # Load key files
        bio_file = self.dataset_dir / "raw_data/wikipedia/biography.json"
        articles_file = self.dataset_dir / "raw_data/wikipedia/related_articles.json"
        chunks_file = self.dataset_dir / "processed_data/training_chunks.json"
        docs_file = self.dataset_dir / "processed_data/structured_documents.json"
        
        try:
            with open(bio_file, 'r', encoding='utf-8') as f:
                biography = json.load(f)
            
            with open(articles_file, 'r', encoding='utf-8') as f:
                articles = json.load(f)
            
            with open(chunks_file, 'r', encoding='utf-8') as f:
                chunks = json.load(f)
            
            with open(docs_file, 'r', encoding='utf-8') as f:
                documents = json.load(f)
            
            # Check: Number of documents
            expected_docs = 1 + len(articles)  # biography + articles
            if len(documents) == expected_docs:
                print(f"  ✓ Document count: {len(documents)} (expected {expected_docs})")
                self.verification_results["checks"].append({
                    "check": "data_consistency",
                    "item": "document_count",
                    "status": "pass"
                })
            else:
                print(f"  ✗ Document count mismatch: {len(documents)} vs {expected_docs}")
                self.verification_results["errors"].append({
                    "check": "data_consistency",
                    "item": "document_count",
                    "message": f"Expected {expected_docs}, got {len(documents)}"
                })
            
            # Check: Chunks exist for all documents
            chunk_doc_ids = set(chunk['document_id'] for chunk in chunks)
            doc_ids = set(doc['id'] for doc in documents)
            
            if chunk_doc_ids == doc_ids:
                print(f"  ✓ All documents have chunks")
                self.verification_results["checks"].append({
                    "check": "data_consistency",
                    "item": "chunk_coverage",
                    "status": "pass"
                })
            else:
                print(f"  ✗ Chunk coverage incomplete")
                self.verification_results["errors"].append({
                    "check": "data_consistency",
                    "item": "chunk_coverage",
                    "message": "Some documents missing chunks"
                })
            
        except Exception as e:
            print(f"  ✗ Error checking consistency: {e}")
            self.verification_results["errors"].append({
                "check": "data_consistency",
                "message": str(e)
            })
    
    def _calculate_quality_metrics(self):
        """
        Calculate final quality metrics.
        """
        try:
            # Load validation report
            validation_file = self.dataset_dir / "raw_data/metadata/validation_report.json"
            with open(validation_file, 'r', encoding='utf-8') as f:
                validation = json.load(f)
            
            stats = validation.get("statistics", {})
            
            print(f"  Token count: {stats.get('estimated_tokens', 0):,}")
            print(f"  Token target: {stats.get('target_tokens', 0):,}")
            print(f"  Progress: {stats.get('progress_percent', 0)}%")
            print(f"  Sources: {stats.get('total_sources', 0)}")
            
            self.verification_results["summary"] = {
                "tokens_collected": stats.get('estimated_tokens', 0),
                "token_target": stats.get('target_tokens', 0),
                "progress_percent": stats.get('progress_percent', 0),
                "total_sources": stats.get('total_sources', 0)
            }
            
        except Exception as e:
            print(f"  ✗ Error calculating metrics: {e}")
    
    def _generate_final_report(self):
        """
        Generate and save final verification report.
        """
        report_file = self.dataset_dir / "VERIFICATION_REPORT.json"
        
        self.verification_results["final_status"] = {
            "checks_passed": len([c for c in self.verification_results["checks"] if c.get("status") == "pass"]),
            "total_checks": len(self.verification_results["checks"]),
            "errors": len(self.verification_results["errors"]),
            "warnings": len(self.verification_results["warnings"]),
            "dataset_ready": len(self.verification_results["errors"]) == 0
        }
        
        with open(report_file, 'w', encoding='utf-8') as f:
            json.dump(self.verification_results, f, ensure_ascii=False, indent=2)
        
        print(f"  ✓ Saved verification report: VERIFICATION_REPORT.json")
    
    def _print_summary(self):
        """
        Print verification summary.
        """
        final = self.verification_results["final_status"]
        
        print("\n" + "="*70)
        print("FINAL VERIFICATION SUMMARY")
        print("="*70)
        print(f"Checks Passed:  {final['checks_passed']}/{final['total_checks']}")
        print(f"Errors:         {final['errors']}")
        print(f"Warnings:       {final['warnings']}")
        print()
        
        summary = self.verification_results["summary"]
        if summary:
            print(f"Token Count:    {summary.get('tokens_collected', 0):,} / {summary.get('token_target', 0):,}")
            print(f"Progress:       {summary.get('progress_percent', 0)}%")
            print(f"Total Sources:  {summary.get('total_sources', 0)}")
            print()
        
        if final["dataset_ready"]:
            print("✅ DATASET VERIFICATION PASSED")
            print("   The dataset is complete and ready for use!")
        else:
            print("⚠️ DATASET VERIFICATION ISSUES DETECTED")
            print(f"   Found {final['errors']} error(s) that need attention.")
        
        print("="*70)


def main():
    """
    Main execution function.
    """
    script_dir = Path(__file__).parent
    dataset_root = script_dir.parent.parent.parent
    dataset_dir = dataset_root / "datasets" / "queen_elizabeth_ii"
    
    verifier = DatasetVerifier(str(dataset_dir))
    verifier.verify_all()


if __name__ == "__main__":
    main()
