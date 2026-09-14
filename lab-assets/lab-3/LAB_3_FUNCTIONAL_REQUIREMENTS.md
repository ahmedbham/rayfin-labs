# Field Technician App

## 1. Purpose

The application will help field technicians review their assigned service jobs, manage work progress, document service activity, and request assistance. Dispatches, including customer management, job creation, scheduling, and technician assignment, are handled in a separate application.

## 2. Users

The application supports field technicians. A technician needs to:

- See jobs assigned to them.
- See scheduled and unscheduled work separately.
- Open a job and review its details.
- Update job progress.
- Mark whether they are on site.
- Complete a work checklist.
- Record equipment being serviced.
- Add notes and photos.
- Request assistance.

## 3. First-Time User Setup

1. A signed-in user who does not yet have an application profile should be taken to a profile setup page.
2. The user must enter a display name.
3. The user may enter a phone number.
4. The user must choose a service region.
5. The user should be able to select an existing region.
6. The user should be able to create a new region if the needed region does not exist.
7. The newly created region should be assigned to the user.
8. After setup, the user should be taken to the technician home page.
9. The application should explain what information is missing if setup cannot be completed.

## 4. Service Regions

1. A service region represents a geographic area in which the company performs work.
2. Every job must belong to one service region.
3. Every user profile must be assigned to at least one service region.
4. A region must have a name.
5. A region may have a description.

## 5. Technician Home Page

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

## 6. Job Details Page

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

## 7. Sample Data

Include a sample-data page to make the application easier to explore.


The implementation may make reasonable technical and visual choices that are not covered here, provided those choices support these business requirements and keep it understandable.
