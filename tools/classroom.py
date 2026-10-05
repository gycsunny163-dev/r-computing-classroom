from pathlib import Path
import argparse, hashlib, json, os, platform, subprocess, sys, time, urllib.request, webbrowser
import psutil
from setup_local import default_runtime, setup

REPO=Path(__file__).resolve().parents[1]
def request(state,endpoint,method='GET'):
    req=urllib.request.Request(state['base_url']+endpoint,method=method,
        headers={'Authorization':'token '+state['token']})
    return urllib.request.urlopen(req,timeout=4)
def reachable(state):
    try:
        with request(state,'/api') as response:return response.status==200
    except Exception:return False
def owned_process(state):
    try:
        p=psutil.Process(state['pid']);cmd=p.cmdline()
        return any('jupyterlab' in a for a in cmd) and '--ServerApp.root_dir='+str(REPO) in cmd
    except (KeyError,psutil.Error):return False
def open_url(url):
    if sys.platform=='darwin':
        result=subprocess.run(['open','-a','Google Chrome',url],stdout=subprocess.DEVNULL,stderr=subprocess.DEVNULL)
        if result.returncode==0:return
    if sys.platform=='win32':
        for root in ('PROGRAMFILES','PROGRAMFILES(X86)','LOCALAPPDATA'):
            chrome=Path(os.environ.get(root,''))/'Google/Chrome/Application/chrome.exe'
            if chrome.is_file():subprocess.Popen([str(chrome),url]);return
    if not webbrowser.open(url):raise SystemExit('Could not open a browser. Check browser installation.')

def main():
    parser=argparse.ArgumentParser()
    parser.add_argument('--runtime',default=str(default_runtime()))
    parser.add_argument('--stop',action='store_true')
    parser.add_argument('--no-open',action='store_true')
    parser.add_argument('--lesson',choices=[f'R{i:02}' for i in range(1,13)])
    args=parser.parse_args()
    runtime=Path(args.runtime).resolve()
    session=runtime/'sessions'/hashlib.sha256(str(REPO).encode()).hexdigest()[:16]
    session.mkdir(parents=True,exist_ok=True)
    state_path=session/'state.json'
    try:state=json.loads(state_path.read_text())
    except (OSError,ValueError):state=None
    if args.stop:
        if state and reachable(state):
            if not owned_process(state):raise SystemExit('Cannot confirm this service belongs to this classroom; stop cancelled.')
            with request(state,'/api/shutdown','POST'):pass
            for _ in range(40):
                if not reachable(state):break
                time.sleep(.2)
            if reachable(state):raise SystemExit('Service has not stopped; keep this window for diagnosis.')
        elif state and owned_process(state):
            raise SystemExit('This service is still running but inaccessible. No files or processes were removed.')
        state_path.unlink(missing_ok=True)
        print('Classroom closed. Saved work is preserved.');return
    setup(runtime)
    if state and not reachable(state) and owned_process(state):
        raise SystemExit('Classroom process exists but cannot be reached. Keep this window for diagnosis; no running kernel was removed.')
    if not state or not reachable(state):
        env=os.environ.copy();env.update(JUPYTER_RUNTIME_DIR=str(session),JUPYTER_DATA_DIR=str(runtime/'data'),
            JUPYTER_CONFIG_DIR=str(runtime/'config'),IPYTHONDIR=str(runtime/'ipython'),PYTHONUNBUFFERED='1')
        command=[sys.executable,'-m','jupyterlab','--no-browser','--ServerApp.ip=127.0.0.1',
          '--ServerApp.port=8893','--ServerApp.port_retries=20','--ServerApp.root_dir='+str(REPO),
          '--ServerApp.default_url=/lab/tree/START.ipynb']
        options={'start_new_session':True} if sys.platform!='win32' else {
            'creationflags':subprocess.CREATE_NEW_PROCESS_GROUP | subprocess.DETACHED_PROCESS}
        with (session/'server.log').open('a',encoding='utf-8') as log:
            process=subprocess.Popen(command,cwd=REPO,env=env,stdin=subprocess.DEVNULL,stdout=log,stderr=log,**options)
        state=None
        for _ in range(200):
            for info in session.glob('jpserver-*.json'):
                try:
                    data=json.loads(info.read_text())
                    if data.get('pid')!=process.pid:continue
                    candidate={'pid':process.pid,'base_url':data['url'].rstrip('/'),'token':data['token'],'repo':str(REPO)}
                    if reachable(candidate):state=candidate;break
                except (OSError,ValueError,KeyError):continue
            if state:break
            if process.poll() is not None:raise SystemExit('Jupyter failed to start. See the local server.log; do not publish authentication tokens.')
            time.sleep(.2)
        if not state:
            process.terminate();raise SystemExit('Startup timed out; only the process created by this invocation was stopped.')
        state_path.write_text(json.dumps(state),encoding='utf-8')
        if sys.platform!='win32':state_path.chmod(0o600)
    path='/lab/tree/'+('work/'+args.lesson+'.ipynb' if args.lesson else 'START.ipynb')
    if not args.no_open:
        open_url(state['base_url']+path+'?token='+state['token'])
        if args.lesson:
            prompt=REPO/'tutor'/f'{args.lesson}.txt'
            if sys.platform=='darwin':subprocess.run(['open','-a','TextEdit',str(prompt)],check=True)
            elif sys.platform=='win32':os.startfile(str(prompt))
            open_url('https://aistudio.google.com/prompts/new_chat')
    print('R classroom ready. '+('Copy the selected tutor text to your AI tutor; nothing was submitted automatically.' if args.lesson else 'Learning is not started automatically.'))
if __name__=='__main__':main()
