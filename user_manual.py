#!/usr/bin/env python3
"""
user-manual: Manage persistent user profile (USER.md) with Novyx memory integration.
v2 SDK compatible with proper exception handling.
"""
import sys
import os
import argparse
import datetime
from pathlib import Path

# Novyx v2 SDK with proper exceptions
try:
    from novyx import Novyx, NovyxUpgradeRequired, NovyxAuthError
    NOVYX_AVAILABLE = True
except ImportError:
    NOVYX_AVAILABLE = False

USER_MD_PATH = Path("USER.md")
NOVYX_KEY_PATH = Path.home() / ".novyx_key"

def get_novyx_client():
    """Initialize Novyx client with error handling."""
    if not NOVYX_AVAILABLE:
        return None
    
    api_key = os.environ.get("NOVYX_API_KEY")
    if not api_key and NOVYX_KEY_PATH.exists():
        with open(NOVYX_KEY_PATH, "r") as f:
            api_key = f.read().strip()
    
    if not api_key:
        return None
        
    return Novyx(api_key=api_key)

def init_profile():
    """Create USER.md if it doesn't exist."""
    if not USER_MD_PATH.exists():
        with open(USER_MD_PATH, "w") as f:
            f.write(f"# User Profile\n\n## Identity\n- Name: User\n- Created: {datetime.datetime.now().isoformat()}\n\n## Preferences\n- Language: English\n\n## Context\n- Project: None\n")
        print(f"Created new profile at {USER_MD_PATH}")

def read_profile():
    """Read the full profile content."""
    init_profile()
    with open(USER_MD_PATH, "r") as f:
        return f.read()

def update_profile(content, section=None):
    """Append content and sync to Novyx."""
    init_profile()
    
    timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    update_text = f"\n- [{timestamp}] {content}"

    with open(USER_MD_PATH, "a") as f:
        f.write(update_text)
    
    print(f"Updated local profile: {USER_MD_PATH}")
    
    # Sync to Novyx
    client = get_novyx_client()
    if client:
        try:
            result = client.remember(f"User Profile Update: {content}")
            memory_id = result.get('uuid', 'unknown')
            print(f"Synced to Novyx (ID: {memory_id})")
        except NovyxUpgradeRequired as e:
            print(f"⚠️ Upgrade required: {e}")
            print("   Novyx features disabled. Continue locally.")
        except NovyxAuthError as e:
            print(f"⚠️ Auth error: {e}")
            print("   Check your API key.")
        except Exception as e:
            print(f"Warning: Novyx sync failed: {e}")
    else:
        print("Note: Novyx not configured. Profile stored locally only.")

def find_in_profile(query):
    """Search USER.md and Novyx."""
    init_profile()
    
    print(f"Searching local profile for '{query}'...")
    with open(USER_MD_PATH, "r") as f:
        lines = f.readlines()
        found = [line.strip() for line in lines if query.lower() in line.lower()]
        
    if found:
        print("\nLocal Matches:")
        for match in found:
            print(f"- {match}")
    else:
        print("No local matches found.")

    # Search Novyx
    client = get_novyx_client()
    if client:
        print(f"\nSearching Novyx for '{query}'...")
        try:
            results = client.recall(query)
            if results:
                print("\nNovyx Matches:")
                for res in results:
                    print(f"- {res.get('observation', '')[:80]} (Score: {res.get('score', 0):.2f})")
            else:
                print("No remote matches.")
        except NovyxUpgradeRequired as e:
            print(f"⚠️ Upgrade required for recall: {e}")
        except Exception as e:
            print(f"Error querying Novyx: {e}")

def show_stats():
    """Show memory usage and profile stats."""
    init_profile()
    
    # Local stats
    size_bytes = USER_MD_PATH.stat().st_size
    last_modified = datetime.datetime.fromtimestamp(USER_MD_PATH.stat().st_mtime)
    
    with open(USER_MD_PATH, "r") as f:
        content = f.read()
        lines = content.splitlines()
        sections = [line for line in lines if line.startswith("## ")]
        entries = [line for line in lines if line.strip().startswith("-")]

    print("\n📊 User Manual Stats")
    print(f"-------------------")
    print(f"Local Profile: {USER_MD_PATH}")
    print(f"Size: {size_bytes} bytes")
    print(f"Last Updated: {last_modified}")
    print(f"Sections: {len(sections)}")
    print(f"Entries: {len(entries)}")

    # Novyx stats
    client = get_novyx_client()
    if client:
        try:
            usage = client.usage()
            if usage:
                tier = usage.get('tier', 'Unknown')
                used = usage.get('usage', {}).get('memories_stored', 'N/A')
                limit = usage.get('usage', {}).get('memory_limit', 'N/A')
                print(f"\n☁️ Novyx Cloud")
                print(f"Tier: {tier}")
                print(f"Memories: {used} / {limit}")
            else:
                print(f"\n☁️ Novyx: Connected (stats unavailable)")
        except NovyxUpgradeRequired as e:
            print(f"\n☁️ Novyx: Upgrade required for stats")
        except Exception as e:
            print(f"\n☁️ Novyx: Error ({e})")
    else:
        print("\n☁️ Novyx: Not configured")

def main():
    parser = argparse.ArgumentParser(description="Manage persistent user profile.")
    subparsers = parser.add_subparsers(dest="command", help="Command to run")

    subparsers.add_parser("read", help="Read the full profile")
    
    update_parser = subparsers.add_parser("update", help="Update the profile")
    update_parser.add_argument("content", help="Content to add")
    
    find_parser = subparsers.add_parser("find", help="Find in profile")
    find_parser.add_argument("query", help="Search query")

    subparsers.add_parser("stats", help="Show profile stats")

    args = parser.parse_args()

    if args.command == "read":
        print(read_profile())
    elif args.command == "update":
        update_profile(args.content)
    elif args.command == "find":
        find_in_profile(args.query)
    elif args.command == "stats":
        show_stats()
    else:
        parser.print_help()

if __name__ == "__main__":
    main()
