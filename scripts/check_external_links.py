"""Check learner-facing links without credentials or media downloads."""
import argparse
from concurrent.futures import ThreadPoolExecutor
from datetime import datetime, timezone
import html
import json
from pathlib import Path
import re
from urllib.error import HTTPError
from urllib.parse import urlsplit, parse_qs, urlencode
from urllib.request import Request, urlopen


def collect(root):
    links = set()
    for path in Path(root).rglob('*'):
        if not path.is_file() or any(p in {'.git', '.venv', '__pycache__'} for p in path.parts):
            continue
        if path.suffix not in {'.md', '.html', '.yml', '.ipynb'}:
            continue
        text = path.read_text(encoding='utf-8')
        if path.suffix == '.ipynb':
            text = '\n'.join(''.join(c['source']) for c in json.loads(text)['cells'] if c['cell_type']=='markdown')
        for url in re.findall(r'https://[^\s<>"\]\)\}]+', text):
            url = html.unescape(url).rstrip("'.,;")
            if '{' in url or '${' in url:
                continue
            links.add(url.split('#')[0])
    return sorted(links)


def check(url):
    item = {'url': url, 'status': 'UNVERIFIED'}
    try:
        request = Request(url, headers={'User-Agent': 'Mozilla/5.0 (compatible; CourseLinkCheck/1.0)'})
        with urlopen(request, timeout=25) as response:
            body = response.read(4*1024*1024).decode('utf-8', errors='replace')
            item.update(http_status=response.status, final_url=response.url)
        if urlsplit(url).hostname in {'www.youtube.com', 'youtube.com'}:
            video = parse_qs(urlsplit(url).query).get('v', [''])[0]
            marker = re.search(r'(?:var )?ytInitialPlayerResponse\s*=\s*', body)
            if not video or not marker:
                raise ValueError('Video metadata unavailable; review manually.')
            player = json.JSONDecoder().raw_decode(body[marker.end():])[0]
            detail = player.get('videoDetails', {})
            status = player.get('playabilityStatus', {}).get('status')
            if status != 'OK' or detail.get('videoId') != video or detail.get('isPrivate'):
                # YouTube may require sign-in from data-center addresses. Its public
                # oEmbed endpoint can confirm the exact video's metadata, not playback.
                endpoint = 'https://www.youtube.com/oembed?' + urlencode({'url': url, 'format': 'json'})
                with urlopen(Request(endpoint, headers={'User-Agent': 'CourseLinkCheck/1.0'}), timeout=25) as response:
                    metadata = json.load(response)
                if (metadata.get('type') != 'video' or metadata.get('provider_name') != 'YouTube'
                        or '/embed/' + video not in metadata.get('html', '')
                        or not metadata.get('title') or not metadata.get('author_name')):
                    raise ValueError('Exact video metadata not confirmed; review manually.')
                item.update(status='METADATA_ONLY', title=metadata['title'], channel=metadata['author_name'],
                            playback_verified=False, detail='Public oEmbed metadata verified; playback requires a browser review.')
                return item
            item.update(title=detail['title'], channel=detail['author'], duration_seconds=int(detail['lengthSeconds']))
        elif 'accounts.google.com' in item['final_url'] and 'colab.research.google.com' in url:
            item.update(status='SIGN_IN_REQUIRED', detail='Colab sign-in is expected; validate notebook source separately.')
            return item
        item['status'] = 'PASS'
    except HTTPError as error:
        item.update(http_status=error.code, status='BROKEN' if error.code in {404,410} else 'UNVERIFIED', detail=str(error))
    except (OSError, ValueError, KeyError, TypeError) as error:
        item['detail'] = str(error)[:240]
    return item


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--root', default='.')
    parser.add_argument('--course-dir')
    parser.add_argument('--output', default='.check-output/external-links.json')
    args = parser.parse_args()
    urls = set(collect(args.root))
    if args.course_dir:
        urls.update(collect(args.course_dir))
    with ThreadPoolExecutor(max_workers=4) as pool:
        results = list(pool.map(check, sorted(urls)))
    counts = {status: sum(r['status']==status for r in results) for status in ['PASS','METADATA_ONLY','SIGN_IN_REQUIRED','UNVERIFIED','BROKEN']}
    report = {'checked_at_utc': datetime.now(timezone.utc).isoformat(), 'counts': counts, 'results': results,
              'scope': 'Public URL availability and video metadata, not a grade or a full media playback test.'}
    output = Path(args.output); output.parent.mkdir(parents=True, exist_ok=True)
    output.write_text(json.dumps(report, ensure_ascii=False, indent=2), encoding='utf-8')
    print(json.dumps(counts))
    for row in results:
        if row['status'] not in {'PASS','SIGN_IN_REQUIRED'}: print(row['status'], row['url'], row.get('detail',''))
    raise SystemExit(1 if counts['BROKEN'] else 2 if counts['UNVERIFIED'] else 0)


if __name__ == '__main__':
    main()
