import io
import json
from pathlib import Path
import sys
import unittest
from unittest.mock import patch
from urllib.error import HTTPError

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / 'scripts'))
from check_external_links import check


class Response(io.BytesIO):
    status = 200
    url = 'https://www.youtube.com/watch?v=abcdefghijk'


class ResourceLinkTests(unittest.TestCase):
    url = 'https://www.youtube.com/watch?v=abcdefghijk'

    def player(self, status='OK', video='abcdefghijk'):
        return Response(('var ytInitialPlayerResponse = '+json.dumps({
            'playabilityStatus': {'status': status},
            'videoDetails': {'videoId':video,'title':'Lecture','author':'Author','lengthSeconds':'123'}
        })+';').encode())

    def metadata(self, video='abcdefghijk'):
        return Response(json.dumps({'type':'video','provider_name':'YouTube','title':'Lecture',
                                    'author_name':'Author','html':f'<iframe src="https://www.youtube.com/embed/{video}"></iframe>'}).encode())

    def test_public_playback(self):
        with patch('check_external_links.urlopen', return_value=self.player()):
            row=check(self.url)
        self.assertEqual(row['status'],'PASS')
        self.assertEqual(row['duration_seconds'],123)

    def test_signin_restriction_is_metadata_only(self):
        with patch('check_external_links.urlopen', side_effect=[self.player('LOGIN_REQUIRED'),self.metadata()]):
            row=check(self.url)
        self.assertEqual(row['status'],'METADATA_ONLY')
        self.assertFalse(row['playback_verified'])
        self.assertNotIn('duration_seconds',row)

    def test_other_video_metadata_is_not_accepted(self):
        with patch('check_external_links.urlopen', side_effect=[self.player('LOGIN_REQUIRED'),self.metadata('other_video')]):
            self.assertEqual(check(self.url)['status'],'UNVERIFIED')

    def test_removed_link(self):
        with patch('check_external_links.urlopen', side_effect=HTTPError(self.url,404,'Not found',None,None)):
            self.assertEqual(check(self.url)['status'],'BROKEN')

    def test_rate_limit_is_not_claimed_broken(self):
        with patch('check_external_links.urlopen', side_effect=HTTPError(self.url,429,'Too many requests',None,None)):
            self.assertEqual(check(self.url)['status'],'UNVERIFIED')

    def test_missing_metadata_is_not_a_pass(self):
        with patch('check_external_links.urlopen', return_value=Response(b'Consent or temporary error')):
            self.assertEqual(check(self.url)['status'],'UNVERIFIED')


if __name__ == '__main__':
    unittest.main()
