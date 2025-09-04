"""
AI-Parseable Knowledge Base for LLM Usage Guidance
This structured data allows the chatbot to provide tailored recommendations
based on user priorities (cost, quality, speed, etc.)
"""

from dataclasses import dataclass, field
from typing import Dict, List, Optional
from enum import Enum


class UserPriority(Enum):
    COST = "cost"
    QUALITY = "quality"
    SPEED = "speed"
    ACCURACY = "accuracy"
    CREATIVITY = "creativity"


class DifficultyLevel(Enum):
    BEGINNER = "beginner"
    INTERMEDIATE = "intermediate"
    ADVANCED = "advanced"


@dataclass
class Technique:
    name: str
    description: str
    use_case: str
    cost_efficiency: int  # 1-10 scale (10 = most cost efficient)
    quality_output: int  # 1-10 scale (10 = highest quality)
    time_to_implement: int  # minutes
    accuracy_requirement: int  # 1-10 scale (10 = highest accuracy needed)
    creativity_level: int  # 1-10 scale (10 = most creative)
    difficulty: DifficultyLevel
    prompt_template: str
    example_workflow: List[str]
    common_pitfalls: List[str]
    best_for_priorities: List[UserPriority]
    tokens_per_task: Dict[str, int]  # estimated token usage


@dataclass
class Domain:
    name: str
    description: str
    core_principles: List[str]
    techniques: List[Technique]
    universal_tips: List[str]
    metric_considerations: Dict[str, str]


# RESEARCH DOMAIN
research_domain = Domain(
    name="Research",
    description="AI-assisted academic and professional research workflows",
    core_principles=[
        "Structured prompting yields better results",
        "Iterative refinement improves accuracy",
        "Critical evaluation is essential",
        "Context and specificity drive quality",
    ],
    techniques=[
        Technique(
            name="Literature Review Synthesis",
            description="Break large topics into focused subtopics for systematic review",
            use_case="Synthesizing research on specific topics or finding gaps in literature",
            cost_efficiency=8,
            quality_output=9,
            time_to_implement=30,
            accuracy_requirement=9,
            creativity_level=4,
            difficulty=DifficultyLevel.INTERMEDIATE,
            prompt_template="Summarise key findings from [timeframe] studies on [specific topic] in [field], focusing on [specific aspect]. Include methodology approaches and identify research gaps.",
            example_workflow=[
                "Define specific research question and scope",
                "Break topic into 3-5 focused subtopics",
                "Generate synthesis for each subtopic",
                "Identify patterns and gaps across subtopics",
                "Create comprehensive overview",
            ],
            common_pitfalls=[
                "Making requests too broad",
                "Not fact-checking citations",
                "Accepting outputs without critical analysis",
            ],
            best_for_priorities=[UserPriority.QUALITY, UserPriority.ACCURACY],
            tokens_per_task={"light": 2000, "standard": 5000, "comprehensive": 12000},
        ),
        Technique(
            name="Hierarchical Research Approach",
            description="Start broad with cheaper models, deep-dive with premium models",
            use_case="Cost-effective research when budget is limited",
            cost_efficiency=9,
            quality_output=7,
            time_to_implement=45,
            accuracy_requirement=7,
            creativity_level=3,
            difficulty=DifficultyLevel.BEGINNER,
            prompt_template="First pass: 'Provide overview of [topic] including main areas and key concepts.' Second pass: 'Deep analysis of [specific area] including [detailed requirements].'",
            example_workflow=[
                "Use basic model for topic overview and structure",
                "Identify 2-3 priority areas for deep analysis",
                "Use premium model for detailed analysis of priority areas",
                "Synthesize findings across all areas",
            ],
            common_pitfalls=[
                "Skipping the broad overview phase",
                "Not prioritizing which areas need detailed analysis",
            ],
            best_for_priorities=[UserPriority.COST, UserPriority.SPEED],
            tokens_per_task={"light": 1500, "standard": 3500, "comprehensive": 8000},
        ),
        Technique(
            name="Multi-Pass Analysis",
            description="Sequential analysis passes for maximum accuracy and depth",
            use_case="When highest quality research output is required",
            cost_efficiency=4,
            quality_output=10,
            time_to_implement=90,
            accuracy_requirement=10,
            creativity_level=5,
            difficulty=DifficultyLevel.ADVANCED,
            prompt_template="Pass 1: Initial synthesis. Pass 2: Critical analysis and assumption checking. Pass 3: Cross-reference verification and gap identification.",
            example_workflow=[
                "Generate initial comprehensive analysis",
                "Critically evaluate findings and identify assumptions",
                "Cross-reference key claims and check for contradictions",
                "Identify knowledge gaps and areas needing further research",
                "Synthesize final high-confidence conclusions",
            ],
            common_pitfalls=[
                "Rushing through intermediate passes",
                "Not allocating enough time for verification",
            ],
            best_for_priorities=[UserPriority.QUALITY, UserPriority.ACCURACY],
            tokens_per_task={"light": 5000, "standard": 12000, "comprehensive": 25000},
        ),
    ],
    universal_tips=[
        "Always provide specific context and constraints",
        "Break complex questions into smaller components",
        "Use follow-up questions to refine outputs",
        "Fact-check all claims and citations",
    ],
    metric_considerations={
        "cost": "Use hierarchical approaches and focus AI on high-value analysis",
        "quality": "Employ multi-pass techniques and extensive verification",
        "speed": "Start with structured outlines and use templates",
        "accuracy": "Always fact-check and cross-reference AI outputs",
    },
)

