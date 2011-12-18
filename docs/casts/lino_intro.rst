What is Lino?
=============

In this screencast I'd like to present Lino: 
how a Lino application looks like, 
and what it can do.

Lino is a framework for developing customized database applications.
I've been working on this project during the last years 
and I now start to hope that other programmers will join the project, 
write their own Lino applications 
which they can then offer to their customers.

Here you see the Lino website, 
we are not going to read this together,
I'd rather going to show you the first real-world Lino application,
which is being used since Januar 2011 
in a Public Welfare Centre
in the German-speaking part of Belgium.


How Lino looks like... one remark here.
In fact, Lino is designed to provide different user interfaces, 
but for the moment there's only one choice, 
namely: a Rich Internet Application 
based on the ExtJS Javascript library. 
It doesn't require anything installed on the client machine.

Lino applications will usually run behind a secured web server, 
probably using HTTP authentication.
So the browser will ask once for our username and password.

Here is now the main screen of this Lino application
for Public Welfare Centres.

The application is very specific: it is useful only for 
Public Welfare Centres, and only for Belgian ones.
But we preferred to show you an example
that is being used in the real world , 
not just a fictive tutorial application.
Of course the data we are seing here is *not* real,
everything in this database is fictive data generated for this demo.

As you can see, this application is in German.
It is being translated to French and Dutch 
because there are probably soon other Public Welfare Centres 
going to use it.

I can select the language of the user interface in the user preferences.
This site is configured to provide only three languages.
For this demo I'm going to set it to English.

The welcome screen is a customizable dashbord. 
For this application it shows mainly a list of tasks 
and events for this user.
This might cange soon because I'm working 
on a genuine Calendar panel that is going to use the 
excellent Ext.ensible library.
