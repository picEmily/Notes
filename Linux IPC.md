参考：https://blog.csdn.net/piaojun_pj/article/details/5943736

排版以及加注释

# Linux进程通信
linux中的进程通信分为三个部分：低级通信，管道通信和进程间通信IPC（inter process communication）。linux的低级通信主要用来传递进程的控制信号——文件锁和软中断信号机制。linux的进程间通信IPC有三个部分——①信号量，②共享内存和③消息队列。以下是我编写的linux进程通信的C语言实现代码。操作系统为redhat9.0，编辑器为vi，编译器采用gcc。下面所有实现代码均已经通过测试，运行无误。

 

一.低级通信--信号通信

 

signal.c



#include <signal.h>
#include <stdio.h>
#include <unistd.h>

 

/*捕捉到信号sig之后，执行预先预定的动作函数*/
void sig_alarm(int sig)
{
 printf("---the signal received is %d. /n", sig);
 signal(SIGINT, SIG_DFL); //SIGINT终端中断信号，SIG_DFL：恢复默认行为，SIN_IGN：忽略信号
}

 

int main()
{
 signal(SIGINT, sig_alarm);//捕捉终端中断信号

 while(1)
 {
  printf("waiting here!/n");
  sleep(1);
 }
 return 0;
}

 

二.管道通信

 

pipe.c

 

#include <stdio.h>

#define BUFFER_SIZE 30


int main()
{
 int x;
 int fd[2];
 char buf[BUFFER_SIZE];
 char s[BUFFER_SIZE];
 pipe(fd);//创建管道

 while((x=fork())==-1);//创建管道失败时，进入循环
 
 /*进入子进程，子进程向管道中写入一个字符串*/
 if(x==0)
 {
  sprintf(buf,"This is an example of pipe!/n");
  write(fd[1],buf,BUFFER_SIZE);
  exit(0);
 }

 

 /*进入父进程，父进程从管道的另一端读出刚才写入的字符串*/
 else
 {
  wait(0);//等待子进程结束
  read(fd[0],s,BUFFER_SIZE);//读出字符串，并将其储存在char s[]中
  printf("%s",s);//打印字符串
 }
 return 0;
}

 

三.进程间通信——IPC

 

①信号量通信

 

sem.c

 

#include <unistd.h>
#include <stdlib.h>
#include <stdio.h>
#include <sys/types.h>
#include <sys/ipc.h>
#include <sys/sem.h>

 

/*联合体变量*/
union semun
{
 int val; //信号量初始值                  
 struct semid_ds *buf;       
 unsigned short int *array; 
 struct seminfo *__buf;     
};

 

/*函数声明，信号量定义*/
static int set_semvalue(void); //设置信号量
static void del_semvalue(void);//删除信号量
static int semaphore_p(void);  //执行P操作
static int semaphore_v(void);  //执行V操作
static int sem_id;             //信号量标识符

 

int main(int argc, char *argv[])
{
 int i;
 int pause_time;
 char op_char = 'O';
 srand((unsigned int)getpid()); 
 sem_id = semget((key_t)1234, 1, 0666 | IPC_CREAT);//创建一个信号量,IPC_CREAT表示创建一个新的信号量
 
 /*如果有参数，设置信号量，修改字符*/
 if (argc > 1)
 {
  if (!set_semvalue())
  {
   fprintf(stderr, "Failed to initialize semaphore/n");
   exit(EXIT_FAILURE);
  }
  op_char = 'X';
  sleep(5);
 }

 for(i = 0; i < 10; i++)  
 {      


  /*执行P操作*/
  if (!semaphore_p())
   exit(EXIT_FAILURE);

  printf("%c", op_char);
  fflush(stdout);
  pause_time = rand() % 3;
  sleep(pause_time);
  printf("%c", op_char);
  fflush(stdout);

 

  /*执行V操作*/
  if (!semaphore_v())
   exit(EXIT_FAILURE);

  pause_time = rand() % 2;
  sleep(pause_time);
 }  
 printf("/n%d - finished/n", getpid());

 if (argc > 1)
 {   
  sleep(10);
  del_semvalue(); //删除信号量
 }   
 exit(EXIT_SUCCESS);
}

 

/*设置信号量*/
static int set_semvalue(void)
{
 union semun sem_union;
 sem_union.val = 1;
 if (semctl(sem_id, 0, SETVAL, sem_union) == -1)
  return(0);
 
 return(1);
}

 

