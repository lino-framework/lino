from time import sleep

from lino.ui import console

STEPS = 3

def work(ui,withMaxVal):
    
    if withMaxVal:
        job = ui.job("Job with maxval",maxval=pow(STEPS,5))
    else:
        job = ui.job("Job without maxval")
    
    job.status("Working hard")
    for n in range(1,STEPS+1):
        job.error('error message %d',n)
        for h in range(1,STEPS+1):
            job.warning('warning message %d.%d',n,h)
            for i in range(1,STEPS+1):
                job.notice('notice message %d.%d.%d',n,h,i)
                for j in range(1,STEPS+1):
                    job.verbose(
                        'verbose message %d.%d.%d.%d',n,h,i,j)
                    for k in range(1,STEPS+1):
                        job.debug(
                            'debug message %d.%d.%d.%d.%d',n,h,i,j,k)
                        job.increment()
                        sleep(0.05)
        
    job.done()


if __name__ == "__main__":
    #print __doc__
    console.parse_args()
    work(console,True)
    work(console,False)
    
    
