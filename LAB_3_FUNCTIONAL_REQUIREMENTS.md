# Field Technician App

## 1. Purpose

The application will help a service company coordinate field technicians, customers, service jobs, and work progress. 

## 2. Users

The application will support two main user roles.

### Dispatcher

A dispatcher coordinates service work. A dispatcher needs to:

- Find and create customers.
- Create service jobs.
- Schedule jobs.
- Assign jobs to technicians.
- Monitor active, overdue, and unscheduled jobs.
- See when a technician has requested help.
- Review and update job details.

### Technician

A technician performs service work. A technician needs to:

- See jobs assigned to them.
- See scheduled and unscheduled work separately.
- Open a job and review its details.
- Update job progress.
- Mark whether they are on site.
- Complete a work checklist.
- Record equipment being serviced.
- Add notes and photos.
- Request help from a dispatcher.

## 3. First-Time User Setup

1. A signed-in user who does not yet have an application profile should be taken to a profile setup page.
2. The user must enter a display name.
3. The user may enter a phone number.
4. The user must choose either the dispatcher role or the technician role.
5. After choosing a role, the user must choose a service region.
6. The user should be able to select an existing region.
7. The user should be able to create a new region if the needed region does not exist.
8. The newly created region should be assigned to the user.
9. After setup, a technician should be taken to the technician home page.
10. After setup, a dispatcher should be taken to the dispatcher home page.
11. The application should explain what information is missing if setup cannot be completed.

## 4. Service Regions

1. A service region represents a geographic area in which the company performs work.
2. Every job must belong to one service region.
3. Every user profile must be assigned to at least one service region.
4. A region must have a name.
5. A region may have a description.
6. When a dispatcher creates a job, the application should use the dispatcher's first assigned region as the initial selection when possible.
7. The dispatcher should still be able to choose a different available region.

## 5. Dispatcher Home Page

The dispatcher home page should provide a quick view of work that needs attention.

1. The page should show jobs where a technician has requested help.
2. The page should show scheduled jobs whose scheduled start time has passed and which are not finished.
3. The page should show jobs that do not have a scheduled date and time.
4. The page should show jobs that are currently being worked.
5. Each job summary should show the job title, current status, and the most useful available date or time.
6. A job that needs help should have a clear visual indicator.
7. A help request should show the technician's explanation when one is available.
8. Selecting a job should open the job details.
9. The dispatcher should be able to open customer search.
10. The dispatcher should be able to start creating a new job.
11. The dispatcher should be able to refresh the page manually.
12. The page should refresh job information automatically at a reasonable interval, such as every 30 seconds.
13. Each section should show a clear empty message when it has no jobs.
14. The page should show an understandable error if job information cannot be loaded.

## 6. Technician Home Page

The technician home page should show work assigned to the signed-in technician.

1. The page should show upcoming scheduled jobs that are not complete or abandoned.
2. Scheduled jobs should be ordered from the earliest scheduled time to the latest.
3. The page should show assigned jobs that do not have a scheduled date and time.
4. Unscheduled jobs should show the most recently updated jobs first.
5. The page should show complete and abandoned jobs separately from active work.
6. Finished jobs should show the most recently updated jobs first.
7. Each job summary should show the job title and current status.
8. A scheduled job should show its scheduled date and time.
9. An unscheduled job should show when it was last updated.
10. A job that needs help should have a clear visual indicator.
11. Selecting a job should open the job details.
12. The technician should be able to refresh the page manually.
13. The page should refresh job information automatically at a reasonable interval, such as every 30 seconds.
14. Each section should show a clear empty message when it has no jobs.
15. The page should show an understandable error if job information cannot be loaded.

## 7. Customer Search

1. A dispatcher should be able to search for a customer by phone number.
2. The search should not run when the phone-number field is empty.
3. The dispatcher should be able to start a search by selecting the search action or pressing Enter.
4. Search results should show the customer's name and phone number.
5. Search results should also show the customer's email address when available.
6. Search results may show the customer's address when available.
7. The application should show a clear message when no customers are found.
8. The application should show progress while a search is running.
9. The application should show an understandable error when a search fails.

## 8. Customer Creation

1. A dispatcher should be able to create a customer from the customer search page.
2. A dispatcher should also be able to create a customer while creating a job.
3. A customer must have a name.
4. A customer must have a phone number.
5. A customer may have an email address.
6. A customer may have an address.
7. If customer creation starts after a phone search, the entered phone number should be carried into the new-customer form.
8. After a customer is created during job creation, that customer should become the selected customer for the job.
9. After a customer is created from customer search, the new customer should appear in the results.
10. The application should confirm successful customer creation.
11. The application should explain why a customer could not be created.

## 9. Job Creation

1. A dispatcher should be able to create a service job.
2. The dispatcher must select a customer.
3. The dispatcher must enter a short job title.
4. The dispatcher may enter a longer description.
5. The dispatcher must select a service region.
6. The dispatcher may choose a scheduled date and time.
7. The dispatcher may assign a technician.
8. The dispatcher should be able to leave the job unassigned.
9. The technician list should contain users whose role is technician.
10. A job without a scheduled date and time should begin as an unscheduled new job.
11. A job with a scheduled date and time should be treated as scheduled work.
12. The application should not create a job when required information is missing.
13. The application should clearly identify that the customer, title, and region are required.
14. The create action should be disabled while the job is being saved.
15. The application should confirm successful job creation.
16. After creation, the dispatcher should return to the dispatcher home page.
17. The application should show an understandable error if the job cannot be created.

## 10. Photos

1. A user should be able to attach one image to a new job note.
2. A user should be able to choose an existing image from the device.
3. When the browser and device support it, a user should be able to take a photo with the camera.
4. The user should see a preview before saving the note.
5. The user should be able to remove the preview and choose another image.
6. The saved image should appear with the note in the job history.
7. The camera view should allow the user to capture a photo or cancel.
8. The application should explain when camera access is unavailable or denied.
9. A failed image or note save should not be shown as successful.

## 11. Job Details Page

1. The job details page should show the job title and current status.
2. The page should show the customer name when available.
3. The page should show the job description when available.
4. The page should show and allow updates to status, schedule, and on-site state.
5. The page should include the help-request area, work checklist, equipment, and job history.
6. The user should be able to return to the previous page.
7. The page should show progress while job information is loading.
8. The page should show a clear message when the job does not exist.
9. The page should show a clear message when job information cannot be loaded.
10. Related customer, equipment, checklist, and history information should be loaded with the job.

## 12. Sample Data

Include a sample-data page to make the application easier to explore.


The implementation may make reasonable technical and visual choices that are not covered here, provided those choices support these business requirements and keep it understandable.
