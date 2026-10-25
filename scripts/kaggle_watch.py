"""Observe one exact Kaggle version through long, quiet compilation stages."""
import argparse
from contextlib import redirect_stderr, redirect_stdout
import os
from pathlib import Path
import re

ROOT=Path(__file__).resolve().parents[1]


def main():
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('kernel',help='Exact owner/slug/version; never follows latest')
    parser.add_argument('--output',type=Path,required=True)
    args=parser.parse_args()
    if not re.fullmatch(r'[A-Za-z0-9_-]+/[A-Za-z0-9_-]+/[1-9][0-9]*',args.kernel):
        parser.error('An exact owner/slug/version is required')
    output=(ROOT/args.output).resolve()
    if not output.is_relative_to(ROOT):
        parser.error('Observer output must remain in the project')
    os.environ['KAGGLE_API_TOKEN']=(ROOT/'.kaggle/access_token').read_text(encoding='utf-8-sig').strip()
    os.environ['KAGGLE_CONFIG_DIR']=str(ROOT/'.kaggle')
    from kaggle.api.kaggle_api_extended import KaggleApi
    api=KaggleApi()
    api.authenticate()
    # Installed CLI 2.2.5 uses these limits to reconnect and deduplicate SSE
    # events. Quiet native compilation can outlast the default five failures.
    # Only observation changes: no save, push, cancellation or submission calls.
    if not hasattr(api,'_LOG_STREAM_MAX_FAILURES'):
        raise RuntimeError('Inspect the installed SDK log-stream API before using this observer')
    api._LOG_STREAM_MAX_FAILURES=120
    api._LOG_STREAM_RECONNECT_DELAY_SEC=5
    output.parent.mkdir(parents=True,exist_ok=True)
    # Retain the encoding of existing PowerShell-captured live logs.
    with output.open('w',encoding='utf-16') as stream, redirect_stdout(stream), redirect_stderr(stream):
        print('Observing exact version:',args.kernel,flush=True)
        try:
            api.kernels_logs_cli(args.kernel,follow=True)
        finally:
            # A returned/failed observer is not a terminal cloud-job result.
            try:
                print('Observer ended; authoritative cloud status:',api.kernels_status(args.kernel).status,flush=True)
            except Exception as exc:
                print('Observer ended; cloud status unavailable:',type(exc).__name__,flush=True)


if __name__=='__main__':
    main()
