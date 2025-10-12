"""
Master script to generate all figures for the report
Runs all visualization scripts in sequence

Usage:
    python generate_all_figures.py
"""

import subprocess
import sys
import os
from pathlib import Path

# Color codes for terminal output
GREEN = '\033[92m'
BLUE = '\033[94m'
RED = '\033[91m'
RESET = '\033[0m'

print(f"{BLUE}{'='*60}")
print("Living Voices Dataset - Report Figure Generator")
print(f"{'='*60}{RESET}\n")

# Create figures directory if it doesn't exist
figures_dir = Path(__file__).parent.parent.parent / 'figures'
figures_dir.mkdir(exist_ok=True)
print(f"{GREEN}✓{RESET} Figures directory ready: {figures_dir}\n")

# List of visualization scripts to run
scripts = [
    'figure_3_1_hierarchical_structure.py',
    'figure_3_2_metadata_records.py',
    'figure_3_3_collection_pipelines.py',
    'figure_3_4_poem_chunk_structure.py'
]

# Run each script
success_count = 0
failed_scripts = []

for script in scripts:
    script_path = Path(__file__).parent / script
    print(f"{BLUE}Running:{RESET} {script}")
    
    try:
        result = subprocess.run(
            [sys.executable, str(script_path)],
            capture_output=True,
            text=True,
            check=True
        )
        print(result.stdout)
        success_count += 1
    except subprocess.CalledProcessError as e:
        print(f"{RED}✗ Failed:{RESET} {script}")
        print(f"Error: {e.stderr}")
        failed_scripts.append(script)
    except Exception as e:
        print(f"{RED}✗ Error running {script}:{RESET} {str(e)}")
        failed_scripts.append(script)

# Summary
print(f"\n{BLUE}{'='*60}")
print("Generation Summary")
print(f"{'='*60}{RESET}")
print(f"{GREEN}✓ Success:{RESET} {success_count}/{len(scripts)} figures generated")

if failed_scripts:
    print(f"\n{RED}✗ Failed scripts:{RESET}")
    for script in failed_scripts:
        print(f"  - {script}")
else:
    print(f"\n{GREEN}🎉 All figures generated successfully!{RESET}")
    print(f"\nFigures saved to: {figures_dir}")
    print("\nFigure placement in report:")
    print("  • Figure 3.1: After 'We chose these personas deliberately...' paragraph")
    print("  • Figure 3.2: After Table 3.2 (Metadata Schema Architecture)")
    print("  • Figure 3.3: After 'This achieved 99.5% extraction accuracy.' paragraph")
    print("  • Figure 3.4: After 'This proved essential...' paragraph in section 3.3")
