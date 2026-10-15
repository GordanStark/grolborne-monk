import sys,asyncio
from playwright.sync_api import sync_playwright
base=sys.argv[1]; pre=sys.argv[2]
tabs=[('start','?lv=1'),('path','?lv=34&open=1'),('spec','?lv=34'),('bars','?lv=34'),('bars','?lv=75'),('tank','?lv=34'),('profs','?lv=34'),('setup','?lv=34'),('ww','?lv=34')]
with sync_playwright() as p:
    b=p.chromium.launch(executable_path='/usr/bin/google-chrome',args=['--no-sandbox'])
    c=b.new_context(viewport={'width':390,'height':844},device_scale_factor=2,is_mobile=True)
    pg=c.new_page(); errs=[]
    pg.on('pageerror',lambda e:errs.append(str(e))); pg.on('console',lambda m:errs.append(m.text) if m.type=='error' else None)
    for t,q in tabs:
        pg.goto(f'{base}/{q}#{t}'); pg.wait_for_timeout(700)
        n=f'shots/{pre}-{t}{q.split("=")[1][:2] if "lv=" in q else ""}.png'
        pg.screenshot(path=n,full_page=False); 
        if t in('path','start'): pg.screenshot(path=n.replace('.png','-full.png'),full_page=True)
        print(n)
    pg.goto(f'{base}/?lv=34&rot=1#start'); pg.wait_for_timeout(500); pg.screenshot(path=f'shots/{pre}-rot.png')
    print('errors',errs); b.close()
