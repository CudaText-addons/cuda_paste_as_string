import os
import json
from cudatext import *
import cudax_lib as appx
from .tools import *

fn_config = os.path.join(os.path.dirname(__file__), 'PasteAsString.sublime-settings')

lexer_map = {
    "source.js": "JavaScript",
    "source.java": "Java",
    "source.vbs": "VBScript",
    "source.cs": "C#",
    "source.perl": "Perl",
    "embedding.php": "PHP",
    "source.ruby": "Ruby",
    "source.c++": "C++",
    }

class Command:
    def get_data(self, lexer):
    
        with open(fn_config, encoding='utf8') as f:
            data = appx._json_loads(f.read())
            
        for d in data['scopes']:
            key = d.get('scope', '_')
            if lexer_map.get(key, '')==lexer:
                return d

    def paste(self):
    
        text = app_proc(PROC_GET_CLIP, '')
        if not text:
            msg_status('Clipboard is empty')
            return
            
        carets = ed.get_carets()
        if len(carets)!=1:
            msg_status('Paste-as-string needs single caret')
            return
        
        x0, y0, x1, y1 = carets[0]
        lexer = ed.get_prop(PROP_LEXER_CARET)
        if not lexer:
            return
            
        data = self.get_data(lexer)
        if not data:
            msg_status('Paste-as-string: no config for lexer '+lexer)
            return
        
        text = make_string(data, text, x0)
        ed.insert(x0, y0, text)
        msg_status('Pasted as string')
