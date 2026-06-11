import zipfile
import json
from typing import List, Dict, Any
from datetime import datetime

class SlackExportParser:
    def __init__(self, zip_path: str):
        self.zip_path = zip_path

    def parse(self) -> List[Dict[str, Any]]:
        messages = []
        
        with zipfile.ZipFile(self.zip_path, 'r') as zip_ref:
            for file_name in zip_ref.namelist():
                if file_name.endswith('.json') and 'channels/' in file_name:
                    with zip_ref.open(file_name) as json_file:
                        channel_data = json.load(json_file)
                        messages.extend(self._parse_channel(channel_data))
        
        return messages

    def _parse_channel(self, channel_data: Dict[str, Any]) -> List[Dict[str, Any]]:
        messages = []
        
        for message in channel_data.get('messages', []):
            if message.get('type') == 'message' and 'text' in message:
                normalized_message = {
                    'message_id': message.get('client_msg_id', message.get('ts')),
                    'author': message.get('user', 'unknown'),
                    'channel': channel_data.get('name', 'unknown'),
                    'timestamp': datetime.fromtimestamp(float(message.get('ts', 0))),
                    'thread_id': message.get('thread_ts', None),
                    'message_text': message.get('text', '')
                }
                messages.append(normalized_message)
        
        return messages

class MessageNormalizer:
    def __init__(self, messages: List[Dict[str, Any]]):
        self.messages = messages

    def normalize(self) -> List[Dict[str, Any]]:
        normalized_messages = []
        
        for message in self.messages:
            normalized_message = {
                'message_id': message['message_id'],
                'author': message['author'],
                'channel': message['channel'],
                'timestamp': message['timestamp'].isoformat(),
                'thread_id': message['thread_id'],
                'message_text': message['message_text']
            }
            normalized_messages.append(normalized_message)
        
        return normalized_messages
