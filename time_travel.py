import json
import re
import os

transcript_path = r'C:\Users\jigga\.gemini\antigravity\brain\c976a7f0-f70f-4ba4-89d1-f11c8a85cc03\.system_generated\logs\transcript_full.jsonl'
vfs = {}

stop_phrase = "maintenant sur toutes les pages tout en bas tu ajoute"

with open(transcript_path, 'r', encoding='utf-8') as f:
    for line in f:
        try:
            entry = json.loads(line)
            
            if entry.get('type') == 'USER_INPUT':
                content = entry.get('content', '')
                if stop_phrase in content:
                    print("Found stop phrase, stopping extraction.")
                    break
                    
            if 'tool_calls' in entry:
                for call in entry['tool_calls']:
                    name = call.get('tool_name') or call.get('name')
                    args = call.get('tool_args') or call.get('args', {})
                    
                    if name in ['default_api:write_to_file', 'write_to_file']:
                        target = args.get('TargetFile')
                        content = args.get('CodeContent', '')
                        if target:
                            target = os.path.basename(target)
                            vfs[target] = content
                            
                    elif name in ['default_api:replace_file_content', 'replace_file_content']:
                        target = args.get('TargetFile')
                        t_content = args.get('TargetContent', '')
                        r_content = args.get('ReplacementContent', '')
                        if target and t_content:
                            target = os.path.basename(target)
                            if target in vfs and vfs[target].count(t_content) == 1:
                                vfs[target] = vfs[target].replace(t_content, r_content)
                            
                    elif name in ['default_api:multi_replace_file_content', 'multi_replace_file_content']:
                        target = args.get('TargetFile')
                        chunks = args.get('ReplacementChunks', [])
                        if target:
                            target = os.path.basename(target)
                            if target in vfs:
                                for chunk in chunks:
                                    t_content = chunk.get('TargetContent', '')
                                    r_content = chunk.get('ReplacementContent', '')
                                    if t_content and vfs[target].count(t_content) == 1:
                                        vfs[target] = vfs[target].replace(t_content, r_content)
                                        
                    elif name in ['default_api:run_command', 'run_command']:
                        cmd = args.get('CommandLine', '')
                        if 'Add-Content' in cmd and 'Global Footer' not in cmd:
                            # Try to extract the target file and appended content
                            # Usually $css = @"..." \n Add-Content -Path "styles.css" ...
                            match_file = re.search(r'Add-Content -Path "(.*?)"', cmd)
                            match_content = re.search(r'@\"(.*?)\"@', cmd, re.DOTALL)
                            if match_file and match_content:
                                target = os.path.basename(match_file.group(1))
                                if target in vfs:
                                    vfs[target] += '\n\n' + match_content.group(1).strip()
                                    
        except Exception as e:
            pass

for target, content in vfs.items():
    if target.endswith('.html') or target.endswith('.css'):
        try:
            with open(os.path.join(r'c:\Users\jigga\Desktop\gesimmo', target), 'w', encoding='utf-8') as out:
                out.write(content)
            print(f'Restored {target} (size: {len(content)})')
        except Exception as e:
            print(f'Failed to restore {target}: {e}')