# PROGRAMMING DOMAIN
programming_domain = Domain(
    name="Programming",
    description="AI-assisted software development and coding workflows",
    core_principles=[
        "Clear context and constraints improve code quality",
        "Iterative refinement beats one-shot generation",
        "Always review and test AI-generated code",
        "Use AI for patterns, not complete applications",
    ],
    techniques=[
        Technique(
            name="Contextual Code Generation",
            description="Provide comprehensive context for accurate code generation",
            use_case="Generating specific functions or code components",
            cost_efficiency=7,
            quality_output=8,
            time_to_implement=15,
            accuracy_requirement=8,
            creativity_level=5,
            difficulty=DifficultyLevel.BEGINNER,
            prompt_template="Context: [language, framework, constraints]\nTask: [specific function needed]\nRequirements: [performance, style, testing]\nInput/Output: [examples if applicable]",
            example_workflow=[
                "Define exact requirements and constraints",
                "Specify programming language and framework",
                "Include example inputs/outputs",
                "Request code with comments and error handling",
                "Test and refine generated code",
            ],
            common_pitfalls=[
                "Insufficient context leading to generic code",
                "Not specifying error handling requirements",
                "Using generated code without testing",
            ],
            best_for_priorities=[UserPriority.SPEED, UserPriority.QUALITY],
            tokens_per_task={"light": 800, "standard": 2000, "comprehensive": 4000},
        ),
        Technique(
            name="Systematic Debugging Assistance",
            description="Structured approach to AI-assisted debugging",
            use_case="Identifying and fixing code issues efficiently",
            cost_efficiency=8,
            quality_output=7,
            time_to_implement=20,
            accuracy_requirement=9,
            creativity_level=3,
            difficulty=DifficultyLevel.INTERMEDIATE,
            prompt_template="Context: [relevant code, environment, error message]\nProblem: [specific issue description]\nRequest: [analysis type - identify cause, suggest fixes, prevention strategies]",
            example_workflow=[
                "Share minimal reproducible code example",
                "Include full error messages and stack traces",
                "Describe expected vs actual behavior",
                "Request step-by-step debugging analysis",
                "Implement and test suggested solutions",
            ],
            common_pitfalls=[
                "Sharing too much irrelevant code",
                "Not including complete error messages",
                "Implementing fixes without understanding them",
            ],
            best_for_priorities=[UserPriority.SPEED, UserPriority.ACCURACY],
            tokens_per_task={"light": 1000, "standard": 2500, "comprehensive": 5000},
        ),
        Technique(
            name="Architecture Planning Assistance",
            description="Use AI for system design and architecture decisions",
            use_case="Planning software architecture and making design decisions",
            cost_efficiency=6,
            quality_output=8,
            time_to_implement=60,
            accuracy_requirement=7,
            creativity_level=8,
            difficulty=DifficultyLevel.ADVANCED,
            prompt_template="Requirements: [functional and non-functional requirements]\nConstraints: [technical, time, resource limitations]\nRequest: [architecture options, trade-off analysis, scalability considerations]",
            example_workflow=[
                "Define clear functional requirements",
                "Specify technical constraints and limitations",
                "Request multiple architectural approaches",
                "Compare trade-offs between approaches",
                "Consider scalability and maintenance implications",
            ],
            common_pitfalls=[
                "Not clearly defining requirements upfront",
                "Ignoring non-functional requirements",
                "Choosing architecture without considering team expertise",
            ],
            best_for_priorities=[UserPriority.QUALITY, UserPriority.CREATIVITY],
            tokens_per_task={"light": 2000, "standard": 5000, "comprehensive": 10000},
        ),
    ],
    universal_tips=[
        "Always test AI-generated code before deployment",
        "Use version control to track AI-assisted changes",
        "Focus on code patterns rather than complete applications",
        "Include error handling and edge cases in requests",
    ],
    metric_considerations={
        "cost": "Focus on snippets and patterns rather than full applications",
        "quality": "Request multiple implementations and code review",
        "speed": "Use AI for boilerplate and common patterns",
        "accuracy": "Always test and validate generated code",
    },
)

