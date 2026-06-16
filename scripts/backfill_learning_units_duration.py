import argparse
import sys
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parents[1]
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

from sqlmodel import Session, select  # noqa: E402

from app.core.constant import ProcessingJobStatus  # noqa: E402
from app.db.database import engine  # noqa: E402
from app.models.db_models import LearningUnit, LearningUnitSegment  # noqa: E402


def _parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Backfill actual audio duration for READY learning units.")
    parser.add_argument("--dry-run", action="store_true", help="Print updates without committing them to the database.")
    return parser.parse_args()


def main() -> None:
    args = _parse_args()
    
    with Session(engine) as session:
        statement = select(LearningUnit).where(
            LearningUnit.status == ProcessingJobStatus.READY.value
        )
        ready_units = list(session.exec(statement).all())
        
        print(f"Found {len(ready_units)} READY learning units to backfill.")
        
        updated_count = 0
        for unit in ready_units:
            # Fetch segments
            seg_statement = select(LearningUnitSegment).where(
                LearningUnitSegment.learning_unit_id == unit.id
            )
            segments = list(session.exec(seg_statement).all())
            
            if not segments:
                print(f"Skipping Unit '{unit.title}' (ID: {unit.id}) - No segments found.")
                continue
                
            total_ms = sum(seg.duration_ms or 0 for seg in segments)
            generated_seconds = int(total_ms / 1000)
            
            if unit.estimated_audio_seconds != generated_seconds:
                print(
                    f"Updating Unit '{unit.title}' (ID: {unit.id}) | "
                    f"Old estimated_audio_seconds: {unit.estimated_audio_seconds}s -> "
                    f"New: {generated_seconds}s (based on {len(segments)} segments)."
                )
                unit.estimated_audio_seconds = generated_seconds
                session.add(unit)
                updated_count += 1
            else:
                print(f"Unit '{unit.title}' already has correct duration {generated_seconds}s. Skipping.")
                
        if not args.dry_run:
            session.commit()
            print(f"Successfully committed {updated_count} updates to the database.")
        else:
            print(f"[Dry Run] Would have committed {updated_count} updates.")


if __name__ == "__main__":
    main()
