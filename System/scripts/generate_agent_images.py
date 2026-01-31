#!/usr/bin/env python3
"""
Generate agent avatar images using OpenRouter (Gemini) with DALL-E fallback.

Primary: OpenRouter → Gemini (for image prompts)
Fallback: OpenAI DALL-E (for actual image generation)

Usage:
    python scripts/generate_agent_images.py
    python scripts/generate_agent_images.py --factory factory_001
    
Requirements:
    pip install python-dotenv requests
"""

import argparse
import os
import sys
import requests
from pathlib import Path

# Add System to path (so we can import lib)
sys.path.insert(0, str(Path(__file__).parent.parent))

# Load environment variables
try:
    from dotenv import load_dotenv
    # Root is parent.parent.parent (System/intro/root)
    project_root = Path(__file__).parent.parent.parent
    env_file = project_root / '.env.local'
    if env_file.exists():
        load_dotenv(env_file)
        print(f"✓ Loaded environment from {env_file}")
    else:
        load_dotenv(project_root / '.env')
except ImportError:
    print("Note: python-dotenv not installed, using system environment variables")


# Output directory (Dashboard is in System, same level as scripts is incorrect, scripts is in System/scripts)
# Root/System/scripts/generate_agent_images.py
# parent = scripts
# parent.parent = System
# Dashboard is System/Dashboard.
OUTPUT_DIR = Path(__file__).parent.parent / 'Dashboard' / 'public' / 'images' / 'agents'


# Agent definitions with role-specific styling
AGENTS = {
    'chairman': {
        'color': 'gold and bronze',
        'theme': 'crown, leadership, authority',
        'description': 'Chairman of the Board AI agent'
    },
    'ceo': {
        'color': 'royal blue',
        'theme': 'target, vision, strategy',
        'description': 'CEO (Chief Executive Officer) AI agent'
    },
    'cfo': {
        'color': 'emerald green',
        'theme': 'dollar sign, charts, finance',
        'description': 'CFO (Chief Financial Officer) AI agent'
    },
    'cmo': {
        'color': 'magenta pink',
        'theme': 'megaphone, marketing, brand',
        'description': 'CMO (Chief Marketing Officer) AI agent'
    },
    'coo': {
        'color': 'orange',
        'theme': 'gears, operations, workflow',
        'description': 'COO (Chief Operations Officer) AI agent'
    },
    'cio': {
        'color': 'cyan teal',
        'theme': 'lock, security, network',
        'description': 'CIO (Chief Information Officer) AI agent'
    },
    'clo': {
        'color': 'purple violet',
        'theme': 'scales of justice, legal, compliance',
        'description': 'CLO (Chief Legal Officer) AI agent'
    },
    'cpo': {
        'color': 'indigo',
        'theme': 'lightbulb, innovation, product',
        'description': 'CPO (Chief Product Officer) AI agent'
    },
    'cto': {
        'color': 'electric blue',
        'theme': 'code, binary, engineering',
        'description': 'CTO (Chief Technology Officer) AI agent'
    },
    'cxa': {
        'color': 'teal',
        'theme': 'headset, support, customer service',
        'description': 'CXA (Customer Experience Agent) AI agent'
    }
}


def generate_prompt(agent_id: str, agent_info: dict) -> str:
    """Generate an image prompt for an agent avatar."""
    return f"""Professional avatar icon for {agent_info['description']}. 
Dark {agent_info['color']} gradient background. 
Stylized futuristic robotic head silhouette with {agent_info['theme']} pattern overlay. 
Modern, sleek, corporate tech aesthetic. 
Minimal, clean circular design suitable for dashboard avatar.
Dark sci-fi style, no text, centered composition.
256x256 pixels."""


def generate_with_dalle(prompt: str, output_path: Path) -> bool:
    """Generate image using OpenAI DALL-E."""
    api_key = os.getenv('OPENAI_API_KEY')
    if not api_key:
        print("  ✗ OPENAI_API_KEY not set, skipping DALL-E generation")
        return False
        
    try:
        response = requests.post(
            "https://api.openai.com/v1/images/generations",
            headers={
                "Authorization": f"Bearer {api_key}",
                "Content-Type": "application/json"
            },
            json={
                "model": "dall-e-3",
                "prompt": prompt,
                "size": "1024x1024",
                "quality": "standard",
                "n": 1
            },
            timeout=120
        )
        response.raise_for_status()
        
        image_url = response.json()["data"][0]["url"]
        
        # Download and save
        img_response = requests.get(image_url)
        img_response.raise_for_status()
        
        with open(output_path, 'wb') as f:
            f.write(img_response.content)
            
        return True
        
    except Exception as e:
        print(f"  ✗ DALL-E error: {e}")
        return False


def generate_image(agent_id: str, agent_info: dict) -> bool:
    """Generate an avatar image for an agent."""
    output_path = OUTPUT_DIR / f"{agent_id}.png"
    prompt = generate_prompt(agent_id, agent_info)
    
    print(f"\n🎨 Generating {agent_id.upper()} avatar...")
    print(f"   Prompt: {prompt[:60]}...")
    
    # Try DALL-E (primary for image generation)
    if generate_with_dalle(prompt, output_path):
        print(f"  ✓ Saved to {output_path}")
        return True
    
    print(f"  ✗ Failed to generate image for {agent_id}")
    return False


def main():
    parser = argparse.ArgumentParser(description="Generate agent avatar images")
    parser.add_argument('--factory', default='development', help='Factory ID for billing')
    parser.add_argument('--agent', help='Generate only specific agent (e.g., ceo)')
    args = parser.parse_args()
    
    # Set factory ID for tracking
    os.environ['FACTORY_ID'] = args.factory
    
    print("=" * 50)
    print("Agent Avatar Generator")
    print(f"Factory: {args.factory}")
    print(f"Output: {OUTPUT_DIR}")
    print("=" * 50)
    
    # Create output directory
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
    
    # Determine which agents to generate
    agents_to_generate = AGENTS
    if args.agent:
        if args.agent not in AGENTS:
            print(f"Error: Unknown agent '{args.agent}'")
            print(f"Available: {', '.join(AGENTS.keys())}")
            sys.exit(1)
        agents_to_generate = {args.agent: AGENTS[args.agent]}
    
    # Generate images
    success_count = 0
    for agent_id, agent_info in agents_to_generate.items():
        if generate_image(agent_id, agent_info):
            success_count += 1
            
    print("\n" + "=" * 50)
    print(f"Generated {success_count}/{len(agents_to_generate)} images")
    print("=" * 50)
    
    if success_count < len(agents_to_generate):
        print("\n⚠️  Some images failed. The dashboard will use CSS gradient fallbacks.")


if __name__ == "__main__":
    main()
