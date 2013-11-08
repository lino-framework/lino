.. _polly.intro:

==========================
Introduction to Lino Polly
==========================

Lino Polly is a general-purpose web application to manage polls. 
A **poll** is a series of questions which one user asks to the 
other users.
A **response** is when a user answers to a poll.

- A public demo version of :ref:`polly` is available at
  http://polly-demo.lino-framework.org
  (log in as instructed there).
  
- Create new polls : :menuselection:`Polls --> Polls`

- Create your response to a poll : :menuselection:`Polls --> My responses`

- Create more "choice sets" in 
  :menuselection:`Configuration -- > Polls --> ChoiceSets`
  (or click `here <http://polly-demo.lino-framework.org/api/polls/ChoiceSets>`_)
  (a choice set is a reusable set of possible answers to a question. 
  Polly currently supports only  blueprint questions with reusable sets of 
  answers.)

TODO:

- More useful information in the `Results` tab
- Display pending polls on the welcome page
- Printable result sheet
- Workflow & user permissions

- Cannot define multiple choice questions. 
  To remain 3NF, this requires another table



