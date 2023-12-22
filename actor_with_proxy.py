
import threading 
import time 
import pykka 

def log(msg):
    thread_name = threading.current_thread().name 
    print(f"{thread_name}: {msg}")

class AnACtor(pykka.ThreadingActor):
    field = "this is the value of AnActor field"
    
    def proc(self):
        """ print the actor running status"""
        log("this was the printed by AnActor.proc()")
    
    def func(self):
        time.sleep(0.5)
        return "this was returned by AnActor.func() after a delay"

if __name__ == "__main__":
    actor = AnACtor.start().proxy()
    for _ in range(3):
        #Method with side effect
        log("calling for AnActor.proc() ...")
        actor.proc()
        
        #Method with return value
        log("calling AnActor.func() ...")
        result = actor.func()
        log("priting result .... (blocking)")
        log(result.get())
        
        #field reading
        log("reading An actor field")
        result = actor.field
        log("print result ... (blocking)")
        log(result.get())
        
        #field writing 
        log("writing AnActor.field ...")
        actor.field= "new value"
        result = actor.field 
        log("printing new field value ... (blocking)")
        log(result.get())
    actor.stop()