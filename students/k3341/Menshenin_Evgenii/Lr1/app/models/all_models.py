import sys
from pathlib import Path

sys.path.append(str(Path(__file__).parent.parent.parent))

from app.models.user import User, UserCreate, UserUpdate, UserRead, UserLogin
from app.models.hackathon import (
    Hackathon,
    HackathonCreate,
    HackathonUpdate,
    HackathonRead,
)
from app.models.participant import (
    Participant,
    ParticipantCreate,
    ParticipantUpdate,
    ParticipantRead,
    ParticipantWithHackathon,
)
from app.models.team import Team, TeamCreate, TeamUpdate, TeamRead
from app.models.task import Task, TaskCreate, TaskUpdate, TaskRead
from app.models.submission import (
    Submission,
    SubmissionCreate,
    SubmissionUpdate,
    SubmissionRead,
)
from app.models.evaluation import (
    Evaluation,
    EvaluationCreate,
    EvaluationUpdate,
    EvaluationRead,
)
from app.models.parsed_page import ParsedPage  # noqa: F401 — Lab 2 parsing table
