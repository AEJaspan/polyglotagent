from enum import Enum
from typing import List, Optional
from pydantic import BaseModel, Field, conint, confloat

# ----------------------------
# Shared types
# ----------------------------

class CEFRLevel(str, Enum):
    A1 = "A1"
    A2 = "A2"
    B1 = "B1"
    B2 = "B2"
    C1 = "C1"
    C2 = "C2"

class Evidence(BaseModel):
    """
    A short quote or summary from the transcript/audio that justifies a judgment.
    Encourage the judge to copy minimal spans verbatim and be specific.
    """
    excerpt: str = Field(..., description="Quoted text or concise summary that supports the score.")
    note: Optional[str] = Field(None, description="Why this excerpt matters for the criterion.")

class Subscore(BaseModel):
    """
    Generic numeric band with CEFR anchoring.
    """
    score: conint(ge=0, le=5) = Field(..., description="0–5 rubric band (0=not evidenced, 5=consistently at target).")
    cefr_estimate: CEFRLevel = Field(..., description="Best-fit CEFR level for this micro-criterion.")
    rationale: str = Field(..., description="Short justification tying observations to CEFR phrasing.")
    evidence: List[Evidence] = Field(default_factory=list, description="Evidence items supporting the score.")
    suggestions: Optional[str] = Field(None, description="Concrete, level-appropriate next steps for improvement.")

# ----------------------------
# Criterion-specific judges
# ----------------------------

class VocabJudge(BaseModel):
    """
    LLM judge for CEFR lexical resource.
    Focus on (a) lexical range and (b) lexical control.
    Range: how wide/precise the vocabulary is for topics and functions.
    Control: appropriacy, collocations, and avoidance of obvious lexical errors.
    Align with CEFR 'Vocabulary range' and 'Vocabulary control' descriptor scales.
    """
    vocab_range: Subscore = Field(..., description="Breadth and specificity of vocabulary available for the task domain.")
    vocab_control: Subscore = Field(..., description="Accuracy/appropriacy: word choice, collocations, word formation.")
    overall_cefr: CEFRLevel = Field(..., description="Holistic CEFR level for lexical resource.")
    overall_comment: str = Field(..., description="Synthesis of range/control evidence in CEFR terms.")

class GrammarJudge(BaseModel):
    """
    LLM judge for CEFR grammatical range and accuracy.
    Range: variety/complexity of structures.
    Accuracy: error density, impact on intelligibility, and control under pressure.
    Align with CEFR 'Grammatical accuracy' and (implied) range descriptors for speaking.
    """
    range_: Subscore = Field(..., alias="range", description="Breadth/complexity of grammatical structures used.")
    accuracy: Subscore = Field(..., description="Grammatical correctness and stability at length.")
    overall_cefr: CEFRLevel = Field(..., description="Holistic CEFR level for grammar.")
    overall_comment: str = Field(..., description="Summary linking range/accuracy to CEFR bands.")

class FluencyJudge(BaseModel):
    """
    LLM judge for CEFR 'Fluency' scale.
    Consider flow, pausing, hesitations, speed control, and ability to keep going.
    Focus on naturalness and whether pauses are content-related vs. language-search.
    """
    fluency: Subscore = Field(..., description="Flow and tempo: pausing, hesitations, reformulations, self-correction.")
    overall_cefr: CEFRLevel = Field(..., description="Holistic CEFR level for fluency.")
    overall_comment: str = Field(..., description="Key indicators (e.g., 'keeps going at B2 with occasional reformulation').")

class CoherenceJudge(BaseModel):
    """
    LLM judge for CEFR 'Coherence & cohesion' (spoken production).
    Assess discourse management: logical sequencing, thematic development, signposting,
    referencing, and use of connectors to build arguments/narratives.
    """
    organization: Subscore = Field(..., description="Logical sequencing and topic development.")
    cohesion_devices: Subscore = Field(..., description="Use of connectors, referencing, and signposting.")
    overall_cefr: CEFRLevel = Field(..., description="Holistic CEFR level for coherence & cohesion.")
    overall_comment: str = Field(..., description="Overall discourse control mapped to CEFR descriptors.")

class InteractionJudge(BaseModel):
    """
    LLM judge for CEFR 'Spoken interaction' scales.
    Consider turn-taking, cooperation strategies, and ability to handle breakdowns:
    asking/answering, clarifying, checking understanding, repairing communication.
    """
    turntaking: Subscore = Field(..., description="Initiating, maintaining, and yielding turns appropriately.")
    cooperation_strategies: Subscore = Field(..., description="Clarifying, confirming, and requesting clarification.")
    managing_breakdowns: Subscore = Field(..., description="Repair strategies to resolve misunderstandings.")
    overall_cefr: CEFRLevel = Field(..., description="Holistic CEFR level for spoken interaction.")
    overall_comment: str = Field(..., description="Interactional competence summary in CEFR terms.")

class PronunciationJudge(BaseModel):
    """
    LLM judge for CEFR Phonological Control (analytic scale in the Companion Volume).
    Evaluate (a) overall phonological control (intelligibility), (b) sound articulation,
    and (c) prosodic features (stress, rhythm, intonation). Accent is NOT penalized;
    rate intelligibility and control.
    """
    overall_phonological_control: Subscore = Field(..., description="Global intelligibility across the sample.")
    sound_articulation: Subscore = Field(..., description="Segmental clarity: consonants/vowels, reductions, elisions.")
    prosody: Subscore = Field(..., description="Stress, rhythm, and intonation supporting meaning and discourse.")
    overall_cefr: CEFRLevel = Field(..., description="Holistic CEFR level for phonological control.")
    overall_comment: str = Field(..., description="Notes on intelligibility and prosody using CEFR phrasing.")

class TaskAchievementJudge(BaseModel):
    """
    Optional: task adequacy for the speaking context (presentation, narrative, discussion).
    Map to 'Overall spoken production' or 'Overall spoken interaction' as relevant:
    whether communicative purpose is achieved at the expected depth/complexity.
    """
    relevance_and_coverage: Subscore = Field(..., description="Addresses the prompt fully and appropriately for the level.")
    functional_adequacy: Subscore = Field(..., description="Performs communicative functions expected at target level.")
    overall_cefr: CEFRLevel = Field(..., description="Holistic CEFR level for task adequacy.")
    overall_comment: str = Field(..., description="Target-level alignment for the specific task type.")

# ----------------------------
# Aggregate evaluation
# ----------------------------

class SpeakingEvaluation(BaseModel):
    """
    Container that aggregates all criterion judges for an end-to-end CEFR-oriented review.
    The 'overall' should consider weakest-strongest profiles and avoid simple averaging;
    encourage bands to be justified against CEFR language (e.g., 'can ...', 'shows control of ...').
    """
    target_level: Optional[CEFRLevel] = Field(None, description="If a target level was set for the task.")
    vocab: VocabJudge
    grammar: GrammarJudge
    fluency: FluencyJudge
    coherence: CoherenceJudge
    interaction: InteractionJudge
    pronunciation: PronunciationJudge
    task: Optional[TaskAchievementJudge] = Field(None, description="Include when the prompt has an explicit communicative task.")

    overall_level: CEFRLevel = Field(..., description="Holistic CEFR level for the performance (A1–C2).")
    overall_summary: str = Field(..., description="Short narrative tying subscores to a single CEFR decision.")
    global_recommendations: Optional[str] = Field(None, description="Top 3–5 priorities for moving toward the next band.")
