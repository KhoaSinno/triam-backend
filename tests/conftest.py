"""
tests/conftest.py
=================
Shared fixtures cho toàn bộ test suite.
- sample_pdf: Tạo PDF thật có bookmarks + nội dung text để trigger TTS pipeline.
"""

import os
import uuid

import pytest
from fpdf import FPDF

from app.api.dependencies.auth import get_current_user
from app.main import app
from app.schemas.user import UserTokenPayload

SAMPLE_PDF_PATH = os.getenv("TEST_PDF_PATH", "tests/sample.pdf")
TEST_USER_ID = uuid.UUID("862d7c26-3160-4f76-9e77-07d91f7317cc")


def _test_current_user(user_id: uuid.UUID = TEST_USER_ID) -> UserTokenPayload:
    return UserTokenPayload(sub=user_id, email="test-user@triam.local", role="authenticated", aud="authenticated")


app.dependency_overrides[get_current_user] = _test_current_user


@pytest.fixture
def auth_as():
    def _set_user(user_id: uuid.UUID):
        app.dependency_overrides[get_current_user] = lambda: _test_current_user(user_id)

    yield _set_user
    app.dependency_overrides[get_current_user] = _test_current_user


def _build_test_pdf(pdf_path: str):
    """
    Tạo file PDF có 2 chương với bookmarks và nội dung tiếng Anh
    để pipeline parse_document_structure → learning units → LLM → TTS hoạt động đúng.
    """
    pdf = FPDF()
    pdf.set_auto_page_break(auto=True, margin=15)

    # ── CHAPTER 1 ────────────────────────────────────────────────────────────
    pdf.add_page()
    pdf.start_section("Chapter 1: The Science of Memory", level=0)
    pdf.set_font("Helvetica", "B", size=18)
    pdf.cell(0, 15, "Chapter 1: The Science of Memory",
             new_x="LMARGIN", new_y="NEXT")
    pdf.ln(5)

    pdf.set_font("Helvetica", size=12)
    body1 = (
        "Memory is one of the most fascinating abilities of the human brain. "
        "It allows us to store and retrieve vast amounts of information, from simple facts "
        "to complex skills and emotional experiences. Scientists have long studied how memory "
        "works, and today we understand it far better than ever before.\n\n"
        "There are three main types of memory: sensory memory, short-term memory, and "
        "long-term memory. Sensory memory holds a brief impression of what we perceive "
        "through our senses. Short-term memory, also called working memory, keeps a small "
        "amount of information active in our minds for a short period of time. Long-term "
        "memory stores information indefinitely and can hold an almost unlimited amount of data.\n\n"
        "The process of forming a memory involves three steps: encoding, storage, and retrieval. "
        "Encoding is the process of converting information into a format that can be stored. "
        "Storage is the maintenance of that information over time. Retrieval is the ability to "
        "access and bring stored information back into conscious awareness when needed.\n\n"
        "Research has shown that emotional experiences tend to be remembered more vividly "
        "than neutral ones. This is because the amygdala, a small almond-shaped structure in "
        "the brain, becomes activated during emotional events and enhances the storage of "
        "those memories in the hippocampus. This is why we often remember exactly where we "
        "were during major life events."
    )
    pdf.multi_cell(0, 8, body1)

    # ── CHAPTER 2 ────────────────────────────────────────────────────────────
    pdf.add_page()
    pdf.start_section("Chapter 2: Effective Learning Techniques", level=0)
    pdf.set_font("Helvetica", "B", size=18)
    pdf.cell(0, 15, "Chapter 2: Effective Learning Techniques",
             new_x="LMARGIN", new_y="NEXT")
    pdf.ln(5)

    pdf.set_font("Helvetica", size=12)
    body2 = (
        "Learning effectively is a skill that can be developed with the right strategies. "
        "Modern cognitive science has revealed several powerful techniques that can dramatically "
        "improve how quickly and thoroughly we learn new material.\n\n"
        "Spaced repetition is one of the most evidence-based methods for retaining information. "
        "Instead of cramming all studying into a single session, spaced repetition involves "
        "reviewing material at gradually increasing intervals. This takes advantage of the "
        "spacing effect, a phenomenon where our brains form stronger memories when learning "
        "is spread out over time rather than concentrated.\n\n"
        "Active recall is another powerful technique. Rather than passively re-reading notes, "
        "active recall means testing yourself on the material. This could involve closing your "
        "book and writing down everything you remember, or answering practice questions. "
        "The act of retrieving information from memory strengthens the neural pathways "
        "associated with that information, making future retrieval easier.\n\n"
        "The Pomodoro Technique helps manage attention and prevent burnout. It involves working "
        "in focused 25-minute intervals separated by short breaks. This structure prevents "
        "mental fatigue and keeps motivation high throughout a study session. Combined with "
        "good sleep, regular exercise, and a healthy diet, these learning techniques can help "
        "anyone become a more effective and confident learner."
    )
    pdf.multi_cell(0, 8, body2)

    os.makedirs(os.path.dirname(pdf_path) if os.path.dirname(
        pdf_path) else ".", exist_ok=True)
    pdf.output(pdf_path)
    print(f"\n  📄 Test PDF đã được tạo tại: {pdf_path}")


@pytest.fixture(scope="session")
def sample_pdf():
    """
    Trả về đường dẫn tới file PDF mẫu.
    - Nếu TEST_PDF_PATH đã tồn tại → dùng ngay (không override).
    - Nếu không → tự tạo PDF có 2 chương với bookmarks và nội dung thật.
    """
    if os.path.exists(SAMPLE_PDF_PATH):
        print(f"\n  📄 Dùng PDF mẫu có sẵn: {SAMPLE_PDF_PATH}")
        return SAMPLE_PDF_PATH

    _build_test_pdf(SAMPLE_PDF_PATH)
    return SAMPLE_PDF_PATH
