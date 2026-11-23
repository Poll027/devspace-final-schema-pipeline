/* Native Linux/POSIX path adapter, not a security sandbox. Maps only supplied
   /workspace and /usr/local/bin trees; all other paths use the host runtime. */
#define _GNU_SOURCE
#include <sys/ptrace.h>
#include <sys/wait.h>
#include <sys/user.h>
#include <sys/syscall.h>
#include <unistd.h>
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <signal.h>
#include <errno.h>
#include <limits.h>
static char root[PATH_MAX];
static void readmem(pid_t p,unsigned long a,void *out,size_t n){for(size_t i=0;i<n;i+=sizeof(long)){long v=ptrace(PTRACE_PEEKDATA,p,a+i,0);memcpy((char*)out+i,&v,n-i<sizeof(long)?n-i:sizeof(long));}}
static void writemem(pid_t p,unsigned long a,const void *in,size_t n){for(size_t i=0;i<n;i+=sizeof(long)){long v=ptrace(PTRACE_PEEKDATA,p,a+i,0);memcpy(&v,(char*)in+i,n-i<sizeof(long)?n-i:sizeof(long));ptrace(PTRACE_POKEDATA,p,a+i,v);}}
static int mapped(const char *p){return (!strncmp(p,"/workspace",10)&&(p[10]==0||p[10]=='/'))||(!strncmp(p,"/usr/local/bin",14)&&(p[14]==0||p[14]=='/'));}
static void patch(pid_t p,unsigned long *arg,unsigned long *buf){char s[PATH_MAX],t[PATH_MAX*2]; if(!*arg)return;size_t i;for(i=0;i<sizeof(s)-1;i++){readmem(p,*arg+i,s+i,1);if(!s[i])break;}s[sizeof(s)-1]=0;if(!mapped(s))return;snprintf(t,sizeof(t),"%s%s",root,s);writemem(p,*buf,t,strlen(t)+1);*arg=*buf;*buf+=sizeof(t);}
typedef struct {pid_t p;int entering;long nr;unsigned long out,len;struct user_regs_struct saved;} State;
static State states[4096];
static State *state(pid_t p){for(int i=0;i<4096;i++)if(states[i].p==p)return &states[i];for(int i=0;i<4096;i++)if(!states[i].p){states[i].p=p;states[i].entering=1;return &states[i];}exit(3);}
int main(int argc,char **argv){if(argc<3){fprintf(stderr,"usage: path_runtime ROOT COMMAND [ARG...]\n");return 2;}if(!realpath(argv[1],root)){perror("root");return 2;}pid_t child=fork();if(!child){ptrace(PTRACE_TRACEME,0,0,0);raise(SIGSTOP);execvp(argv[2],argv+2);perror("exec");_exit(127);}int status,rc=0;waitpid(child,&status,0);ptrace(PTRACE_SETOPTIONS,child,0,PTRACE_O_TRACESYSGOOD|PTRACE_O_TRACEFORK|PTRACE_O_TRACEVFORK|PTRACE_O_TRACECLONE|PTRACE_O_TRACEEXEC|PTRACE_O_EXITKILL);state(child);ptrace(PTRACE_SYSCALL,child,0,0);
while(1){pid_t p=waitpid(-1,&status,__WALL);if(p<0)break;State *s=state(p);if(WIFEXITED(status)||WIFSIGNALED(status)){if(p==child)rc=WIFEXITED(status)?WEXITSTATUS(status):128+WTERMSIG(status);s->p=0;continue;}int sig=WSTOPSIG(status),event=status>>16;if(event){if(event==PTRACE_EVENT_FORK||event==PTRACE_EVENT_VFORK||event==PTRACE_EVENT_CLONE){unsigned long np;ptrace(PTRACE_GETEVENTMSG,p,0,&np);State *ns=state(np);ns->entering=1;}if(event==PTRACE_EVENT_EXEC)s->entering=0;ptrace(PTRACE_SYSCALL,p,0,0);continue;}if(sig==(SIGTRAP|0x80)){struct user_regs_struct r;ptrace(PTRACE_GETREGS,p,0,&r);if(s->entering){s->saved=r;s->nr=r.orig_rax;s->out=0;unsigned long buf=r.rsp-32768;
#define A(x) patch(p,(unsigned long*)&r.x,&buf)
switch(r.orig_rax){
case SYS_open:case SYS_stat:case SYS_lstat:case SYS_access:case SYS_execve:case SYS_chdir:case SYS_mkdir:case SYS_rmdir:case SYS_unlink:case SYS_chmod:case SYS_truncate: A(rdi);break;
case SYS_openat:case SYS_newfstatat:case SYS_faccessat:case SYS_faccessat2:case SYS_mkdirat:case SYS_unlinkat:case SYS_fchmodat:case SYS_execveat:case SYS_utimensat:A(rsi);break;
case SYS_rename:case SYS_link:case SYS_symlink:A(rdi);A(rsi);break;
case SYS_renameat:case SYS_renameat2:case SYS_linkat:A(rsi);A(r10);break;
case SYS_symlinkat:A(rdi);A(rdx);break;
case SYS_readlink:s->out=r.rsi;s->len=r.rdx;A(rdi);break;
case SYS_readlinkat:s->out=r.rdx;s->len=r.r10;A(rsi);break;
case SYS_getcwd:s->out=r.rdi;s->len=r.rsi;break;
}ptrace(PTRACE_SETREGS,p,0,&r);
}else{if(s->out&&(long)r.rax>0){char t[PATH_MAX*2];size_t n=r.rax;if(n>=sizeof(t))n=sizeof(t)-1;readmem(p,s->out,t,n);t[n]=0;size_t k=strlen(root);if(!strncmp(t,root,k)&&mapped(t+k)){memmove(t,t+k,n-k+1);writemem(p,s->out,t,n-k);r.rax-=k;}}r.rdi=s->saved.rdi;r.rsi=s->saved.rsi;r.rdx=s->saved.rdx;r.r10=s->saved.r10;r.r8=s->saved.r8;r.r9=s->saved.r9;ptrace(PTRACE_SETREGS,p,0,&r);}s->entering=!s->entering;ptrace(PTRACE_SYSCALL,p,0,0);continue;}ptrace(PTRACE_SYSCALL,p,0,(sig==SIGSTOP||sig==SIGTRAP)?0:sig);}return rc;}