/*删除信号量*/
static void del_semvalue(void)
{
 union semun sem_union; 
 if (semctl(sem_id, 0, IPC_RMID, sem_union) == -1)
  fprintf(stderr, "Failed to delete semaphore/n");
}

 

/*执行P操作*/
static int semaphore_p(void)
{
 struct sembuf sem_b;  
 sem_b.sem_num = 0;
 sem_b.sem_op = -1; /* P() */
 sem_b.sem_flg = SEM_UNDO;
 if (semop(sem_id, &sem_b, 1) == -1)
 {
  fprintf(stderr, "semaphore_p failed/n");
  return(0);
 }
 return(1);
}


/*执行V操作*/
static int semaphore_v(void)
{
 struct sembuf sem_b;
 sem_b.sem_num = 0;
 sem_b.sem_op = 1; /* V() */
 sem_b.sem_flg = SEM_UNDO;
 if (semop(sem_id, &sem_b, 1) == -1)
 {
  fprintf(stderr, "semaphore_v failed/n");
  return(0);
 }
 return(1);
}

 

②消息队列通信

 

send.c

 

#include <stdlib.h>
#include <stdio.h>
#include <string.h>
#include <errno.h>
#include <unistd.h>
#include <sys/types.h>
#include <sys/ipc.h>
#include <sys/msg.h>
#define MAX_TEXT 512

 

/*用于消息收发的结构体--my_msg_type：消息类型，some_text：消息正文*/
struct my_msg_st
{
 long int my_msg_type;
 char some_text[MAX_TEXT];
};

 

int main()
{
 int running = 1;//程序运行标识符
 struct my_msg_st some_data;
 int msgid;//消息队列标识符
 char buffer[BUFSIZ];

 

 /*创建与接受者相同的消息队列*/
 msgid = msgget((key_t)1234, 0666 | IPC_CREAT);
 if (msgid == -1)
 {
  fprintf(stderr, "msgget failed with error: %d/n", errno);
  exit(EXIT_FAILURE);
    }

 

 /*向消息队列中发送消息*/
 while(running)
 {
  printf("Enter some text: ");
  fgets(buffer, BUFSIZ, stdin);
  some_data.my_msg_type = 1;
  strcpy(some_data.some_text, buffer);
  if (msgsnd(msgid, (void *)&some_data, MAX_TEXT, 0) == -1)
  {
   fprintf(stderr, "msgsnd failed/n");
   exit(EXIT_FAILURE);
  }
  if (strncmp(buffer, "end", 3) == 0)
  {
   running = 0;
  }
 }
 exit(EXIT_SUCCESS);
}

 

receive.c

 

#include <stdlib.h>
#include <stdio.h>
#include <string.h>
#include <errno.h>
#include <unistd.h>
#include <sys/types.h>
#include <sys/ipc.h>
#include <sys/msg.h>

 

/*用于消息收发的结构体--my_msg_type：消息类型，some_text：消息正文*/
struct my_msg_st
{
 long int my_msg_type;
 char some_text[BUFSIZ];
};

 

int main()
{
 int running = 1;//程序运行标识符
 int msgid; //消息队列标识符
 struct my_msg_st some_data;
 long int msg_to_receive = 0;//接收消息的类型--0表示msgid队列上的第一个消息

 

 /*创建消息队列*/
 msgid = msgget((key_t)1234, 0666 | IPC_CREAT);
 if (msgid == -1)
 {
  fprintf(stderr, "msgget failed with error: %d/n", errno);
  exit(EXIT_FAILURE);
 }

 

 /*接收消息*/
 while(running)
 {
  if (msgrcv(msgid, (void *)&some_data, BUFSIZ,msg_to_receive, 0) == -1)
  {
   fprintf(stderr, "msgrcv failed with error: %d/n", errno);
   exit(EXIT_FAILURE);
  }
  printf("You wrote: %s", some_data.some_text);
  if (strncmp(some_data.some_text, "end", 3) == 0)
  {
   running = 0;
  }
 }

 

 /*删除消息队列*/
 if (msgctl(msgid, IPC_RMID, 0) == -1)
 {
  fprintf(stderr, "msgctl(IPC_RMID) failed/n");
  exit(EXIT_FAILURE);
 }
 exit(EXIT_SUCCESS);
}

 

③共享内存通信

 

share.h

 

#define TEXT_SZ 2048 //申请共享内存大小

struct shared_use_st
{
 int written_by_you; //written_by_you为1时表示有数据写入，为0时表示数据已经被消费者提走
 char some_text[TEXT_SZ];
};

 

