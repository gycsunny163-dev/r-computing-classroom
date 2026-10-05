from pathlib import Path
import argparse, json, os, re, shlex, shutil, subprocess, sys

REPO=Path(__file__).resolve().parents[1]
def quote_r_wrapper_paths(r):
    """Quote conda R's literal Unix paths; upstream wrappers can omit quotes."""
    if sys.platform=='win32':return
    wrapper=Path(r).resolve()
    original=wrapper.read_text(encoding='utf-8')
    if not original.startswith('#!'):return
    pattern=r'^(R_HOME_DIR|R_SHARE_DIR|R_INCLUDE_DIR|R_DOC_DIR)=(/[^\n]*)$'
    repaired=re.sub(pattern,lambda m:m[1]+'='+shlex.quote(m[2]),original,flags=re.M)
    if repaired==original:return
    backup=wrapper.with_name(wrapper.name+'.classroom-original')
    if not backup.exists():shutil.copy2(wrapper,backup)
    wrapper.write_text(repaired,encoding='utf-8')

def default_runtime():
    if sys.platform=='win32':
        return Path(os.environ['LOCALAPPDATA'])/'RClassroom-v1'
    return Path.home()/'Library/Application Support/RClassroom-v1'

def setup(runtime):
    runtime=Path(runtime).resolve()
    runtime.mkdir(parents=True,exist_ok=True)
    r=shutil.which('R')
    if not r:
        raise SystemExit('R was not found in this environment. Run setup again.')
    if not Path(r).resolve().is_relative_to((runtime/'environment').resolve()):
        raise SystemExit('R is outside the course environment. Run the course setup entry again.')
    quote_r_wrapper_paths(r)
    data=runtime/'data'
    kernel=data/'kernels/r-course';kernel.mkdir(parents=True,exist_ok=True)
    rhome=subprocess.check_output([r,'--vanilla','--slave','-e','cat(R.home())'],text=True).strip()
    spec={'argv':[r,'--vanilla','--slave','-e','IRkernel::main()','--args','{connection_file}'],
          'display_name':'R · Computing Classroom','language':'R','env':{'R_HOME':rhome}}
    (kernel/'kernel.json').write_text(json.dumps(spec,ensure_ascii=False,indent=2),encoding='utf-8')
    work=REPO/'work';work.mkdir(exist_ok=True)
    for template in (REPO/'course/lessons').glob('*.ipynb'):
        target=work/template.name
        if not target.exists():shutil.copy2(template,target)
    state=work/'learning-state.json'
    if not state.exists():
        state.write_text(json.dumps({'learning':'paused','mastery':'unassessed','records':[]},indent=2),encoding='utf-8')
    (runtime/'installation.json').write_text(json.dumps({'python':sys.executable,'R':r,'R_HOME':rhome,'kernel':'r-course'},ensure_ascii=False,indent=2),encoding='utf-8')
    os.environ['JUPYTER_DATA_DIR']=str(data)
    print(subprocess.check_output([r,'--vanilla','--slave','-e','cat(R.version.string)'],text=True).strip())
    print('R classroom setup complete. Student files in work/ are preserved.')
    return runtime

if __name__=='__main__':
    parser=argparse.ArgumentParser();parser.add_argument('--runtime',default=str(default_runtime()))
    setup(parser.parse_args().runtime)
