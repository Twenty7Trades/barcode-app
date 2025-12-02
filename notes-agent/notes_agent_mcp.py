#!/usr/bin/env python3
"""
Notes Agent MCP Server
Model Context Protocol server for session documentation across all projects
"""

import json
import os
import sys
import subprocess
from pathlib import Path
from datetime import datetime
from typing import Any, Dict, List, Optional

# MCP Server implementation
class NotesAgentMCPServer:
    def __init__(self):
        self.project_root = None
        self.config_path = None
        
    def detect_project_root(self, start_path: str = None) -> Optional[str]:
        """Detect project root by looking for notes-agent folder or config"""
        if start_path is None:
            start_path = os.getcwd()
            
        current = Path(start_path).resolve()
        
        # Look for notes-agent folder
        while current != current.parent:
            notes_agent = current / "notes-agent"
            if notes_agent.exists() and notes_agent.is_dir():
                return str(current)
            current = current.parent
            
        return None
    
    def ensure_project_setup(self, project_path: str = None) -> Dict[str, Any]:
        """Ensure project has notes-agent setup, initialize if needed"""
        if project_path is None:
            project_path = os.getcwd()
            
        project_path = Path(project_path).resolve()
        notes_agent_dir = project_path / "notes-agent"
        config_file = notes_agent_dir / "config.json"
        
        if not notes_agent_dir.exists():
            return {
                "status": "not_initialized",
                "message": f"Notes agent not found in {project_path}. Run 'notes-agent init' first.",
                "project_path": str(project_path)
            }
        
        if not config_file.exists():
            return {
                "status": "not_initialized",
                "message": f"Config file not found. Run 'notes-agent init' first.",
                "project_path": str(project_path)
            }
        
        try:
            with open(config_file) as f:
                config = json.load(f)
            return {
                "status": "ready",
                "project_path": str(project_path),
                "config": config
            }
        except Exception as e:
            return {
                "status": "error",
                "message": f"Error reading config: {e}",
                "project_path": str(project_path)
            }
    
    def add_session(self, session_data: Dict[str, Any], project_path: str = None) -> Dict[str, Any]:
        """Add a session entry to the project's notes"""
        setup = self.ensure_project_setup(project_path)
        
        if setup["status"] != "ready":
            return {
                "success": False,
                "error": setup.get("message", "Project not initialized")
            }
        
        project_path = setup["project_path"]
        notes_agent_js = Path(project_path) / "notes-agent" / "notes-agent.js"
        
        if not notes_agent_js.exists():
            return {
                "success": False,
                "error": "notes-agent.js not found"
            }
        
        # Ensure date is set
        if "date" not in session_data:
            session_data["date"] = datetime.now().strftime("%Y-%m-%d")
        
        # Convert to JSON string
        json_str = json.dumps(session_data)
        
        try:
            result = subprocess.run(
                ["node", str(notes_agent_js), "session", json_str],
                cwd=project_path,
                capture_output=True,
                text=True,
                check=True
            )
            
            return {
                "success": True,
                "message": "Session added successfully",
                "output": result.stdout.strip()
            }
        except subprocess.CalledProcessError as e:
            return {
                "success": False,
                "error": f"Error running notes-agent: {e.stderr}",
                "output": e.stdout
            }
    
    def get_summary(self, project_path: str = None) -> Dict[str, Any]:
        """Get project summary"""
        setup = self.ensure_project_setup(project_path)
        
        if setup["status"] != "ready":
            return {
                "success": False,
                "error": setup.get("message", "Project not initialized")
            }
        
        project_path = setup["project_path"]
        notes_agent_js = Path(project_path) / "notes-agent" / "notes-agent.js"
        
        try:
            result = subprocess.run(
                ["node", str(notes_agent_js), "summary"],
                cwd=project_path,
                capture_output=True,
                text=True,
                check=True
            )
            
            return {
                "success": True,
                "summary": result.stdout.strip(),
                "config": setup.get("config", {})
            }
        except subprocess.CalledProcessError as e:
            return {
                "success": False,
                "error": f"Error running notes-agent: {e.stderr}"
            }
    
    def initialize_project(self, project_path: str = None, project_type: str = None) -> Dict[str, Any]:
        """Initialize notes-agent in a project"""
        if project_path is None:
            project_path = os.getcwd()
        
        project_path = Path(project_path).resolve()
        notes_agent_dir = project_path / "notes-agent"
        
        # Check if already initialized
        if notes_agent_dir.exists():
            return {
                "success": False,
                "error": "Project already initialized. Use 'notes-agent update' to refresh."
            }
        
        # Copy notes-agent from global location
        global_notes_agent = Path(__file__).parent / "notes-agent"
        if not global_notes_agent.exists():
            return {
                "success": False,
                "error": "Global notes-agent not found. Please install notes-agent globally first."
            }
        
        # Copy files
        import shutil
        try:
            shutil.copytree(global_notes_agent, notes_agent_dir)
            
            # Initialize config
            notes_agent_js = notes_agent_dir / "notes-agent.js"
            if project_type:
                # Non-interactive init
                config = {
                    "projectName": project_path.name,
                    "projectType": project_type,
                    "urls": {},
                    "credentials": {},
                    "notes": [],
                    "sessions": [],
                    "deployments": [],
                    "troubleshooting": [],
                    "commands": [],
                    "documentation": []
                }
                config_file = notes_agent_dir / "config.json"
                with open(config_file, "w") as f:
                    json.dump(config, f, indent=2)
            else:
                # Interactive init
                subprocess.run(
                    ["node", str(notes_agent_js), "init"],
                    cwd=project_path,
                    check=False
                )
            
            return {
                "success": True,
                "message": f"Notes agent initialized in {project_path}",
                "project_path": str(project_path)
            }
        except Exception as e:
            return {
                "success": False,
                "error": f"Error initializing: {e}"
            }