producer.c

 

#include <unistd.h>
#include <stdlib.h>
#include <stdio.h>
#include <string.h>
#include <sys/types.h>
#include <sys/ipc.h>
#include <sys/shm.h>
#include "share.h"


int main()
{
 int running = 1; //程序运行标志位
 void *shared_memory = (void *)0;
 struct shared_use_st *shared_stuff;
 char buffer[BUFSIZ];
 int shmid; //共享内存标识符

 

 /*创建共享内存*/
 shmid = shmget((key_t)1234, sizeof(struct shared_use_st), 0666 | IPC_CREAT);
 if (shmid == -1)
 {
  fprintf(stderr, "shmget failed/n");
  exit(EXIT_FAILURE);
 }

 

 /*将共享内存连接到一个进程的地址空间中*/
 shared_memory = shmat(shmid, (void *)0, 0);//指向共享内存第一个字节的指针
 if (shared_memory == (void *)-1)
 {
  fprintf(stderr, "shmat failed/n");
  exit(EXIT_FAILURE);
 }

 printf("Memory attached at %X/n", (int)shared_memory);
 shared_stuff = (struct shared_use_st *)shared_memory;

 

 /*生产者写入数据*/
 while(running)
 {
  while(shared_stuff->written_by_you == 1)
  {
   sleep(1);           
   printf("waiting for client.../n");
  }
  printf("Enter some text: ");
  fgets(buffer, BUFSIZ, stdin);
  strncpy(shared_stuff->some_text, buffer, TEXT_SZ);
  shared_stuff->written_by_you = 1;
  if (strncmp(buffer, "end", 3) == 0)
  {
   running = 0;
  }
 }

 

    /*该函数用来将共享内存从当前进程中分离,仅使得当前进程不再能使用该共享内存*/
 if (shmdt(shared_memory) == -1)
 {
  fprintf(stderr, "shmdt failed/n");
  exit(EXIT_FAILURE);
 }

 printf("producer exit./n");
 exit(EXIT_SUCCESS);
}

 

customer.c

 

#include <unistd.h>
#include <stdlib.h>
#include <stdio.h>
#include <string.h>
#include <sys/types.h>
#include <sys/ipc.h>
#include <sys/shm.h>
#include "share.h"


int main()
{
 int running = 1;//程序运行标志位
 void *shared_memory = (void *)0;
 struct shared_use_st *shared_stuff;
 int shmid; //共享内存标识符
 srand((unsigned int)getpid());   

 

 /*创建共享内存*/
 shmid = shmget((key_t)1234, sizeof(struct shared_use_st), 0666 | IPC_CREAT);
 if (shmid == -1)
 {
  fprintf(stderr, "shmget failed/n");
  exit(EXIT_FAILURE);
 }

 

 /*将共享内存连接到一个进程的地址空间中*/
 shared_memory = shmat(shmid, (void *)0, 0);//指向共享内存第一个字节的指针
 if (shared_memory == (void *)-1)
 {
  fprintf(stderr, "shmat failed/n");
  exit(EXIT_FAILURE);
 }

 printf("Memory attached at %X/n", (int)shared_memory);
 shared_stuff = (struct shared_use_st *)shared_memory;
 shared_stuff->written_by_you = 0;

 

 /*消费者读取数据*/
 while(running)
 {
  if (shared_stuff->written_by_you)
  {
   printf("You wrote: %s", shared_stuff->some_text);
   sleep( rand() % 4 ); 
   shared_stuff->written_by_you = 0;
   if (strncmp(shared_stuff->some_text, "end", 3) == 0)
   {
    running = 0;
   }
  }
 }

 

 /*该函数用来将共享内存从当前进程中分离,仅使得当前进程不再能使用该共享内存*/
 if (shmdt(shared_memory) == -1)
 {
  fprintf(stderr, "shmdt failed/n");
  exit(EXIT_FAILURE);
 }

 

 /*将共享内存删除,所有进程均不能再访问该共享内存*/
 if (shmctl(shmid, IPC_RMID, 0) == -1)
 {
  fprintf(stderr, "shmctl(IPC_RMID) failed/n");
  exit(EXIT_FAILURE);
 }

 exit(EXIT_SUCCESS);
}
————————————————
版权声明：本文为CSDN博主「寂寞的泡面」的原创文章，遵循 CC 4.0 BY-SA 版权协议，转载请附上原文出处链接及本声明。
原文链接：https://blog.csdn.net/piaojun_pj/article/details/5943736