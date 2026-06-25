import logging
from concurrent.futures import ThreadPoolExecutor, as_completed
from typing import Dict, List

from config import settings
from models import CriteriaSchema, EvaluationSchema
from llm_service import build_json_chain, safe_llm_invoke

logger = logging.getLogger("pipeline")

def analyze_jd(jd_text: str) -> CriteriaSchema:
    chain, parser = build_json_chain(
        "Extract structured hiring criteria. Output JSON only.",
        "Job Description:\n{jd}\n\nFormat:\n{format_instructions}",
        CriteriaSchema
    )

    result = safe_llm_invoke(
        chain,
        {"jd": jd_text, "format_instructions": parser.get_format_instructions()},
        CriteriaSchema
    )

    return result or CriteriaSchema()

def _eval_one(criteria: CriteriaSchema, name: str, text: str):
    chain, parser = build_json_chain(
        "Score the candidate strictly based on criteria. Output JSON only.",
        "Criteria:\n{criteria}\n\nCandidate: {candidate_name}\nResume:\n{resume_text}\n\nFormat:\n{format_instructions}",
        EvaluationSchema
    )

    payload = {
        "criteria": criteria.model_dump(),
        "candidate_name": name,
        "resume_text": text,
        "format_instructions": parser.get_format_instructions(),
    }

    return safe_llm_invoke(chain, payload, EvaluationSchema)

def evaluate_candidates(criteria: CriteriaSchema, resumes: Dict[str, str]):
    results = []
    with ThreadPoolExecutor(max_workers=settings.max_workers) as pool:
        futures = {pool.submit(_eval_one, criteria, n, t): n for n, t in resumes.items()}
        for f in as_completed(futures):
            r = f.result()
            if r:
                results.append(r)
    return results

def rank_candidates(evals: List[EvaluationSchema]):
    return sorted(evals, key=lambda x: x.overall_score, reverse=True)
