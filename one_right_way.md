# One Right Way: Script Development Guidelines

## Core Principles

1. **One Right Way**
   - Each script should have a single, clear way to accomplish its task
   - Avoid configuration options when possible
   - Use sensible defaults that work for the most common case

2. **Self-Contained**
   - Each script should include all necessary configuration in its directory
   - Use a local `.env` file for environment-specific settings
   - Never modify files in `works-do-not-modify/`

3. **Documentation First**
   - Every script starts with a clear docstring
   - Document requirements, dependencies, and usage examples
   - Keep documentation up-to-date with the code

## File Structure

```
scripts/
  airtable/
    .env                    # Local config (not in version control)
    script_name.py          # Main script
    works-do-not-modify/    # Reference copies (never modified)
      script_name.py
      .env.example
```

## Environment Configuration

### .env File
Create a `.env` file in the same directory as the script with these variables:

```bash
# Airtable Configuration
AIRTABLE_API_KEY=your_api_key_here
AIRTABLE_BASE_ID=your_base_id_here
```

### Loading Environment
Use this pattern to load environment variables:

```python
import os
from pathlib import Path
from dotenv import load_dotenv

# Load environment
script_dir = Path(__file__).parent
env_path = script_dir / '.env'
if not env_path.exists():
    print(f"Error: .env file not found at {env_path}")
    print("Please create it with the required variables (see one_right_way.md)")
    exit(1)
load_dotenv(env_path)

# Access variables
API_KEY = os.getenv('AIRTABLE_API_KEY')
BASE_ID = os.getenv('AIRTABLE_BASE_ID')
```

## Script Template

```python
"""
Script purpose in one line.

More detailed description if needed.

Requirements:
- .env file in same directory with required variables
- List any other dependencies here

Example usage:
    python script_name.py
"""

import os
from pathlib import Path
from dotenv import load_dotenv

# --- Configuration ---
# Load environment
script_dir = Path(__file__).parent
env_path = script_dir / '.env'
if not env_path.exists():
    print(f"Error: .env file not found at {env_path}")
    exit(1)
load_dotenv(env_path)

# Constants
CONSTANT_VALUE = "example"

# --- Main Function ---
def main():
    """Main function with core logic."""
    print(f"Running with {CONSTANT_VALUE}")

if __name__ == "__main__":
    main()
```

## Best Practices

1. **Error Handling**
   - Fail fast with clear error messages
   - Validate required environment variables on startup
   - Use try/except blocks for expected failures

2. **Logging**
   - Use print() for user-facing messages
   - Include progress indicators for long-running operations
   - Format output for easy reading

3. **Code Style**
   - Follow PEP 8
   - Use type hints for function signatures
   - Keep functions small and focused
   - Use meaningful variable names

4. **Documentation**
   - Document the "why" not just the "what"
   - Include example input/output in docstrings
   - Update documentation when changing behavior

## When to Create a New Script

Create a new script when:
- The new functionality is significantly different
- The script would become too complex with the new feature
- The script would require many new configuration options

Otherwise, extend the existing script following the established patterns.
