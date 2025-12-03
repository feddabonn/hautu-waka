#!/usr/bin/env python3
"""
Hautū Waka Build Script

Combines JSON data files with HTML template to produce a single self-contained HTML file.

Usage:
    python build.py

Outputs:
    output/hautu-waka.html
"""

import json
import os
from pathlib import Path

# Paths
SCRIPT_DIR = Path(__file__).parent
DATA_DIR = SCRIPT_DIR / "data"
TEMPLATE_FILE = SCRIPT_DIR / "template.html"
OUTPUT_DIR = SCRIPT_DIR / "output"
OUTPUT_FILE = OUTPUT_DIR / "hautu-waka.html"


def load_json(filename):
    """Load a JSON file from the data directory."""
    filepath = DATA_DIR / filename
    with open(filepath, "r", encoding="utf-8") as f:
        return json.load(f)


def make_id(name):
    """Convert a name to a URL-friendly ID."""
    return name.lower().replace(" ", "-").replace("(", "").replace(")", "").replace("/", "-").replace("'", "")


def build_intro_html(intro):
    """Generate HTML for the introduction section."""
    sections_html = ""
    for section in intro["sections"]:
        sections_html += f"""
        <div class="intro-block">
            <h3>{section["heading"]}</h3>
            <p>{section["content"]}</p>
        </div>
        """
    
    video_html = ""
    if intro.get("video"):
        video_html = f"""
        <div class="video-embed">
            <iframe src="{intro["video"]}" frameborder="0" allowfullscreen></iframe>
        </div>
        """
    
    return f"""
    <section id="introduction" class="section section-intro">
        <div class="container">
            <h1>{intro["title"]}</h1>
            <p class="subtitle">{intro["subtitle"]}</p>
            <p class="hook">{intro["hook"]}</p>
            {sections_html}
            {video_html}
            <div class="attribution">
                <p>{intro["attribution"]["primary"]}</p>
                <p>{intro["attribution"]["organisations"]}</p>
            </div>
        </div>
    </section>
    """


def build_stage_overlay_data(stages, tools_lookup):
    """Generate JavaScript data for stage overlays."""
    stage_data = []
    for stage in stages:
        tool_names = [tools_lookup[t]["name"] for t in stage["tools"] if t in tools_lookup]
        stage_data.append({
            "id": stage["id"],
            "name_maori": stage["name_maori"],
            "name_english": stage["name_english"],
            "as_stage": stage["as_stage"],
            "as_state": stage["as_state"],
            "reflection_questions": stage["reflection_questions"],
            "tools": [{"id": t, "name": tools_lookup[t]["name"]} for t in stage["tools"] if t in tools_lookup],
            "hotspot": stage["hotspot"]
        })
    return json.dumps(stage_data, indent=2)


def build_tools_html(tools, stages_lookup):
    """Generate HTML for the tools section."""
    tools_html = ""
    for tool in tools:
        # Stage badges
        stage_badges = ""
        for stage_id in tool["stages"]:
            if stage_id in stages_lookup:
                stage = stages_lookup[stage_id]
                stage_badges += f'<span class="badge badge-stage">{stage["name_maori"]}</span> '
        
        # Muscle links
        muscle_links = ""
        for muscle_id in tool["muscles"]:
            muscle_name = muscle_id.replace("-", " ").title()
            muscle_links += f'<a href="#muscle-{muscle_id}" class="muscle-link">{muscle_name}</a> '
        
        video_html = ""
        if tool.get("video"):
            video_html = f"""
            <div class="video-embed">
                <iframe src="{tool["video"]}" frameborder="0" allowfullscreen></iframe>
            </div>
            """
        
        tools_html += f"""
        <div id="tool-{tool["id"]}" class="tool-entry">
            <h3>{tool["name"]}</h3>
            <p class="description">{tool["description"]}</p>
            {video_html}
            <div class="meta">
                <div class="stages">
                    <span class="meta-label">Used in:</span> {stage_badges}
                </div>
                <div class="muscles">
                    <span class="meta-label">Develops:</span> {muscle_links}
                </div>
            </div>
        </div>
        """
    
    return f"""
    <section id="tools" class="section section-tools">
        <div class="container">
            <h2>Tools</h2>
            <p class="section-intro">Processes and methods that help navigate each stage. Click a muscle name to see what it means.</p>
            <div class="tools-list">
                {tools_html}
            </div>
        </div>
    </section>
    """


