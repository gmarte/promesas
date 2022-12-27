# CS50W Final Project - Promises

- [CS50W Final Project - Promises](#cs50w-final-project---promises)
  - [Overview](#overview)
  - [Distinctiveness and Complexity](#distinctiveness-and-complexity)
  - [File structure description](#file-strcuture-descriotion)
  - [How to run the application](#how-to-run-the-application)
  - [Features I would like to improve/add](#todo-list)


## Overview
It is common for politicians to make promises to the public as a way of campaigning for office and attempting to gain the support of voters. These promises can cover a wide range of issues, from policy positions to specific initiatives or programs that the politician plans to implement if elected. However, it is also not uncommon for politicians to fail to follow through on their promises once they are in power.

There are a number of reasons why politicians might fail to deliver on their promises. One reason is that the demands and realities of governing can be very different from what was anticipated during the campaign. Politicians may find that it is more difficult to implement their ideas or policies than they had anticipated, or that they face unforeseen obstacles or resistance.

Another reason is that politicians may make promises that are simply unrealistic or unsustainable. In the heat of a campaign, it can be tempting to make grandiose promises that are not feasible in the long term, in order to appeal to voters. Once in office, these politicians may find that they are unable to follow through on these promises, either because of a lack of resources or political support.

Finally, some politicians may simply be more interested in getting elected than in fulfilling their promises once in office. They may make promises that they have no intention of keeping in order to win votes, and then neglect to follow through on those promises once they are in power.

The current president of the Dominican Republic, Luis Abinader, and several politicians from his party, Partido Revolucionario Moderno, have made an excessive number of promises that are unrealistic. In response, I have created this website to hold them and future politicians accountable for their promises.

## Distinctiveness and Complexity

I have designed and developed a web application using Django, REST framework, and Bootstrap to fulfill the requirements of the assignment.

- [x] Your web application must be sufficiently distinct from the other projects in this course (and, in addition, may not be based on the old CS50W Pizza project), and more complex than those.
  - [x] A project that appears to be a social network is a priori deemed by the staff to be indistinct from Project 4, and should not be submitted; it will be rejected.
  - [x] A project that appears to be an e-commerce site is strongly suspected to be indistinct from Project 2, and your README.md file should be very clear as to why it’s not. failing that, it should not be submitted; it will be rejected.
- [x] Your web application must utilize Django (including at least one model) on the back-end and JavaScript on the front-end.
- [x] Your web application must be mobile-responsive.

### Features

The web application has a database of promises made by politicians. These promises could are entered manually by users or admins collected from public statements made by politicians.
Each promise would have following status: 
| STATUS | DESCRIPTION |
| ------ | ------ |
| COMPLETE | The promise is mostly or completely fulfilled.
| IN PROGRESS | The promise is in the works or being considered.
| STALLED | Could occur due to inaction by administration or lack of support from legislative branch.
| BEHIND SCHEDULE | No progress, perhaps due to financial limitations, opposition from lawmakers or a change in priorities.
| INCONCLUSIVE | Every promise begins at this level and retains this rating until evidence of progress or proof that it has been shelved.
| UNSTARTED | The promise is accomplished only in part, but has succeeded at least in part consistently with the goal of the promise.

- Users of the web application can search for promises by politician, by keyword, by date, by evidences or by status.
- The web application provides reports for the users to track on the progress of a promise, such as by providing updates or evidence of fulfillment.
- The web application also provide a dashboard for tracking the performance of politicians and party over time, such as by displaying graphs showing the percentage of promises and their status.
- To ensure the accuracy and impartiality of the information on the web application, it would be moderated by a team of independent fact-checkers.

Overall, the goal of this web application is to provide a transparent and accountable to track and report on the promises the politicians have made to the public.

## File Structure Description
```
|   .gitignore
|   db.sqlite3
|   manage.py
|   README.md
|   requeriments.txt
|   
+---data
|       party.csv
|       politician.csv
|       position.csv
|       promise.csv
|       rating.csv
|       user.csv
|       
+---media
|   +---parties
|   |       Logo_del_partido_Fuerza_del_Pueblo.png
|   |       Partido_Reformista_Social_Cristiano.png
|   |       PLD_Dominican_Republic_logo.png
|   |       PRM_LOGO.png
|   |       
|   \---politician
|           220px-Faride_Raful.png
|           220px-Faride_Raful_VjsqLhe.png
|           itobisono.jpg
|           luis_abinader.jpg
|           PRM_LOGO.png
|           WIN_20220620_12_24_10_Pro.jpg
|           
+---promesas
|   |   asgi.py
|   |   settings.py
|   |   urls.py
|   |   wsgi.py
|   |   __init__.py
|   |   
|           
+---promise_tracker
|   |   admin.py
|   |   apps.py
|   |   forms.py
|   |   models.py
|   |   routers.py
|   |   serializers.py
|   |   tests.py
|   |   urls.py
|   |   views.py
|   |   __init__.py
|   |          
|   +---static
|   |   \---promise_tracker
|   |           chart.js
|   |           datatables-simple-demo.js
|   |           materials.js
|   |           script.js
|   |           style.css
|   |           variables.js
|   |           
|   +---templates
|   |   +---party
|   |   |       party_confirm_delete.html
|   |   |       party_detail.html
|   |   |       party_form.html
|   |   |       party_list.html
|   |   |       
|   |   +---politician
|   |   |       politician_confirm_delete.html
|   |   |       politician_detail.html
|   |   |       politician_form.html
|   |   |       politician_list.html
|   |   |       
|   |   +---position
|   |   |       position_confirm_delete.html
|   |   |       position_detail.html
|   |   |       position_form.html
|   |   |       position_list.html
|   |   |       
|   |   +---promise
|   |   |       promise_confirm_delete.html
|   |   |       promise_detail.html
|   |   |       promise_form.html
|   |   |       promise_list.html
|   |   |       
|   |   \---promise_tracker
|   |           index.html
|   |           layout.html
|   |           login.html
|   |           paginator.html
|   |           promise_form.html
|   |           promise_list.html
|   |           register.html
|   |           
```
## How to run the application

## TODO List


