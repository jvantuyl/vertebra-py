"""
Evented Scheduler for Vertebra Core
===================================

Tasks plug into the scheduler.  They are either active or pending.  
Pending tasks have some sort of trigger.  When that trigger fires, the 
scheduler makes the task active.

As long as there are active tasks, the scheduler executes their run
function.  Active tasks are executed strictly according to their 
priority.  If they don't specify one, the default priority is 100.

When they run, they are given the a parameter that references what has
caused them to wake up.  This is either a trigger or None if the task 
is active.

When a task needs to sleep, it registers a trigger which signifies the
conditions upon which it will be awakened and then puts itself to sleep.
Note that it is possible to register a trigger without going to sleep.  This
currently doesn't make any sense, but it may be possible to use it to create
recurrent, persistent triggers.

Triggers are specific to the type of scheduler. This coupling is necessary
to simplify the sleeping behavior. If a trigger is able to wake up the loop
when it's idle, then there's really no way to compartmentalize the trigger
from the scheduler's idle function.

When a task runs, its return value can indicate instructions to the
scheduler.  None, unsurprisingly, does nothing.  A list (but not a class
that derives from a list) specifies a list of instructions that are
processed in turn.  Any other value must have a registered "handler".
Values that have no handler cause the task to be aborted.

A handler has a list of types that it provides.  If a value is an instance
of one of these types, then the handler's handle function is called with the
task and the value.  It must return a task, a trigger, or a list of tasks
and triggers.  If a task is already registered with this scheduler, it will
not be added to the queue a second time.

Active tasks are registered with the scheduler via the "add_task" function.
Pending tasks are added via the "add_pending" function, which is called with
the trigger.  It is prefectly safe to schedule more than one task one
trigger.  If the trigger has already been fired, the task will just be set
as active.
"""
