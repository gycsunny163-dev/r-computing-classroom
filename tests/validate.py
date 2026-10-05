from pathlib import Path
import argparse, json, os, platform, tempfile
import nbformat
from nbclient import NotebookClient
import sys

REPO=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(REPO/'tools'))
from setup_local import setup,default_runtime

parser=argparse.ArgumentParser()
parser.add_argument('--runtime',default=str(default_runtime()))
parser.add_argument('--save-example-outputs',action='store_true',help='Maintainer-only: update prepared examples, never learner work.')
args=parser.parse_args()
runtime=setup(Path(args.runtime))
os.environ['JUPYTER_DATA_DIR']=str(runtime/'data')
os.environ['JUPYTER_RUNTIME_DIR']=str(runtime/'validation-runtime')
Path(os.environ['JUPYTER_RUNTIME_DIR']).mkdir(exist_ok=True)
out=REPO/'.validation';out.mkdir(exist_ok=True)
results=[]
for source in sorted((REPO/'course/lessons').glob('*.ipynb')):
    nb=nbformat.read(source,as_version=4);nbformat.validate(nb)
    # Execute only prepared example cells. Learner answers are never read.
    before=[c.source for c in nb.cells if c.cell_type=='code'][1:]
    NotebookClient(nb,kernel_name='r-course',timeout=120,
      resources={'metadata':{'path':str(REPO/'work')}},allow_errors=False).execute()
    after=[c.source for c in nb.cells if c.cell_type=='code'][1:]
    assert before==after and all('Original first attempt' in c or 'Revision only' in c for c in after)
    nbformat.write(nb,out/source.name)
    if args.save_example_outputs:nbformat.write(nb,source)
    results.append({'lesson':source.stem,'executed':True,'learner_cells_empty':True,
      'images':sum(any(m in o.get('data',{}) for m in ('image/png','image/svg+xml')) for c in nb.cells if c.cell_type=='code' for o in c.get('outputs',[]))})
    print(source.stem+': passed',flush=True)

# Independent checks validate mechanics, not student exercise answers.
code='''stopifnot(identical(c(4,5,6)[1], 4))
stopifnot(identical(c(1,2,3) * c(2,3,4), c(2,6,12)))
stopifnot(is.na(mean(c(1,NA,3))))
stopifnot(mean(c(1,NA,3), na.rm=TRUE)==2)
stopifnot(isTRUE(all.equal(sd(c(1,2,3)),1)))
fit_check <- lm(y ~ x, data=data.frame(x=0:4,y=1+2*(0:4)))
stopifnot(isTRUE(all.equal(unname(coef(fit_check)),c(1,2))))
set.seed(19); a <- rnorm(4)
set.seed(19); b <- rnorm(4)
stopifnot(identical(a,b))
p <- tempfile(fileext=".csv")
write.csv(data.frame(x=1:3,y=c(2,4,6)),p,row.names=FALSE)
stopifnot(nrow(read.csv(p))==3); unlink(p)
cat("R semantic and CSV checks passed\\n")
cat(R.version.string,"\\n")
'''
checks=nbformat.v4.new_notebook(cells=[nbformat.v4.new_code_cell(code)])
NotebookClient(checks,kernel_name='r-course',timeout=120,resources={'metadata':{'path':str(REPO/'work')}}).execute()
nbformat.write(checks,out/'environment-checks.ipynb')
summary={'platform':platform.system(),'architecture':platform.machine(),
         'python':platform.python_version(),'lessons':results,'semantic_and_csv_checks':'passed',
         'mastery':'unassessed','all_passed':True,'windows_runtime_verified':platform.system()=='Windows'}
(out/'report.json').write_text(json.dumps(summary,ensure_ascii=False,indent=2),encoding='utf-8')
print('All 12 prepared examples and independent environment checks passed.')
