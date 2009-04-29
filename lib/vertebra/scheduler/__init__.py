"""
Evented Scheduler for Vertebra Core
===================================

Tasks plug into the scheduler.  They are either active or pending.  
Pending tasks have some sort of trigger.  When that trigger fires, the 
scheduler makes the task active.

Active tasks are registered with the scheduler via the "schedule" function.

As long as there are active tasks, the scheduler executes their run
function.  For priority schedulers, active tasks are executed strictly
according to their priority, from lowest to highest.

When they run, they are given the a parameter that references what has
caused them to wake up.  This is either a trigger or the scheduler if the
task is active.

When a task needs to sleep, it returns a trigger which signifies the
conditions upon which it will be awakened and then puts itself to sleep.

Triggers are specific to the type of scheduler. This coupling is necessary
to simplify the sleeping behavior. If a trigger is able to wake up the loop
when it's idle, then there's really no way to compartmentalize the trigger
from the scheduler's idle function.

When a task runs, its return value can indicate instructions to the
scheduler.  Since failure to return a value effectively returns None,
we log a warning and unschedule a task if this is returned.  Your task
iteration should always return something.

If the return value is a list (but not a class that derives from a list)
specifies a list of instructions that are processed in turn.

If the return value is a task, it will schedule that task and unschedule
the current task.

If an Exception is raised, it's caught and passed in as if it had been
returned.

Any other value must have a registered "handler".  Values that have no
handler cause the task to be aborted, just None.

A handler has a list of types that it provides.  If a value is an instance
of one of these types, then the handler's handle function is called with
the task and the value.  It must return a task, a trigger, or a list of
tasks and triggers.  If a task is already registered with this scheduler,
it will not be added to the queue a second time.

The behavior of None, triggers, and tasks are actually implemented with
handlers.  Since most IPC and sleeping functionality is likely to be
closely tied to the scheduler, there are no other handlers provided by
default.

Presumably, any IPC or sleeping functionality will be provided by related
sets of handlers and triggers.  Additional handlers can be passed to the
scheduler at creation time.
"""

from scheduler import (BaseScheduler,BusyScheduler,
                      ThreadSafePQueue,SimplePQueue)
from handler import Handler,NoneHandler
from sentinel import Sentinels,BaseSentinelHandler
from task import Task,TaskHandler,NoopOnceTask,NoopCountTask