# WRITING DOMAIN
writing_domain = Domain(
    name="Writing",
    description="AI-assisted content creation and writing workflows",
    core_principles=[
        "AI works best as collaborative partner, not replacement",
        "Structure and outline before detailed writing",
        "Maintain your unique voice and perspective",
        "Multiple iterations improve quality",
    ],
    techniques=[
        Technique(
            name="Structured Content Development",
            description="Use AI for ideation, outlining, and iterative improvement",
            use_case="Creating articles, reports, or long-form content",
            cost_efficiency=7,
            quality_output=8,
            time_to_implement=45,
            accuracy_requirement=6,
            creativity_level=7,
            difficulty=DifficultyLevel.BEGINNER,
            prompt_template="Audience: [target audience]\nPurpose: [inform/persuade/entertain]\nTone: [professional/casual/academic]\nConstraints: [word count, style requirements]\nTask: [outline/draft/revise specific section]",
            example_workflow=[
                "Define audience, purpose, and constraints",
                "Generate content outline with AI assistance",
                "Develop each section iteratively",
                "Use AI for editing and improvement suggestions",
                "Final human review and voice consistency check",
            ],
            common_pitfalls=[
                "Skipping the outlining phase",
                "Using AI content without adding personal perspective",
                "Not maintaining consistent voice throughout",
            ],
            best_for_priorities=[UserPriority.QUALITY, UserPriority.CREATIVITY],
            tokens_per_task={"light": 1500, "standard": 4000, "comprehensive": 8000},
        ),
        Technique(
            name="Rapid Content Generation",
            description="Quick content creation for time-sensitive needs",
            use_case="Fast turnaround content like social media, emails, or quick articles",
            cost_efficiency=9,
            quality_output=6,
            time_to_implement=15,
            accuracy_requirement=5,
            creativity_level=6,
            difficulty=DifficultyLevel.BEGINNER,
            prompt_template="Format: [email/post/article]\nKey points: [3-5 main messages]\nTone: [specify tone]\nLength: [word/character limit]\nCall-to-action: [if applicable]",
            example_workflow=[
                "List key points to communicate",
                "Specify format and length constraints",
                "Generate initial draft with AI",
                "Quick edit for tone and accuracy",
                "Add personal touches and finalize",
            ],
            common_pitfalls=[
                "Sacrificing too much quality for speed",
                "Not proofreading AI-generated content",
                "Using generic outputs without personalization",
            ],
            best_for_priorities=[UserPriority.SPEED, UserPriority.COST],
            tokens_per_task={"light": 500, "standard": 1200, "comprehensive": 2500},
        ),
    ],
    universal_tips=[
        "Always maintain your authentic voice",
        "Use AI for structure, you provide the insights",
        "Edit AI content to match your style",
        "Fact-check all claims and statistics",
    ],
    metric_considerations={
        "cost": "Use AI for outlines and editing, write content yourself",
        "quality": "Multiple draft iterations with different approaches",
        "speed": "Focus on templates and rapid generation techniques",
        "creativity": "Use AI for ideation and alternative perspectives",
    },
)

