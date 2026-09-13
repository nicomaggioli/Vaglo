"""Validate media range handling without opening a network listener."""
import importlib.util
import io
from pathlib import Path
from unittest import TestCase,main
ROOT=Path(__file__).resolve().parents[1]
spec=importlib.util.spec_from_file_location('preview', ROOT/'serve.py');m=importlib.util.module_from_spec(spec);spec.loader.exec_module(m)
class RangeTests(TestCase):
 def request(self, header):
  h=object.__new__(m.NoCache);h.path='/assets/trailer.vtt';h.headers={'Range':header};h.translate_path=lambda _:str(ROOT/'assets/trailer.vtt');h.response_headers={};h.send_response=lambda s:setattr(h,'status',s);h.send_header=lambda k,v:h.response_headers.update({k:v});h.end_headers=lambda:None
  f=h.send_head();out=io.BytesIO()
  if f:
   with f:h.copyfile(f,out)
  return h,out.getvalue()
 def test_partial(self):
  h,b=self.request('bytes=2-12');self.assertEqual(h.status,206);self.assertEqual(b,(ROOT/'assets/trailer.vtt').read_bytes()[2:13]);self.assertEqual(h.response_headers['Content-Length'],'11')
 def test_suffix(self):
  h,b=self.request('bytes=-8');self.assertEqual(h.status,206);self.assertEqual(b,(ROOT/'assets/trailer.vtt').read_bytes()[-8:])
 def test_open_ended(self):
  h,b=self.request('bytes=10-');self.assertEqual(b,(ROOT/'assets/trailer.vtt').read_bytes()[10:])
 def test_invalid(self):
  for r in ['bytes=99999-','bytes=20-10','bytes=-0','bytes=-','bytes=0-1,3-4']:
   with self.subTest(r=r):
    h,b=self.request(r);self.assertEqual(h.status,416);self.assertEqual(b,b'')
if __name__=='__main__':main()