# CLI Interface
def main():
    import argparse
    
    parser = argparse.ArgumentParser(description="Notes Agent - Session Documentation Tool")
    parser.add_argument("command", choices=["init", "session", "summary", "update", "mcp"], 
                       help="Command to execute")
    parser.add_argument("--project", "-p", help="Project path (default: current directory)")
    parser.add_argument("--type", "-t", help="Project type (for init)")
    parser.add_argument("--json", "-j", help="JSON input for session command")
    
    args = parser.parse_args()
    
    server = NotesAgentMCPServer()
    project_path = args.project or os.getcwd()
    
    if args.command == "init":
        result = server.initialize_project(project_path, args.type)
        if result["success"]:
            print(f"✅ {result['message']}")
        else:
            print(f"❌ {result['error']}")
            sys.exit(1)
    
    elif args.command == "session":
        if args.json:
            session_data = json.loads(args.json)
            result = server.add_session(session_data, project_path)
            if result["success"]:
                print(result["message"])
            else:
                print(f"❌ {result['error']}")
                sys.exit(1)
        else:
            print("Usage: notes-agent session --json '{\"title\":\"...\"}'")
            print("Or use interactive mode: node notes-agent/notes-agent.js session")
            sys.exit(1)
    
    elif args.command == "summary":
        result = server.get_summary(project_path)
        if result["success"]:
            print(result["summary"])
        else:
            print(f"❌ {result['error']}")
            sys.exit(1)
    
    elif args.command == "update":
        setup = server.ensure_project_setup(project_path)
        if setup["status"] != "ready":
            print(f"❌ {setup.get('message', 'Project not initialized')}")
            sys.exit(1)
        
        notes_agent_js = Path(setup["project_path"]) / "notes-agent" / "notes-agent.js"
        subprocess.run(["node", str(notes_agent_js), "update"], cwd=setup["project_path"])
    
    elif args.command == "mcp":
        # MCP server mode
        print("Starting MCP server...", file=sys.stderr)
        # MCP server implementation would go here
        # For now, just run the CLI
        pass


if __name__ == "__main__":
    main()


