import os
import json
from typing import Dict, List, Any, Optional
from openai import AsyncAzureOpenAI
from dotenv import load_dotenv

load_dotenv()

class OpenAIService:
    def __init__(self):
        self.client = AsyncAzureOpenAI(
            azure_endpoint=os.getenv("AZURE_OPENAI_ENDPOINT"),
            api_key=os.getenv("AZURE_OPENAI_API_KEY"),
            api_version=os.getenv("AZURE_OPENAI_API_VERSION", "2024-12-01-preview")
        )
        self.deployment_name = os.getenv("AZURE_OPENAI_DEPLOYMENT_NAME", "gpt-4o-mini")
    
    async def generate_explanation(
        self, 
        topic: str, 
        user_input: str, 
        learning_style: str = "visual",
        difficulty_level: str = "beginner",
        explanation_length: str = "medium"
    ) -> str:
        """Generate a personalized explanation"""
        try:
            prompt = f"""
You are an expert educational tutor. Create a personalized explanation based on the user's profile.

Topic: {topic}
User Question: {user_input}
Learning Style: {learning_style}
Difficulty Level: {difficulty_level}
Explanation Length: {explanation_length}

Create an engaging, personalized explanation that:
1. Matches the user's learning style
2. Is appropriate for their difficulty level
3. Answers their specific question
4. Uses examples and analogies when helpful
5. Encourages further learning

Format your response as a clear, well-structured explanation.
"""
            
            response = await self.client.chat.completions.create(
                model=self.deployment_name,
                messages=[
                    {"role": "system", "content": "You are an expert educational tutor."},
                    {"role": "user", "content": prompt}
                ],
                temperature=0.7,
                max_tokens=1000
            )
            
            return response.choices[0].message.content.strip()
        except Exception as e:
            return f"Error generating explanation: {str(e)}"
    
    async def generate_quiz(
        self, 
        topic: str, 
        difficulty_level: str = "beginner",
        num_questions: int = 5
    ) -> List[Dict[str, Any]]:
        """Generate quiz questions for a topic"""
        try:
            prompt = f"""
You are an expert quiz creator. Generate educational quiz questions for the given topic.

Topic: {topic}
Difficulty Level: {difficulty_level}
Number of Questions: {num_questions}

Create {num_questions} multiple-choice questions that:
1. Test understanding of the topic
2. Match the difficulty level
3. Have 4 answer options each
4. Include one correct answer and three plausible distractors
5. Cover different aspects of the topic

Format your response as JSON with this structure:
{{
    "questions": [
        {{
            "question": "Question text here",
            "options": ["Option A", "Option B", "Option C", "Option D"],
            "correct_answer": 0,
            "explanation": "Why this answer is correct"
        }}
    ]
}}
"""
            
            response = await self.client.chat.completions.create(
                model=self.deployment_name,
                messages=[
                    {"role": "system", "content": "You are an expert quiz creator. Always respond with valid JSON."},
                    {"role": "user", "content": prompt}
                ],
                temperature=0.7,
                max_tokens=2000
            )
            
            content = response.choices[0].message.content.strip()
            quiz_data = json.loads(content)
            return quiz_data.get("questions", [])
        except Exception as e:
            return [{"error": f"Error generating quiz: {str(e)}"}]
    
    async def evaluate_answer(
        self, 
        topic: str, 
        question: str, 
        correct_answer: str, 
        user_response: str
    ) -> str:
        """Evaluate user's answer and provide feedback"""
        try:
            prompt = f"""
You are an expert educational evaluator. Provide feedback on the user's answer.

Topic: {topic}
Question: {question}
Correct Answer: {correct_answer}
User's Answer: {user_response}

Provide:
1. Whether the answer is correct or incorrect
2. Constructive feedback explaining why
3. Suggestions for improvement if needed
4. Encouragement to continue learning

Be supportive and educational in your feedback.
"""
            
            response = await self.client.chat.completions.create(
                model=self.deployment_name,
                messages=[
                    {"role": "system", "content": "You are an expert educational evaluator."},
                    {"role": "user", "content": prompt}
                ],
                temperature=0.7,
                max_tokens=500
            )
            
            return response.choices[0].message.content.strip()
        except Exception as e:
            return f"Error evaluating answer: {str(e)}"
    
    async def generate_learning_path(
        self, 
        topic: str, 
        current_level: str = "beginner",
        learning_goals: List[str] = None
    ) -> Dict[str, Any]:
        """Generate a personalized learning path"""
        try:
            goals_text = ", ".join(learning_goals) if learning_goals else "general understanding"
            
            prompt = f"""
Create a personalized learning path for the topic: {topic}

Current Level: {current_level}
Learning Goals: {goals_text}

Generate a structured learning path with:
1. Learning objectives
2. Step-by-step modules
3. Prerequisites
4. Estimated time for each module
5. Recommended resources

Format as JSON with this structure:
{{
    "topic": "{topic}",
    "current_level": "{current_level}",
    "learning_goals": {learning_goals or []},
    "modules": [
        {{
            "title": "Module title",
            "description": "What you'll learn",
            "duration": "Estimated time",
            "prerequisites": ["Required knowledge"],
            "objectives": ["Learning objectives"]
        }}
    ],
    "total_estimated_time": "Total time estimate"
}}

IMPORTANT: Respond with ONLY valid JSON. No additional text or explanations.
"""
            
            response = await self.client.chat.completions.create(
                model=self.deployment_name,
                messages=[
                    {"role": "system", "content": "You are an expert educational curriculum designer. Always respond with valid JSON only. No additional text."},
                    {"role": "user", "content": prompt}
                ],
                temperature=0.7,
                max_tokens=2000
            )
            
            content = response.choices[0].message.content.strip()
            
            # Clean up the response to ensure it's valid JSON
            if content.startswith("```json"):
                content = content[7:]
            if content.endswith("```"):
                content = content[:-3]
            
            return json.loads(content)
        except json.JSONDecodeError as e:
            return {
                "error": f"JSON parsing error: {str(e)}",
                "raw_response": content if 'content' in locals() else "No response received"
            }
        except Exception as e:
            return {"error": f"Error generating learning path: {str(e)}"}

# Global instance
openai_service = OpenAIService()