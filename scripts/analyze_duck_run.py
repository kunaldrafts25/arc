"""Audit actual model-gameplay evidence from a completed public notebook run."""
import argparse
import json
from pathlib import Path
from statistics import mean


def summarize(rows):
    if not rows:
        raise ValueError('No gameplay records')
    problems = []
    for row in rows:
        # A warmup RESET can happen before the model is ready. An action count
        # alone therefore cannot establish that inference/gameplay worked.
        if row['state'] in ('crashed','not_started'):
            problems.append(f"{row['game_id']}: {row['state']}")
        if row['actions'] <= 1 or row['generated_tokens'] <= 0:
            problems.append(f"{row['game_id']}: no substantive model-driven gameplay")
        if row['score'] is None:
            problems.append(f"{row['game_id']}: score unavailable")
    result = dict(model_gameplay_verified=not problems, problems=problems,
                  games=len(rows), levels=sum(r['levels_completed'] for r in rows),
                  full_wins=sum(r['total_levels']>0 and r['levels_completed']==r['total_levels'] for r in rows),
                  mean_public_score=mean(r['score'] for r in rows) if all(r['score'] is not None for r in rows) else None,
                  generated_tokens=sum(r['generated_tokens'] for r in rows),
                  notes={r['game_id']:r['note'] for r in rows if r.get('note')},
                  boundary='Public development gameplay only. Not a hidden score or proof of the 71-point goal.')
    return result


def analyze(directory):
    rows = json.loads((directory/'hydra_model_summary.json').read_text(encoding='utf-8'))
    result = summarize(rows)
    (directory/'analysis.json').write_text(json.dumps(result,indent=2)+'\n',encoding='utf-8')
    return result


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('directory',type=Path)
    args = parser.parse_args()
    result = analyze(args.directory)
    print(json.dumps(result,indent=2))
    if not result['model_gameplay_verified']:
        raise SystemExit(1)


if __name__ == '__main__':
    main()