def build_muscles_html(muscles_data, tools_lookup):
    """Generate HTML for the muscles section."""
    dimensions_html = ""
    
    for dimension in muscles_data["dimensions"]:
        muscles_html = ""
        for muscle in dimension["muscles"]:
            # Tool links
            tool_links = ""
            if muscle["tools"]:
                for tool_id in muscle["tools"]:
                    if tool_id in tools_lookup:
                        tool_links += f'<a href="#tool-{tool_id}" class="tool-link">{tools_lookup[tool_id]["name"]}</a> '
            else:
                tool_links = '<span class="no-tools">No specific tools mapped</span>'
            
            muscles_html += f"""
            <div id="muscle-{muscle["id"]}" class="muscle-entry">
                <h4>{muscle["name"]}</h4>
                <p class="description">{muscle["description"]}</p>
                <div class="meta">
                    <span class="meta-label">Developed by:</span> {tool_links}
                </div>
            </div>
            """
        
        dimensions_html += f"""
        <div class="dimension" id="dimension-{dimension["id"]}">
            <h3>{dimension["name"]} <span class="dimension-english">({dimension["name_english"]})</span></h3>
            <p class="dimension-description">{dimension["description"]}</p>
            <div class="muscles-list">
                {muscles_html}
            </div>
        </div>
        """
    
    return f"""
    <section id="muscles" class="section section-muscles">
        <div class="container">
            <h2>Muscles</h2>
            <p class="section-intro">{muscles_data["intro"]}</p>
            <div class="dimensions">
                {dimensions_html}
            </div>
        </div>
    </section>
    """


def build_sources_html(sources):
    """Generate HTML for the mycorrhizal network section."""
    categories_html = ""
    
    for category in sources["categories"]:
        items_html = ""
        for item in category["items"]:
            # Handle different item structures
            if "title" in item:
                # It's a reading
                name = item["title"]
                detail = f' — {item["author"]}' if item.get("author") else ""
            else:
                name = item["name"]
                if item.get("author"):
                    detail = f' — {item["author"]}'
                elif item.get("role"):
                    detail = f' — {item["role"]}'
                elif item.get("description"):
                    detail = f' — {item["description"]}'
                else:
                    detail = ""
            
            if item.get("link"):
                items_html += f'<li><a href="{item["link"]}" target="_blank">{name}</a>{detail}</li>'
            else:
                items_html += f'<li>{name}{detail}</li>'
        
        categories_html += f"""
        <div class="source-category">
            <h3>{category["name"]}</h3>
            <p class="category-description">{category["description"]}</p>
            <ul>
                {items_html}
            </ul>
        </div>
        """
    
    return f"""
    <section id="sources" class="section section-sources">
        <div class="container">
            <h2>Mycorrhizal Network</h2>
            <p class="section-intro">{sources["intro"]}</p>
            <div class="sources-grid">
                {categories_html}
            </div>
        </div>
    </section>
    """


def build_html(intro, stages, tools, muscles, sources):
    """Build the complete HTML file."""
    
    # Create lookup dictionaries
    tools_lookup = {t["id"]: t for t in tools}
    stages_lookup = {s["id"]: s for s in stages}
    
    # Generate section HTML
    intro_html = build_intro_html(intro)
    tools_html = build_tools_html(tools, stages_lookup)
    muscles_html = build_muscles_html(muscles, tools_lookup)
    sources_html = build_sources_html(sources)
    
    # Generate stage data for JavaScript
    stage_data_js = build_stage_overlay_data(stages, tools_lookup)
    
    # Read template
    with open(TEMPLATE_FILE, "r", encoding="utf-8") as f:
        template = f.read()
    
    # Replace placeholders
    html = template.replace("{{INTRO_SECTION}}", intro_html)
    html = html.replace("{{TOOLS_SECTION}}", tools_html)
    html = html.replace("{{MUSCLES_SECTION}}", muscles_html)
    html = html.replace("{{SOURCES_SECTION}}", sources_html)
    html = html.replace("{{STAGE_DATA}}", stage_data_js)
    
    return html


def main():
    """Main build function."""
    print("Loading data files...")
    intro = load_json("intro.json")
    stages = load_json("stages.json")
    tools = load_json("tools.json")
    muscles = load_json("muscles.json")
    sources = load_json("sources.json")
    
    print("Building HTML...")
    html = build_html(intro, stages, tools, muscles, sources)
    
    # Ensure output directory exists
    OUTPUT_DIR.mkdir(exist_ok=True)
    
    # Write output file
    with open(OUTPUT_FILE, "w", encoding="utf-8") as f:
        f.write(html)
    
    print(f"Built: {OUTPUT_FILE}")
    print(f"File size: {OUTPUT_FILE.stat().st_size / 1024:.1f} KB")


if __name__ == "__main__":
    main()
