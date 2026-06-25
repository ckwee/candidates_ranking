from typing import List, Dict
from pydantic import BaseModel, Field

class CriteriaSchema(BaseModel):
    must_haves: List[str] = Field(default_factory=list)
    good_to_haves: List[str] = Field(default_factory=list)
    experience_years: str = "N/A"
    education: str = "N/A"
    key_responsibilities: List[str] = Field(default_factory=list)
    weights: Dict[str, float] = Field(default_factory=dict)

class EvaluationSchema(BaseModel):
    candidate_name: str
    overall_score: float = Field(..., ge=0, le=100)
    confidence: float = Field(..., ge=0, le=100)
    strengths: List[str] = Field(default_factory=list)
    weaknesses: List[str] = Field(default_factory=list)
    justification: str
    category_scores: Dict[str, float] = Field(default_factory=dict)

class PipelineRequest(BaseModel):
    job_description: str
    resumes: Dict[str, str]

class PipelineResponse(BaseModel):
    criteria: CriteriaSchema
    evaluations: List[EvaluationSchema]
    ranking: List[EvaluationSchema]
