import sys
from pathlib import Path
ROOTPATH=str(Path(__file__).parent)
sys.path.append(ROOTPATH)

from src import SnakeController
from src import map

from socket import socket,AF_INET,SOCK_DGRAM,timeout,SOL_SOCKET,SO_RCVBUF
import numpy as np
import time
from multiprocessing import Pool,Manager,Process,Array,Value
import ctypes


def receive_message(values,is_write):
        
    sock=socket(AF_INET,SOCK_DGRAM)
    sock.setsockopt( 
            SOL_SOCKET, 
            SO_RCVBUF, 
            65536) 
    sock.settimeout(0.2)
    sock.bind(("",5000))
    
    t_now = time.perf_counter()
    t_pre = time.perf_counter()
    t_interval = 0.05 # カメラと同期

    while True:
        t_now = time.perf_counter()
        if (t_now - t_pre < t_interval):
            continue
        t_pre = t_now
        
        t=time.time_ns()
        try:
            msg=sock.recv(256)
            msg=msg.decode(encoding="utf-8")
            joint_radian=[float(rad) for rad in msg.split(",")]
            # print(joint_radian[0])
            print(joint_radian)
            joint_count=map(np.array(joint_radian),input_max=np.pi/2.0,input_min=-np.pi/2.0,
                                output_max=4095,output_min=0)
            
            is_write.value=True
            for i in range(len(values)):
                values[i]=int(joint_count[i])
            is_write.value=False
            
        except timeout:
            print("socket timeout")
        except KeyboardInterrupt:
            break
        # print((time.time_ns()-t)/(10**9))
        
    sock.close()



def control_snake(snake_controller,values,is_write):
    
    start_time=time.time_ns()
    
    is_quit=False
    while not is_quit:
        t=time.time_ns()
        try:
            if not is_write.value:
                
                # #蛇のコントロール
                joint_count=np.zeros(12)
                joint_count=[val for val in values]

                snake_controller.write_goal_position(
                    np.array(joint_count,dtype=int)
                )
                
            else:
                pass
                # print(time.time(),"No data...")
                 
        except KeyboardInterrupt:
            is_quit=True
            
    print("done")


def main():
    
    values=Array(ctypes.c_short,[0]*12)
    for i in range(12):
        values[i]=0
    
    is_write=Value(ctypes.c_bool,False)
    is_write.value=False
    
    
    snake_controller=SnakeController() #インスタンス化
    snake_controller.set_initial_position() #蛇をまっすぐにする
    time.sleep(3)
    snake_controller.torque_enable() #サーボを待機状態にset
    
    process1=Process(target=receive_message,args=(values,is_write))
    process1.start()
    
    process2=Process(target=control_snake,args=(snake_controller,values,is_write))
    process2.start()
    
    process1.join()
    process2.join()
    
            

if __name__=="__main__":
    main()