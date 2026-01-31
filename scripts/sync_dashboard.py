import csv
import json
import os
import shutil
import sys
import re

def sync_dashboard(csv_path):
    print(f"Syncing dashboard with data from {csv_path}...")
    
    # Paths
    base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    dashboard_js_path = os.path.join(base_dir, "Dashboard", "js", "data.js")
    images_dest_dir = os.path.join(base_dir, "Dashboard", "images", "agents")
    
    if not os.path.exists(dashboard_js_path):
        print(f"Error: Dashboard data file not found at {dashboard_js_path}")
        return

    if not os.path.exists(images_dest_dir):
        os.makedirs(images_dest_dir)

    # Read CSV
    agents = {}
    try:
        with open(csv_path, 'r') as f:
            reader = csv.DictReader(f)
            for row in reader:
                role = row['Role'].strip()
                key = role.lower().split(' ')[0] # 'Chairman (Cedric)' -> 'chairman'
                if key == 'chairman': key = 'chairman' # Explicit check just in case
                
                # Normalize keys for dashboard (some might be different)
                if key == 'chief': key = 'ceo' # Fallback
                
                # Check for special content
                notes = row.get('Notes', '')
                backstory = row.get('Backstory', '')
                image_path = row.get('ImagePath', '')
                
                # Personality
                enneagram = f"Type {row.get('Enneagram', '?')} ({row.get('Wing', '?')})"
                mbti = row.get('MBTI', '?')
                western = row.get('Western Zodiac', '?')
                chinese = row.get('Chinese Zodiac', '?')
                
                agents[key] = {
                    'role_name': role,
                    'enneagram': enneagram,
                    'mbti': mbti,
                    'western': western,
                    'chinese': chinese,
                    'notes': notes,
                    'backstory': backstory,
                    'image_path_src': image_path
                }
    except Exception as e:
        print(f"Error reading CSV: {e}")
        return

    # Read existing JS
    with open(dashboard_js_path, 'r') as f:
        js_content = f.read()

    # Regex to find AGENTS object
    # Matches: const AGENTS = { ... };
    # We need to capture the content inside to parse/replace carefully or just replace whole block
    # Replacing structured block is safer if we reconstruct it
    
    # We will build a new AGENTS block text
    # We need to preserve the static fields like 'icon', 'accentColor' which are NOT in CSV
    # So we must parse the existing JS object to extract those.
    
    # Simple parsing of the JS object is hard with regex. 
    # Strategy: Iterate over keys in the JS content and replace specific fields.
    
    new_js_content = js_content
    
    for key, data in agents.items():
        # Find the agent block in JS
        # key: { ... }
        # detailed pattern: key\s*:\s*\{[^}]+\}
        # This is risky if nested braces. 
        # But AGENTS object is flat depth 1 agents, depth 2 props.
        
        # Better approach: Use known keys (ceo, cfo, etc.) and replace properties inside.
        
        print(f"Updating {key}...")
        
        # 1. Update Personality
        # pattern: personality:\s*\{\s*enneagram:\s*"[^"]*",\s*mbti:\s*"[^"]*",\s*western:\s*"[^"]*",\s*chinese:\s*"[^"]*"\s*\}
        # We can construct the new string
        
        new_personality = f'''personality: {{
            enneagram: "{data['enneagram']}",
            mbti: "{data['mbti']}",
            western: "{data['western']}",
            chinese: "{data['chinese']}"
        }}'''
        
        # Regex to find the personality block for this key
        # We look for 'key:', then content, then 'personality: {'
        
        # Let's try to replace specific lines first.
        # This assumes formatting is somewhat consistent (which it is, verified by view_file)
        
        # Find start of agent block
        agent_start_idx = new_js_content.find(f"{key}: {{")
        if agent_start_idx == -1:
            print(f"Warning: Agent {key} not found in data.js")
            continue
            
        # Find end of agent block (next "}," or end of file)
        # simplistic: look for "sampleVoice:" as an anchor or "imagePath:"
        
        # Update Personality Block
        # We can regex replace inside the substring from agent_start
        # Look for personality: { ... } inside this agent's scope
        
        # Let's do a targeted replace for this agent's personality
        # We need a regex that matches THIS agent's personality block.
        # Pattern: (key:\s*\{[\s\S]*?personality:\s*\{)([\s\S]*?)(\})
        
        pattern_pers = r'(' + key + r':\s*\{[\s\S]*?personality:\s*\{)([\s\S]*?)(\})'
        match = re.search(pattern_pers, new_js_content)
        if match:
            # We construct the inner content
            inner_new = f'\n            enneagram: "{data["enneagram"]}",\n            mbti: "{data["mbti"]}",\n            western: "{data["western"]}",\n            chinese: "{data["chinese"]}"\n        '
            # Replace
            new_js_content = new_js_content.replace(match.group(0), f"{match.group(1)}{inner_new}{match.group(3)}")
        
        # Update CommStyle if backstory is better? 
        # Use Notes + Backstory snippet
        if data['backstory']:
            # Maybe append? or Replace?
            # User wants CSV to drive it.
            # Let's append Backstory to Notes and use as CommStyle
            new_comm = f"{data['notes']}. {data['backstory']}".replace('"', '\\"').strip()
            # Truncate if too long?
             
            # pattern_comm = r'(' + key + r':\s*\{[\s\S]*?commStyle:\s*")([^"]*)(")'
            # match_comm = re.search(pattern_comm, new_js_content)
            # if match_comm:
            #     new_js_content = new_js_content.replace(match_comm.group(0), f'{match_comm.group(1)}{new_comm}{match_comm.group(3)}')
            pass # Skipping comm style update for now to preserve hand-written quality unless user asks
            
        # Handle Image
        src_path = data['image_path_src']
        if src_path and os.path.exists(src_path):
            filename = f"{key}.png"
            dest_path = os.path.join(images_dest_dir, filename)
            shutil.copy2(src_path, dest_path)
            print(f"Copied image to {dest_path}")
            
            # Update path in JS just in case (though it defaults to right path)
            rel_path = f"images/agents/{filename}"
            pattern_img = r'(' + key + r':\s*\{[\s\S]*?imagePath:\s*")([^"]*)(")'
            match_img = re.search(pattern_img, new_js_content)
            if match_img:
                new_js_content = new_js_content.replace(match_img.group(0), f'{match_img.group(1)}{rel_path}{match_img.group(3)}')

    # Write back
    with open(dashboard_js_path, 'w') as f:
        f.write(new_js_content)
        
    print("Dashboard data.js updated successfully.")

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python sync_dashboard.py <csv_path>")
        sys.exit(1)
    
    sync_dashboard(sys.argv[1])
