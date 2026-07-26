import json
import requests


class OllamaLLM:
    """
    Wrapper around a local Ollama model.

    Supports:
    - Normal text generation
    - JSON generation for AI agent planning
    - Chat interface
    """

    def __init__(
        self,
        model="qwen2.5:1.5b",
        host="http://localhost:11434"
    ):
        self.model = model
        self.host = host.rstrip("/")

    # ---------------------------------------------------------
    # Internal Text Request
    # ---------------------------------------------------------

    def _generate(
        self,
        prompt,
        temperature=0.3,
        max_tokens=512
    ):

        url = f"{self.host}/api/generate"

        payload = {
            "model": self.model,
            "prompt": prompt,
            "stream": False,
            "options": {
                "temperature": temperature,
                "num_predict": max_tokens
            }
        }

        response = requests.post(
            url,
            json=payload,
            timeout=180
        )

        response.raise_for_status()

        data = response.json()

        return data.get("response", "").strip()

    # ---------------------------------------------------------
    # Internal JSON Request
    # ---------------------------------------------------------

    def _generate_json(
        self,
        prompt,
        temperature=0.1,
        max_tokens=512
    ):

        url = f"{self.host}/api/generate"

        payload = {
            "model": self.model,
            "prompt": prompt,
            "stream": False,
            "format": "json",
            "options": {
                "temperature": temperature,
                "num_predict": max_tokens
            }
        }

        response = requests.post(
            url,
            json=payload,
            timeout=180
        )

        response.raise_for_status()

        data = response.json()

        return data.get("response", "").strip()

    # ---------------------------------------------------------
    # Text Generation
    # ---------------------------------------------------------

    def generate(
        self,
        prompt,
        temperature=0.3,
        max_tokens=512
    ):

        try:

            return self._generate(
                prompt,
                temperature,
                max_tokens
            )

        except Exception as e:

            return f"LLM Error: {e}"

    # ---------------------------------------------------------
    # JSON Generation
    # ---------------------------------------------------------

    def generate_json(
        self,
        prompt,
        temperature=0.1,
        max_tokens=512
    ):

        planner_prompt = f"""
Return ONLY a JSON object.

No explanation.

No markdown.

No code fences.

{prompt}
"""

        response = None

        try:

            try:
                response = self._generate_json(
                    planner_prompt,
                    temperature,
                    max_tokens
                )
            except Exception:
                response = self._generate(
                    planner_prompt,
                    temperature,
                    max_tokens
                )

            print("\n================ RAW RESPONSE ================")
            print(repr(response))
            print("==============================================")

            cleaned = response.strip()

            # Remove markdown fences
            if cleaned.startswith("```json"):
                cleaned = cleaned[len("```json"):]

            if cleaned.startswith("```"):
                cleaned = cleaned[3:]

            if cleaned.endswith("```"):
                cleaned = cleaned[:-3]

            cleaned = cleaned.strip()

            # Extract JSON object if surrounded by text
            start = cleaned.find("{")
            end = cleaned.rfind("}")

            if start != -1 and end != -1:
                cleaned = cleaned[start:end + 1]

            print("\n=============== CLEANED JSON =================")
            print(repr(cleaned))
            print("==============================================")

            parsed = json.loads(cleaned)

            print("\n============== PARSED SUCCESS ================")
            print(parsed)
            print("==============================================")

            return parsed

        except Exception as e:

            print("\n=============== JSON ERROR ===================")
            print(e)
            print("==============================================")

            return {
                "success": False,
                "error": str(e),
                "raw_response": response
            }

    # ---------------------------------------------------------
    # Chat Interface
    # ---------------------------------------------------------

    def chat(
        self,
        system_prompt,
        user_prompt,
        temperature=0.3
    ):

        prompt = f"""
SYSTEM:
{system_prompt}

USER:
{user_prompt}

ASSISTANT:
"""

        return self.generate(
            prompt,
            temperature
        )