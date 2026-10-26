# GitHub Setup Checklist

## 1. Repository
1. Create a repo `studysync` (private or public; add your instructor if private).
2. Add your teammate as a collaborator (Settings > Collaborators).
3. Push this project: see README "Getting started".
4. Protect `main` (Settings > Branches): require a pull request and 1 approval, require the CI check to pass.

## 2. Labels (Issues > Labels)
`user-story`, `bug`, `iteration-1`, `iteration-2`, `iteration-3`, `optional`, `documentation`, `testing`, `review`

## 3. Milestones (Issues > Milestones)
Iteration 1, Iteration 2, Iteration 3, Final Delivery. Set due dates from the schedule in the proposal.

## 4. Projects board (Projects > New project > Board)
Columns: Backlog, In Progress, Review, Done. Add every issue to it.

## 5. Starter issues (create one per item, link to requirement IDs)
**Iteration 1:** FR1-FR2 registration/login; FR3-FR4 group create/join; FR9 access control; set up CI; deploy to Render.
**Iteration 2:** FR5 sessions; FR6 tasks; FR7 status; FR8 dashboard; FR10 multiple groups.
**Iteration 3:** test gaps and coverage; bug fixes; usability pass; final report; demo script.
**Optional (label `optional`):** O1 .ics export, O2 comments, O3 charts, O4 reminders, O5 RSVP.

## 6. Branch and commit workflow
- Branch per issue: `feature/12-task-status`, `fix/20-login-redirect`
- Commit messages: `Add task status endpoint (#12)`
- Open a PR, the other member reviews, squash and merge. Both of you must commit and review.
