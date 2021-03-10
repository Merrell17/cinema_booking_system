# Timelog

* CINEMA BOOKING SYSTEM
* HUGH MERRELL
* 2310969M
* Mireilla Bikanga Ada


## Week 1

## 29 September 2020
* *1 hour* Read project notes and current cinema trends
* *0.5 hour* initial meeting with supervisor

## 03 October 2020
* *3 Hours* Looked at cinema booking systems, effects of covid and possible ways to take the project e.g web app or phone app
* *1 Hour* Looked at past disertations 

## Week 2

## 05 October 2020
* *0.5 hour* Create Github repo

## 06 October 2020
* *0.5 hour* Group meeting with supervisor
* *0.5 hour* Prepare For Meeting
* *0.5 hour* Main meeting with supervisor
* *0.5 hour* Flesh out notes on what needs to be done and update timelog
* *1 hour* Read Hotel Booking Dissertation in full 

## 09 October 2020
* *2 hours* Looking at pros and cons of Vue and Odeon including mobile apps

## 11 October 2020
* *1 hour* Reading Game Based Learning Dissertation in full

## Week 3

## 12 October 2020
* *3 hours* Reading about cinemas, effects of covid, film delays, streaming competitors and typing up background document.
## 18 October 2020
* *3 hours* Examining existing 3rd party ticket selling websites and the possiblility of developing a web app that sold tickets from multiple sites 

## Week 4

## 19 October 2020
* *3 hours* Deciding what direction to take the project and started created requirements 
## 20 October 2020
* *1.5 hours* Looking further at requirements + meeting prep

## 21 October 2020 
* *2.5* Creating and distributing google forum to refine requirements

## 23 October 2020 
* *3 hours* Re-learning how to make ER diagrams + make ER diagram for cinema booking system

## 25 October 2020 
* *1 hours* Examine google document results + refine requirements 
* *1.5 hours* Write some user stories and software process (agile vs waterfall) 

## 27 October 2020

* *1 hour* Begin wireframe creation process

## 31 October 2020

* *2 hour* Finish Wireframes

## 1 November 2020

* *2 hour* Create System Architecture 

## 2 November 2020

* *1 hour* Database Design


## 7 November 2020

* *2 hour* Modelled addtions to db in drawio and recreated main db in Vertabelo with new payment, address and cinema tables 

## 8 November 2020

* *7 hours* Learnt about activity diagrams and made one for site. Created site map and editted System Architecture diagram.

## 9 November 2020
* *2 hours* Setting up flask on desktop and completed part of tutorial

## 12 November 2020
* *2 hours* Decided on sprint duration and created issues. Installed needed packages, spent some time looking at the offical Flask tutorial and got everything ready to start developing.
* *6 hours* Learned how to get MySQL working with flask, many problems installing MySQL with flask. Eventually got MySQL installed properly but more errors with accounts and errors with Flask.   
* *2 hours* Errors with flask's template engine Werkzeug, fixes on stackoverflow all say the same thing which i have matched, but error still occuring.

## 13 November 2020
* *6 hours* Error gone first time after running program in the morning, restart must have fixed something. Created a database on localhost, connected it to app, built addCinema.html - some issues and implmentation is not very elegant but eventually got the HTLML form working to populate the database. 

## 17 November 2020
* *2 hours* So far all development done on desktop PC. Got project running on laptop which uses a different OS. Some more complications with MySQL but eventually got it running. 

## 21 November 2020
* *2 hours* HTML, CSS & JS Guides
* *2 hours* Trying to make nav bar - lots of erros with style sheet not linking properly and then not styling properly.

## 22 November 2020
* *3 hours* Stopped trying to make nav bar as it was taking up too much time and not providing any functionality to the site. Began working on Add Screen page, more issues with MySQL whilst trying to reformat the DB. Page isnt working quite right

## 24 November 2020
* *2 hours* Getting ready for meeting nav bar looks as it should on laptop and an issue with Add Screen has also fixed itself. New issue to solve with SQL query giving an error.
 
