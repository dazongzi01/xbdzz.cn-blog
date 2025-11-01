"""
Claude API wrapper for workflow system
"""

import json
import os
from typing import Optional, Dict, Any, List


class ClaudeAPI:
    """Wrapper for Anthropic Claude API"""

    def __init__(self, api_key: Optional[str] = None):
        """Initialize Claude API client"""
        self.api_key = api_key or os.environ.get('ANTHROPIC_API_KEY')
        if not self.api_key:
            raise ValueError(
                "ANTHROPIC_API_KEY not set. Please set the environment variable or pass api_key."
            )

        try:
            from anthropic import Anthropic
            self.client = Anthropic(api_key=self.api_key)
        except ImportError:
            raise ImportError(
                "anthropic package not installed. Install with: pip install anthropic"
            )

    def call_api(
        self,
        prompt: str,
        system: str = "",
        model: str = "claude-3-5-sonnet-20241022",
        max_tokens: int = 2000,
        temperature: float = 0.7
    ) -> str:
        """Call Claude API with given prompt"""
        messages = [{"role": "user", "content": prompt}]

        response = self.client.messages.create(
            model=model,
            max_tokens=max_tokens,
            temperature=temperature,
            system=system if system else None,
            messages=messages
        )

        return response.content[0].text

    def generate_content(
        self,
        topic: str,
        audiences: List[str],
        outline: str,
        word_count: int = 5000,
        style: str = "专业准确"
    ) -> str:
        """Generate article content for given topic and audiences"""

        system_prompt = """你是一个专业的技术文章编写专家。你的任务是：
1. 为多个不同的受众编写内容
2. 确保内容准确、专业、有趣
3. 使用清晰的结构和易于理解的语言
4. 包含具体的示例和实际应用场景"""

        audiences_text = "\n".join([f"  - {a}" for a in audiences])
        user_prompt = f"""请为以下主题编写一篇文章：

主题：{topic}

目标受众：
{audiences_text}

内容大纲：
{outline}

写作风格要求：{style}

目标字数：约 {word_count} 字

请编写完整的文章内容，确保：
1. 内容结构清晰，易于阅读
2. 对多个受众都有吸引力
3. 包含必要的示例和说明
4. 使用恰当的格式和强调"""

        return self.call_api(
            prompt=user_prompt,
            system=system_prompt,
            max_tokens=4000
        )

    def generate_title_variants(self, original_title: str, count: int = 3) -> List[str]:
        """Generate title variants for the given title"""
        system_prompt = "你是一个创意文案专家，擅长编写吸引人的标题。"

        user_prompt = f"""请为以下主题生成 {count} 个不同风格的标题变体：

原标题：{original_title}

要求：
1. 标题需要有吸引力
2. 需要传达原标题的核心信息
3. 可以采用不同的风格（如提问式、陈述式、引人思考等）

请只返回标题列表，每个标题占一行，不需要编号。"""

        response = self.call_api(prompt=user_prompt, system=system_prompt)
        return [line.strip() for line in response.strip().split('\n') if line.strip()]

    def analyze_content_structure(self, content: str, target_audiences: List[str]) -> Dict[str, Any]:
        """Analyze content and suggest structure improvements"""
        audiences_text = "\n".join([f"  - {a}" for a in target_audiences])

        system_prompt = """你是一个内容结构分析专家。分析给定的内容并提供结构化的建议。
请以JSON格式返回结果。"""

        user_prompt = f"""请分析以下内容，并为这些目标受众提供结构优化建议：

内容：
{content}

目标受众：
{audiences_text}

请返回JSON格式的分析结果，包含：
- sections：建议的主要部分
- key_points：每个部分的关键点
- improvements：改进建议
- estimated_word_count：估计字数"""

        response = self.call_api(prompt=user_prompt, system=system_prompt)

        try:
            # Extract JSON from response
            json_match = response.find('{')
            json_end = response.rfind('}') + 1
            if json_match >= 0 and json_end > json_match:
                json_str = response[json_match:json_end]
                return json.loads(json_str)
        except json.JSONDecodeError:
            pass

        return {"analysis": response}

    def optimize_for_audience(
        self,
        content: str,
        original_audience: str,
        target_audience: str
    ) -> str:
        """Rewrite content for a different audience"""

        system_prompt = f"""你的任务是将内容从为'{original_audience}'编写的风格改写为适合'{target_audience}'的风格。
保持信息准确性，但调整复杂度、词汇和示例以适应目标受众。"""

        user_prompt = f"""请将以下内容改写为适合'{target_audience}'的风格：

原内容：
{content}

改写要求：
1. 保持核心信息准确
2. 调整专业术语的使用和解释
3. 使用适合目标受众的例子和类比
4. 调整内容的深度和广度"""

        return self.call_api(prompt=user_prompt, system=system_prompt, max_tokens=3000)

    def generate_qa_section(self, content: str, count: int = 5) -> List[Dict[str, str]]:
        """Generate Q&A section based on content"""

        system_prompt = """你是一个FAQ编写专家。基于提供的内容生成常见问题及答案。
请以JSON数组格式返回，每个问题是一个对象，包含"question"和"answer"字段。"""

        user_prompt = f"""基于以下内容，生成 {count} 个常见问题及其答案：

内容：
{content}

请返回JSON数组格式，例如：
[
  {{"question": "问题1？", "answer": "答案1"}},
  {{"question": "问题2？", "answer": "答案2"}}
]"""

        response = self.call_api(prompt=user_prompt, system=system_prompt)

        try:
            json_match = response.find('[')
            json_end = response.rfind(']') + 1
            if json_match >= 0 and json_end > json_match:
                json_str = response[json_match:json_end]
                return json.loads(json_str)
        except json.JSONDecodeError:
            pass

        return []

    def check_quality(self, content: str) -> Dict[str, Any]:
        """Check content quality and return score and suggestions"""

        system_prompt = """你是一个内容质量审核专家。分析内容的质量并提供改进建议。
请以JSON格式返回检查结果。"""

        user_prompt = f"""请检查以下内容的质量，包括：
- 清晰度（0-100）
- 准确性（0-100）
- 结构（0-100）
- 吸引力（0-100）

内容：
{content}

请返回JSON格式：
{{
  "clarity_score": 数字,
  "accuracy_score": 数字,
  "structure_score": 数字,
  "engagement_score": 数字,
  "overall_score": 数字,
  "suggestions": ["建议1", "建议2", ...]
}}"""

        response = self.call_api(prompt=user_prompt, system=system_prompt)

        try:
            json_match = response.find('{')
            json_end = response.rfind('}') + 1
            if json_match >= 0 and json_end > json_match:
                json_str = response[json_match:json_end]
                return json.loads(json_str)
        except json.JSONDecodeError:
            pass

        return {"error": "Failed to parse quality check response"}
