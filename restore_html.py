import json
import os

transcript_path = r'C:\Users\jigga\.gemini\antigravity\brain\c976a7f0-f70f-4ba4-89d1-f11c8a85cc03\.system_generated\logs\transcript_full.jsonl'

vfs = {}

with open(transcript_path, 'r', encoding='utf-8') as f:
    for line in f:
        try:
            entry = json.loads(line)
            if 'tool_calls' in entry:
                for call in entry['tool_calls']:
                    name = call.get('tool_name') or call.get('name')
                    args = call.get('tool_args') or call.get('args', {})
                    
                    if name in ['default_api:write_to_file', 'write_to_file']:
                        target = args.get('TargetFile')
                        content = args.get('CodeContent')
                        if target and content is not None:
                            target = os.path.basename(target)
                            vfs[target] = content
        except Exception as e:
            pass

for target, content in vfs.items():
    if target.endswith('.html'):
        with open(os.path.join(r'c:\Users\jigga\Desktop\gesimmo', target), 'w', encoding='utf-8') as out:
            out.write(content)
        print(f'Restored HTML: {target}')