## 30 November 2020
* *2.5 hours* Learning more CSS and Javascript and doing more work on Nav bar which is now almost complete
* *2 hours* Eventually fixed error when searching the database.

## 1 December 2020
* *2.5 hours* Add screen page and Add film page now working. 
* *1 hours* Started create a screening page + meeting prep  

## 10 December 2020
* *4 Hours* Got create a screeening page to work: Issues with MySQL server and displaying cinemas correctly in order with screen numbers, managed to fix.

## 12 December 2020
* *7 Hours* Progressed with Flask tutorial, realised current implentation of project would cause issues down the line and used several bad practises.
refactored all views and templates to use Flask's application factory along with blueprints, a far better design pattern.

## 14 December 2020
* *2 Hours* Desktop died, adjusted MySQL server setup and new depencencies on linux laptop to work with progess made
* *3 Hours* Implemented backend authetication functionality - login, register and logout functionality using Session data. Currently an issue with 
register form data not being posted to MySQL server so Login is not possible.
* *2 Hours* Got Dynamic URL routing working with Cinema Time page. Began creating a data stucture to feed to .html to allow for times to be shown in the correct
order. 

## 18 December 2020
* *6 Hours* Time trying to fix a bug with registration fixed where form data wasnt being posted to the database, asked on forums but no solution. 
## 19 December 2020
* *2 Hours* Found error with login - had db.connect.cursor instead of db.connection.cursor in code which was causing no connection to be established so no data was given.
* *4 Hours* Got full login logout functionality working with session variables.

## 22 December 2020
* *5 Hours* Working on cinema screening page structure. Also tried to get a convinient data structure to give to my HTML template to allow for screenings to show in correct order but SQL understanding wasn't good enough.
## 23 December 2020
* *6 Hours* Went through a full MyMQL crash course and worked on queries

## 24 December 2020
* *5 Hours* Got a query working that gave the correct data to get the cinema screening page working 

## 27 December 2020
* *6 Hours* Polished screening page,

## 28 December 2020
* *5 Hours* Got a rough working seat select page working which counts the number of selected tickets

## 29 December 2020
* *4 Hours* Working out how to get javascipt variable of selected seats back to python, looked in to AJAX, eventually learned I could use a HTML hidden field and append the javascript variable to it and it would be avalible in Python request.  

## 30 December 2020
* *5 Hours* Polishing seat select page and fixed bug with user cookies


## 3 January 2021
* *5 Hours* 

## 4 January 2021
* *5 Hours* 

## 5 January 2021
* *5 Hours* 

## 6 January 2021
* *6 Hours* Time improving HTML, CSS and Javascript

## 7 January 2021
* *6 Hours* Time improving HTML, CSS and Javascript

## 8 January 2021
* *5 Hours* * *6 Hours* Started making cinema seat select page, still struggling with understanding of Javascript and getting squares representing seats to draw correctly

## 9 January 2021
* *5 Hours* Got a rough working seat select page working which counts the number of selected tickets

## 10 January 2021
* *4 Hours* Working out how to get javascipt variable of selected seats back to python, looked in to AJAX, eventually learned I could use a HTML hidden field and append the javascript variable to it and it would be avalible in Python request. 


## 11 January 2021
* *4 Hours* Created and styled payment screen

## 11 January 2021
* *4 Hours* Created and styled booking succesful screen 

## 15 January 2021
* *3 Hours* Added ability to reset details 

## 16 January 2021
* *3 Hours* Added ability to reset password. Also looked in web scraping + beatiful soup library for film details so admins can add films easily. Found IMDbPY library and looked in to using it.
* *1 Hours* Created make deletions page for admin but issues with logisitcs of deleting data e.g user viewing their old bookings. Adding a boolean 'active' field 
might be better solution.

## 17 January 2021
* *3 Hours* Made movie images clickable with page giving details about the film. Added ability to see screenings at various cinemas on this page too.
* *3 Hours* Started looking in to dissertation writing, watched recommended Simon Peyton Jones lecture on writing paper and started writing process. 

