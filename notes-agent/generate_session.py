#!/usr/bin/env python3
"""
Session Summary Generator - Auto-generates session summaries from chat history
Usage: python notes-agent/generate_session.py
"""

import json
import subprocess
import sys
from datetime import datetime
from pathlib import Path

def generate_session_summary():
    """
    Generate a session summary based on the current conversation context.
    This function should be called by the AI assistant with details about the session.
    """
    
    # Get session data from command line arguments or stdin
    if len(sys.argv) > 1:
        try:
            session_data = json.loads(sys.argv[1])
        except json.JSONDecodeError:
            print("❌ Invalid JSON provided", file=sys.stderr)
            sys.exit(1)
    else:
        # Try to read from stdin
        try:
            session_data = json.load(sys.stdin)
        except (json.JSONDecodeError, EOFError):
            print("❌ No valid JSON input provided", file=sys.stderr)
            print("\nUsage:")
            print("  python notes-agent/generate_session.py '{\"title\":\"...\",\"summary\":\"...\"}'")
            print("  echo '{\"title\":\"...\"}' | python notes-agent/generate_session.py")
            sys.exit(1)
    
    # Ensure date is set
    if 'date' not in session_data:
        session_data['date'] = datetime.now().strftime('%Y-%m-%d')
    
    # Convert to JSON string for Node.js script
    json_str = json.dumps(session_data)
    
    # Call the Node.js script with JSON input
    script_path = Path(__file__).parent / 'notes-agent.js'
    project_root = Path(__file__).parent.parent
    
    try:
        result = subprocess.run(
            ['node', str(script_path), 'session', json_str],
            cwd=str(project_root),
            capture_output=True,
            text=True,
            check=True
        )
        print(result.stdout)
        return 0
    except subprocess.CalledProcessError as e:
        print(f"❌ Error running notes agent: {e.stderr}", file=sys.stderr)
        return 1

if __name__ == '__main__':
    sys.exit(generate_session_summary())


