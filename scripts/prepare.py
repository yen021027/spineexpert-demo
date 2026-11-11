"""Import exact public Blogger text. No summaries or clinical rewrites."""
import json,re,urllib.request,html,hashlib
from html.parser import HTMLParser
from pathlib import Path
ROOT=Path(__file__).resolve().parent.parent
OUT=ROOT/'public';OUT.mkdir(exist_ok=True)
(OUT/'assets').mkdir(exist_ok=True)
class Plain(HTMLParser):
    def __init__(self): super().__init__();self.parts=[];self.skip=0
    def handle_starttag(self,t,a):
        if t in ('script','style','iframe'): self.skip+=1
        if not self.skip and t in ('p','div','br','li','h1','h2','h3','h4','tr'): self.parts.append('\n')
    def handle_endtag(self,t):
        if t in ('script','style','iframe'): self.skip=max(0,self.skip-1)
        if not self.skip and t in ('p','div','li','h1','h2','h3','h4','tr'): self.parts.append('\n')
    def handle_data(self,d):
        if not self.skip:self.parts.append(d)
    def result(self): return [re.sub(r'[\t\r \u00a0]+',' ',p).strip() for p in ''.join(self.parts).split('\n') if p.strip()]
def fetch(url):return urllib.request.urlopen(urllib.request.Request(url,headers={'User-Agent':'Mozilla/5.0'}),timeout=40).read()
groups=[('endoscopy','微創脊椎內視鏡','/p/blog-page_5.html'),('osteoporosis','骨質疏鬆與高齡脊椎手術','/p/blog-page_48.html'),('deformity','脊椎側彎與畸形','/p/blog-page_81.html'),('cervical','頸椎疾病診斷與治療','/p/blog-page_30.html'),('revision','脊椎翻修（revision）手術','/p/revision.html')]
categories=[]
for id,name,path in groups:
    url='http://spineexpert.blogspot.com'+path
    raw=fetch(url).decode('utf-8');links=set(re.findall(r'https?://spineexpert\.blogspot\.com/\d{4}/[^\s\"\'<>]+',html.unescape(raw)))
    categories.append(dict(id=id,name=name,url=url,links=links))
entries=json.loads((ROOT/'feed.json').read_text('utf-8'))['feed']['entry']
posts=[]
for e in entries:
    url=next(x['href'] for x in e['link'] if x['rel']=='alternate')
    parser=Plain();parser.feed(e.get('content',{}).get('$t',''))
    title=e['title']['$t'].translate(str.maketrans({',':'，',':':'：','?':'？','!':'！','(':'（',')':'）',';':'；'}))
    posts.append(dict(id=e['id']['$t'].split('post-')[-1],title=title,date=e['published']['$t'][:10],updated=e['updated']['$t'][:10],url=url,labels=[c['term'] for c in e.get('category',[])],categories=[c['id'] for c in categories if url in c['links'] or url.replace('http:','https:') in c['links']],paragraphs=parser.result()))
data=dict(source='http://spineexpert.blogspot.com/?m=1',imported='2026-11-11',posts=posts,categories=[{k:v for k,v in c.items() if k!='links'} for c in categories])
(OUT/'data.json').write_text(json.dumps(data,ensure_ascii=False,separators=(',',':')),encoding='utf-8')
h=(ROOT/'homepage.html').read_text('utf-8')
photo=re.search(r"class='profile-img'.*?src='([^']+)'",h).group(1)
if photo.startswith('//'):photo='https:'+photo
(OUT/'assets'/'doctor.jpg').write_bytes(fetch(photo.replace('/s220/','/s960/')))
print(json.dumps({'posts':len(posts),'categories':[{c['name']:sum(c['id'] in p['categories'] for p in posts)} for c in categories],'photo':photo},ensure_ascii=False))
