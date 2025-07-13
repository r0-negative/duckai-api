import base64
import hashlib
import json
import requests
from typing import Dict, List
from py_mini_racer import py_mini_racer


class DuckAi:
    def __init__(self, model: str = "gpt-4o-mini"):
        self.model = model
        self.status_url = "https://duckduckgo.com/duckchat/v1/status"
        self.chat_api = "https://duckduckgo.com/duckchat/v1/chat"
        self.headers = self._initialize_headers()

    def _initialize_headers(self) -> Dict[str, str]:
        return {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:139.0) Gecko/20100101 Firefox/139.0",
            "Accept": "*/*",
            "Accept-Language": "en-US,en;q=0.5",
            "Accept-Encoding": "gzip, deflate, br, zstd",
            "Referer": "https://duckduckgo.com/",
            "Cache-Control": "no-store",
            "x-vqd-accept": "1",
            "Connection": "keep-alive",
            "Cookie": "dcm=3",
            "Sec-Fetch-Dest": "empty",
            "Sec-Fetch-Mode": "cors",
            "Sec-Fetch-Site": "same-origin",
            "Priority": "u=4",
            "Pragma": "no-cache",
            "TE": "trailers"
        }

    class OperationError(Exception):
        def __init__(self, error_text: str):
            super().__init__(error_text)

    def get_hashes(self, vqd_hash_b64: str) -> str:
        js_script = base64.b64decode(vqd_hash_b64).decode("utf-8")
        ctx = py_mini_racer.MiniRacer()

        ctx.eval("""
            function parseHTML(html) {
                const root = { tagName: null, children: [], parent: null };
                let current = root;
                const blockElements = new Set([
                    'address','article','aside','blockquote','div','dl','fieldset','figcaption',
                    'figure','footer','form','h1','h2','h3','h4','h5','h6','header','hr',
                    'main','nav','ol','p','pre','section','table','ul'
                ]);
                const voidElements = new Set([
                    "area","base","br","col","embed","hr","img","input",
                    "link","meta","param","source","track","wbr"
                ]);
                const tagRegex = /<\/?([a-zA-Z0-9]+)>?/g;
                let match;
                while ((match = tagRegex.exec(html)) !== null) {
                    const tag = match[1].toLowerCase();
                    const isClosing = html[match.index + 1] === '/';
                    if (!isClosing) {
                        if (current.tagName === 'p' && (blockElements.has(tag) || tag === 'p')) {
                            current = current.parent || root;
                        }
                        const elem = { tagName: tag, children: [], parent: current };
                        current.children.push(elem);
                        if (!voidElements.has(tag)) {
                            current = elem;
                        }
                    } else {
                        if (tag === 'br') {
                            if (current.parent) {
                                current.parent.children.push({ tagName: 'br', children: [], parent: current.parent });
                            } else {
                                root.children.push({ tagName: 'br', children: [], parent: root });
                            }
                            continue;
                        }
                        if (voidElements.has(tag)) continue;
                        let temp = current;
                        while (temp && temp.tagName !== tag) temp = temp.parent;
                        if (temp) current = temp.parent || root;
                    }
                }
                while (current && current !== root) current = current.parent || root;
                return root;
            }

            const voidElements = new Set(["area","base","br","col","embed","hr","img","input","link","meta","param","source","track","wbr"]);
            function serialize(node) {
                if (!node.tagName) return node.children.map(serialize).join('');
                if (voidElements.has(node.tagName)) return `<${node.tagName}>`;
                let html = `<${node.tagName}>`;
                html += node.children.map(serialize).join('');
                html += `</${node.tagName}>`;
                return html;
            }

            function findAll(node) {
                let result = [];
                if (node.tagName) result.push(node);
                node.children.forEach(child => {
                    result = result.concat(findAll(child));
                });
                return result;
            }

            var document = {
                createElement: function(tagName) {
                    return {
                        _innerHTML: '',
                        _parsedTree: null,
                        get innerHTML() {
                            return serialize(this._parsedTree);
                        },
                        set innerHTML(html) {
                            this._innerHTML = html;
                            this._parsedTree = parseHTML(html);
                        },
                        querySelectorAll: function(sel) {
                            if (sel !== '*') return [];
                            if (!this._parsedTree) return [];
                            return findAll(this._parsedTree);
                        }
                    };
                },
                body: {
                    appendChild: function() {},
                    removeChild: function() {}
                }
            };

            var navigator = {
                userAgent: "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:140.0) Gecko/20100101 Firefox/140.0",
                webdriver: false
            };

            var window = {
                top: {
                    Array_Object: {}, Object: {}, Promise: {}, Proxy: {}, Symbol: {}, JSON: {}, Window: {}
                }
            };

            Object.keys = function(obj) {
                var keys = [];
                for (var k in obj) keys.push(k);
                return keys;
            };
        """)

        result = json.loads(ctx.eval(f"JSON.stringify({js_script})"))
        hashed = [base64.b64encode(hashlib.sha256(ch.encode()).digest()).decode() for ch in result['client_hashes']]
        result['client_hashes'] = hashed
        result['meta']['origin'] = "https://duckduckgo.com"
        result['meta']['stack'] = (
            "Error\n"
            "    at b (https://duckduckgo.com/dist/wpm.chat.576c5771a56bc23aac8e.js:1:14240)\n"
            "    at async https://duckduckgo.com/dist/wpm.chat.576c5771a56bc23aac8e.js:1:16463"
        )
        result['meta']['duration'] = "41"
        return base64.b64encode(json.dumps(result).encode()).decode()

    def models(self) -> List[str]:
        return [
            "gpt-4o-mini",
            "o3-mini",
            "claude-3-haiku-20240307",
            "meta-llama/Meta-Llama-3.1-70B-Instruct-Turbo",
            "mistralai/Mixtral-8x7B-Instruct-v0.1"
        ]

    def chat(self, prompt: str) -> str:
        data = {
            "model": self.model,
            "messages": [{
                "role": "user",
                "content": [{"type": "text", "text": prompt}]
            }]
        }

        status_res = requests.get(self.status_url, headers={**self.headers})
        vqd_hash_header = status_res.headers.get("x-vqd-hash-1")

        if not vqd_hash_header:
            raise self.OperationError("Missing VQD hash from status response.")

        self.headers["x-vqd-hash-1"] = self.get_hashes(vqd_hash_header)
        self.headers["Content-Type"] = "application/json; charset=utf-8"

        response = requests.post(self.chat_api, headers=self.headers, json=data, verify=False)

        if response.status_code == 200:
            return self._parse_response(response.content)
        raise self.OperationError("chat(): " + response.text)

    def _parse_response(self, response_content: bytes) -> str:
        response_text = response_content.decode("utf-8", errors="replace")
        messages = []

        for line in response_text.splitlines():
            if line.startswith("data: "):
                try:
                    message_data = json.loads(line.removeprefix("data: "))
                    if message_data.get("message"):
                        messages.append(message_data["message"])
                except json.JSONDecodeError:
                    continue

        return ''.join(messages)
