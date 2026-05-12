from pathlib import Path
import json

root = Path(__file__).resolve().parents[1]
channels = json.loads((root / 'shared/schemas/channel.schema.json').read_text(encoding='utf-8'))
print('Channel schema loaded:', channels['type'])
