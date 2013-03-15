online_safe2eat
===============

Django Version of the Safe2Eat package


safe2eat is, obviously, a very simply program. my original intention was to have my mentorship program up and running, but once it was up on the VM under apache, the circular references built into the (apperently poor) design bit me.

The program worked great on my own machine, but when I moved it up, the pace of the imports must have changed in a way I don't understand, though I do know now how the circular dependencies bite one in the ass. I tried various workarounds and felt myself getting in deeper and deeper with code that was becoming harder and harder to read, and thus harder to debug. In the end, I had to raise the white flag and quickly move in another direction.

I decided to port my api mashup to django as another exercise, that of porting code. Fortuantely for me, I was able to put it all together fairly quickly. This was only becuase of all the time I had spent with Django on my other project, and the fact that I had already figured out how to deploy Djago apps on the VM. 

I wish I had had more time to work on this second project, as there are many pieces I would love to add. I would add a map that would change when you clicked a particular restaurant. Then I could also add directions. Also, I would like to make it so one could get the next 20 restuarants. There are many ways it could be improved, but for now it is, at least from what I can tell, a successful deployment of the mashup.

As for the MentorFinder program, I will be digging into that next quarter, tearing it down, and redesigning it with what I've learned. I think my desire to break it in to small components blinded me to where the code moved instead. If a class has a heavy dependency on another particular class, perhaps it is best to placce them in the same module. 

Thanks for a great class. It was a blast and I leanred a ton. 


Chris Overly