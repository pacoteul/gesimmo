import json
import re

transcript_path = r'C:\Users\jigga\.gemini\antigravity\brain\c976a7f0-f70f-4ba4-89d1-f11c8a85cc03\.system_generated\logs\transcript_full.jsonl'
css_content = ""

with open(transcript_path, 'r', encoding='utf-8') as f:
    for line in f:
        try:
            entry = json.loads(line)
            if 'tool_calls' in entry:
                for call in entry['tool_calls']:
                    name = call.get('tool_name') or call.get('name')
                    args = call.get('tool_args') or call.get('args', {})
                    
                    target = args.get('TargetFile', '')
                    if 'styles.css' in target:
                        if name in ['default_api:write_to_file', 'write_to_file']:
                            content = args.get('CodeContent', '')
                            if content:
                                css_content = content
                                
                        elif name in ['default_api:replace_file_content', 'replace_file_content']:
                            t_content = args.get('TargetContent', '')
                            r_content = args.get('ReplacementContent', '')
                            if t_content and css_content.count(t_content) == 1:
                                css_content = css_content.replace(t_content, r_content)
                                
                        elif name in ['default_api:multi_replace_file_content', 'multi_replace_file_content']:
                            chunks = args.get('ReplacementChunks', [])
                            for chunk in chunks:
                                t_content = chunk.get('TargetContent', '')
                                r_content = chunk.get('ReplacementContent', '')
                                if t_content and css_content.count(t_content) == 1:
                                    css_content = css_content.replace(t_content, r_content)
                                    
                        elif name in ['default_api:run_command', 'run_command']:
                            cmd = args.get('CommandLine', '')
                            if 'styles.css' in cmd and 'Add-Content' in cmd and 'Global Footer' not in cmd:
                                match = re.search(r'@\"(.*?)\"@', cmd, re.DOTALL)
                                if match:
                                    css_content += '\n\n' + match.group(1).strip()
        except Exception as e:
            pass

with open(r'c:\Users\jigga\Desktop\gesimmo\styles.css', 'w', encoding='utf-8') as out:
    out.write(css_content)
print(f'Restored CSS with size: {len(css_content)}')