## 18 January 2021
* *3 Hours* Added ability to add films by just giving IMBd id, admins no longer have to find and input film info themselves
* *2 Hours* Bug fixing errors on IMBd images not appearing, not all films have usuable images (non existant or poor quality). 
admins will have to select their own even with an IMBd ID.
* *1 Hours* Found another bug where reservation is being created before confirming payment, couldn't find why and currently unfixed.

## 19 January 2021
* *1 Hours* Fixed SQL error when adding film with mutiple directors

## 22 January 2021
* *2 Hours* Decided on best way to store reservation data which was deleted by admin and adjusted ER diagram to represent changes
* *3 Hours* Attempted to implement delete section of backend but query to delete related data but wasn't working nor were suggested fixes. Adjusted database to use ON CASCADE DELETE which made it far simpler. 


## 23 January 2021
* *1 Hours* Implemented front end page for admin deletions and got it working with the backend so deletions were possible
* *3 Hours* Editted MyAccount page to pull data from new table where deleted. Editted booking confirmation page to work with new data.

## 24 January 2021
* *6 Hours* Added styling to admin section and created testing directory. Bug in testing not working with imports, fixed by making __init__.py in testing directory. 

## 25 January 2021
* *2 Hours* Added things from prep doc to dissertation.

## 29 January 2021
* *2 Hours* Polished some frontend + backend code in admin section. Fixed bad key error on hitting submit without having selected cinema. Fixed bug caused by bad logic in function when entering IMDb id and film details.
* *1 Hours* Changed cinema id to auto increment in MySQL. Issue with foreign key address_id and address table whilst inserting cinemas but is fixed.

## 30 January 2021
* *1 Hours* Tried to get clash checking working without needing to store endtime in database but was unfeasable. 
* *3 Hours* Got endtime calculated and stored in database on inserting films. Spent a long time trying to use MySQL's ADD_TIME() function with film duration. Eventually resorted to pulling SQL start_time timestamp, coverting it to python datetime object, adding film duration minutes, coverting back and storing results.    

## 1 Febuary 2021
* *1.5 hours* Dissertation Writing 
* *5 hours* Went through offical Flask tutorials testing section. Fixed bug causing tests not run and completed tests for authentication, Flask app and Admin Section. Revealed bad implementation - using HTML required tag on forms doesn't stop data being posted with HTTP, need to add more checking on user input.    

## 5 Febuary 2021
* *3 hours* Found bug on MyAccount reservation links - when a link is clicked it directs you to a booking confirmation different to the one the one described by the link.
Couldn't find bug, maybe something to do with URL routing.


## 6 Febuary 2021
* *2 hours* Trying to restyle screen times page but timings/bullet list not formatting as expected
* *4 hours* Spent time relearning CSS grid and flexbox. Got a codepen working with a rough template for the screen times page with 7 buckets/week days for screen times to go in.

## 7 Febuary 2021
* *3.5 hours* Redesinged screening page to match template made. Refactored associated Python function to get the next 7 week days and distribute screenings to the correct day.
Screen time page now works as expected. Editted create screening page to order screens by cinema and number.
* *2 hours* wrote some more dissertation.
* *1 hours* Cleaning code, added more visual feedback with message flashing, added database clean up after testing. 
## 8 Febuary 2021
* *2 hours* Looked again for bug in MyAccount reservation links. Checked for URL pattern matching but wasn't the issue. Found bug in python confirmation function - nested SQL query returning mutiple reservations when only one was expected.
* *1 hours* Fixed bug where booking was being created before confirming payment  
* *1 hours* Adding checks to confirmation method ensuring that selected seats weren't already taken (if user pressed back button after booking they could resubmit the same form creating another booking for the same seats) found new bug when creating booking that all chosen seats were set to 0. Reverted to old git commit, issue still present. Used flask's debugger and MySQL workbench to try and find why issue was being caused. 
* *6 hours* Large chain of bugs found, mainly ended up being due to the use of <form action="link_to_next_page".. > rather than having python listening for a POST request with 
  if request.method=='POST' and rerouting to "link_to_next_page" from there. This was triggering the subsequent functions request.method=='POST' which was causing the previous bug with data being inserted before submitting form. Other issues with reservation_id being set to an empty string, list of seats selected being passed to function was being reformatted to a list of single chars, process_ticket function was being rerun when clicking subsequent page causing the selected seats to be set to 'None'.
  Bug fixed refactoring to use using  if request.method=='POST', processing data and redirecting from there. Session variable used to hold selected tickets to stop them being reformatted to list of chars.  
 
 ## 13 Febuary 2021
