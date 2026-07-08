import json
import re

transcript_path = r'C:\Users\jigga\.gemini\antigravity\brain\c976a7f0-f70f-4ba4-89d1-f11c8a85cc03\.system_generated\logs\transcript_full.jsonl'
css_parts = []

with open(transcript_path, 'r', encoding='utf-8') as f:
    for line in f:
        try:
            entry = json.loads(line)
            if 'tool_calls' in entry:
                for call in entry['tool_calls']:
                    name = call.get('tool_name') or call.get('name')
                    args = call.get('tool_args') or call.get('args', {})
                    
                    if name in ['default_api:write_to_file', 'write_to_file'] and args.get('TargetFile', '').endswith('styles.css'):
                        content = args.get('CodeContent')
                        if content:
                            css_parts = [content]
                            
                    elif name in ['default_api:run_command', 'run_command']:
                        cmd = args.get('CommandLine', '')
                        if 'styles.css' in cmd and 'Add-Content' in cmd and 'Global Footer' not in cmd:
                            match = re.search(r'@\"(.*?)\"@', cmd, re.DOTALL)
                            if match:
                                css_parts.append(match.group(1).strip())
        except Exception as e:
            pass

print(f'Found {len(css_parts)} parts of CSS.')
with open('c:/Users/jigga/Desktop/gesimmo/styles.css', 'w', encoding='utf-8') as out:
    for part in css_parts:
        out.write(part + '\n\n')
