# Iteration 1 Review and Retrospective

**Dates:** Oct 22, 2026 to Oct 27, 2026 | **Attendees:** Mohamed Alarbah, Mohamed Abdullah

## Planned vs. completed
| Issue # | Story | Status |
|---|---|---|
| #1 | Registration and login | Done |
| #2 | Create and join groups | Done |
| #3 | Group access control | Done |
| #4 | Deploy first version to Render | Done |
| #13 | Use a persistent database (added during iteration) | Done |

## Demo / evidence
Live app: https://studysync-tkty.onrender.com
Screenshots and verification notes are in the comments on issues #1, #2, #3, #4 and #13.

## What went well
- CI ran the tests on every pull request and caught problems early.
- The project board flow (Backlog, In Progress, Review, Done) worked once the automation was fixed.
- Pull request reviews between both members.

## What did not go well
- The Render Blueprint defaulted to a paid plan until we added `plan: free`.
- The free tier reset our SQLite data, so accounts disappeared after restarts.
- The first database driver setup failed because SQLAlchemy needed `postgresql+psycopg2://`.

## Changes for the next iteration
- Test every feature on the live site, not only locally.
- Create a bug issue for each defect and fix it through a reviewed pull request.
- Add free-tier and database limits to the risk list.

## Scope changes and justification
Added a persistent database (Neon Postgres) in Iteration 1 instead of Iteration 3, because the free hosting reset user accounts and blocked testing. No features were removed.