* *1 hours* Fixed bug in tests, request being redirected before running function 
* *1 hours* Wrote up requirements, formatted user stories.

 ## 22 Febuary 2021
* *5 hours* Wrote up software development methodology, design section and started implementation 

##  27 Febuary 2021
* *0.5 hours* Looked in to various means of launching database and web app
* *4.5 hours* Configured an AWS RDS instance to hold the database. Configured an AWS EC2 instance with necessary requirements to edit RDS instance. Looked in to migrating current database but too time consuming. Many issues with AWS security groups and being denied access to cloud database from local host. Fixed issues and editted code base to be compatible with updated version of MySQL used by RDS and was able to modify AWS hosted database via localhost application. 
##  28 Febuary 2021
* *0.5 hours* Looked in to hosting flask on EC2 along with the database but pythonanywhere was said to be much faster 
* *6 hours* Launched web application on pythonanywhere. More errors connecting to AWS from here and access was denied to the database. Eventually gave up on AWS and decided to launch database on pythonanywhere's database host service. Got web app running, errors with adding films via IMDb id and images loading.  

##  1 March 2021
* *1.5 hours* Images weren't being found on pythonanywhere. Refactored main code base to ensure relative path would be found on pythonanywhere host. Images now loading. 
* *1 hours* Tried to fix IMDb connection error. Found thread saying outbound connections to non-whitelisted were denied without a paid account, imdb.com wasn't on the list which was causing the issue. Will pay for account to fix this when usability testing starts. 
* *1 hours* Remade wireframes
* *1.5 hours* Wrote more implementation chapter of disseration 
* *1 hours* Looked in to usability testing and the possible pros and cons of each method. Google form with link to website and tasks to perform seems most appopriate. 
* *1.5 hours* Fixed small issues with urls, sidebar being overlapped by form entries and website errors when entering certain urls e.g for a reservation that doesn't exist. 

##  3 March 2021
* *1 hours* Improved spanning of nav bar on smaller windows 
* * *3 hours* Fixed screening dates overflowing when too many were added to one day. Added the ability to press next and previous week for the same page. 

##  4 March 2021
* *5 hours* Added animation to film images on hovering. Added a 'coming soon' image to fill white space when site is empty. Made images on film times page clickable. Added handling of IDBd's that closely resemble correct format. Corrected seat number shown by confirmation page.


##  6 March 2021
* *10 hours* Editted Google usablity form. Spent rest of the day preparing site for usability test - improving site styling on mobile, allowing users to add films without images. Added links to cinemas which were screenings a given film from that film's page. Errors with pythonanywhere database not matching localhost's schema, updated .sql file and fixed database. Fixed bug with bad logic in session variables causing wrong cinema to be displayed. Fixed bug with pythonanywhere not displaying images properly.  Fixed bug with pythonanywhere not deleting images properly. Fixed payment form being squashed on mobile devices. Attempted to fix bug with safari not allowing html5 datetime input form - couldn't fix, admins cant create screenings on iphones. Fixed issue caused by cinemas with spaces in name. 

##  8 March 2021
* *2.5 hours* Completed Usability form
* *2.5 hours* Dissertation Work

##  9 March 2021
* *4 hours* Dissertation Work