# Complete knowledge base structure
knowledge_base = {
    "domains": {
        "research": research_domain,
        "programming": programming_domain,
        "writing": writing_domain,
        # Add visual_creative and presentation domains here
    },
    "universal_principles": [
        "Be specific in your requests",
        "Provide relevant context",
        "Iterate and refine outputs",
        "Always verify and fact-check",
        "Maintain human judgment and expertise",
    ],
    "priority_optimization": {
        UserPriority.COST: {
            "strategies": [
                "Use hierarchical approaches (cheap model first, premium for details)",
                "Focus AI on high-value tasks, do routine work yourself",
                "Use templates and standardized prompts",
                "Batch similar tasks together",
            ],
            "token_saving_tips": [
                "Start with shorter, focused prompts",
                "Use bullet points instead of full sentences in prompts",
                "Reference previous context instead of re-explaining",
            ],
        },
        UserPriority.QUALITY: {
            "strategies": [
                "Use multi-pass approaches",
                "Request multiple perspectives or approaches",
                "Include verification and fact-checking steps",
                "Provide extensive context and examples",
            ],
            "quality_indicators": [
                "Specificity and detail in outputs",
                "Logical consistency",
                "Appropriate complexity for audience",
                "Actionable and practical advice",
            ],
        },
        UserPriority.SPEED: {
            "strategies": [
                "Use templates and standardized workflows",
                "Start with outlines before detailed content",
                "Focus on single-pass generation with light editing",
                "Prepare reusable prompt templates",
            ],
            "time_saving_tips": [
                "Have clear objectives before starting",
                "Use shorter prompts for faster responses",
                "Prepare context documents in advance",
            ],
        },
    },
}


def get_recommendations(
    domain: str,
    user_priorities: Dict[UserPriority, float],
    task_complexity: DifficultyLevel = DifficultyLevel.INTERMEDIATE,
) -> Dict:
    """
    Generate tailored recommendations based on user's domain, priorities, and complexity needs
    """

    if domain not in knowledge_base["domains"]:
        return {"error": f"Domain '{domain}' not found"}

    domain_data = knowledge_base["domains"][domain]

    # Score techniques based on user priorities
    scored_techniques = []
    for technique in domain_data.techniques:
        if (
            technique.difficulty.value <= task_complexity.value
            or task_complexity == DifficultyLevel.ADVANCED
        ):

            # Calculate priority score
            priority_score = 0
            for priority, weight in user_priorities.items():
                if priority == UserPriority.COST:
                    priority_score += technique.cost_efficiency * weight
                elif priority == UserPriority.QUALITY:
                    priority_score += technique.quality_output * weight
                elif priority == UserPriority.SPEED:
                    priority_score += (10 - (technique.time_to_implement / 10)) * weight
                elif priority == UserPriority.ACCURACY:
                    priority_score += technique.accuracy_requirement * weight
                elif priority == UserPriority.CREATIVITY:
                    priority_score += technique.creativity_level * weight

            scored_techniques.append(
                {
                    "technique": technique,
                    "score": priority_score,
                    "estimated_cost": technique.tokens_per_task,
                    "time_estimate": technique.time_to_implement,
                }
            )

    # Sort by score
    scored_techniques.sort(key=lambda x: x["score"], reverse=True)

    # Get top priority strategy
    top_priority = max(user_priorities.items(), key=lambda x: x[1])[0]
    optimization_strategy = knowledge_base["priority_optimization"].get(
        top_priority, {}
    )

    return {
        "domain": domain,
        "recommended_techniques": scored_techniques[:3],  # Top 3 techniques
        "optimization_strategy": optimization_strategy,
        "domain_principles": domain_data.core_principles,
        "universal_tips": domain_data.universal_tips,
    }


# Example usage
if __name__ == "__main__":
    # Budget-conscious programmer
    recommendations = get_recommendations(
        domain="programming",
        user_priorities={
            UserPriority.COST: 0.6,
            UserPriority.SPEED: 0.3,
            UserPriority.QUALITY: 0.1,
        },
        task_complexity=DifficultyLevel.BEGINNER,
    )

    print("=== BUDGET-CONSCIOUS PROGRAMMER RECOMMENDATIONS ===")
    for i, rec in enumerate(recommendations["recommended_techniques"], 1):
        technique = rec["technique"]
        print(f"\n{i}. {technique.name}")
        print(f"   Score: {rec['score']:.1f}/10")
        print(f"   Cost Efficiency: {technique.cost_efficiency}/10")
        print(f"   Time: {technique.time_to_implement} minutes")
        print(f"   Use case: {technique.use_case}")
        print(f"   Estimated tokens: {technique.tokens_per_task}")
